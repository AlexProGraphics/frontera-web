#!/usr/bin/env python3
"""Dependency-free checks for the static site; never builds or deploys it."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

SITE = Path(__file__).resolve().parents[1] / "website"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = set()
        self.links = []
        self.errors = []
        self.h1_count = 0
        self.main_count = 0
        self.has_language = False
        self.has_viewport = False
        self.has_description = False
        self.has_title = False
        self.release_blocked = False

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            identifier = attrs["id"]
            if identifier in self.ids:
                self.errors.append(f"duplicate id: {identifier}")
            self.ids.add(identifier)
        self.h1_count += tag == "h1"
        self.main_count += tag == "main"
        self.has_language |= tag == "html" and attrs.get("lang") == "es"
        self.has_title |= tag == "title"
        self.has_viewport |= tag == "meta" and attrs.get("name") == "viewport"
        self.has_description |= (
            tag == "meta" and attrs.get("name") == "description"
            and bool(attrs.get("content"))
        )
        self.release_blocked |= "data-release-blocker" in attrs
        if tag in {"script", "iframe", "form", "object", "embed"}:
            self.errors.append(f"unexpected active content: {tag}")
        if tag == "img" and "alt" not in attrs:
            self.errors.append("image missing alt attribute")
        for attribute in ("href", "src"):
            if attribute in attrs:
                self.links.append((tag, attribute, attrs[attribute]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", action="store_true",
                        help="also reject draft markers and placeholder contacts")
    args = parser.parse_args()
    pages = {}
    errors = []
    for path in sorted(SITE.rglob("*.html")):
        page = Page(path)
        source = path.read_text(encoding="utf-8")
        page.feed(source)
        page.close()
        pages[path.resolve()] = page
        for valid, label in (
            (page.has_language, "Spanish document language"),
            (page.has_title, "page title"),
            (page.has_description, "meta description"),
            (page.has_viewport, "mobile viewport"),
            (page.h1_count == 1, "exactly one h1"),
            (page.main_count == 1, "exactly one main landmark"),
        ):
            if not valid:
                page.errors.append(f"missing or invalid {label}")
        if args.release and (page.release_blocked or re.search(
            r"frontera\.example|CONTACTO_PUBLICO_PENDIENTE", source,
            flags=re.IGNORECASE
        )):
            page.errors.append("release blocked: draft banner or placeholder contact remains")

    if len(pages) != 3:
        errors.append(f"expected 3 site pages, found {len(pages)}")
    for path, page in pages.items():
        for tag, attribute, link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                if url.scheme not in {"https", "mailto"}:
                    page.errors.append(f"unsupported link scheme: {link}")
                if tag != "a" or attribute != "href":
                    page.errors.append(f"remote asset is not allowed: {link}")
                if url.scheme == "mailto" and ".example" in link:
                    page.errors.append("placeholder contact must not be a working mailto link")
                continue
            if url.path.startswith("/"):
                page.errors.append(f"root-relative link breaks project Pages paths: {link}")
                continue
            target = ((path.parent / unquote(url.path)).resolve()
                      if url.path else path)
            if not target.is_relative_to(SITE.resolve()):
                page.errors.append(f"link leaves publish directory: {link}")
                continue
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                page.errors.append(f"missing link or asset: {link}")
            elif url.fragment:
                destination = pages.get(target)
                if destination is None or unquote(url.fragment) not in destination.ids:
                    page.errors.append(f"missing anchor target: {link}")
        errors.extend(f"{path.relative_to(SITE)}: {error}" for error in page.errors)

    if errors:
        print("Site checks failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    link_count = sum(len(page.links) for page in pages.values())
    print(f"PASS: {len(pages)} pages; {link_count} links/assets; language, landmarks and metadata.")
    print("Release guard passed." if args.release else
          "Preview checks only. Run with --release before App Store submission; human approval is still required.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
