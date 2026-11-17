# Frontera · Privacidad y soporte

Sitio público e independiente para la app de bienestar **Frontera**. Este
repositorio contiene únicamente la web y sus comprobaciones: **no contiene el
código, historial de Git, fixtures ni datos de usuarios de la app iOS**.

## Contenido

- `website/index.html`: presentación y accesos a privacidad y soporte.
- `website/privacy/`: política y controles de privacidad.
- `website/support/`: preguntas frecuentes y contacto.
- `docs/apple-requirements.md`: requisitos oficiales de Apple y comprobaciones
  pendientes antes de usar las URL en App Store Connect.

## Desarrollo local

Python 3.10 o posterior, sin paquetes adicionales:

```sh
python3 scripts/check-site.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory website
```

Abrir `http://127.0.0.1:8000/`, `/privacy/` y `/support/`. El sitio no utiliza
JavaScript ni recursos remotos y admite el prefijo de proyecto de GitHub Pages.

## Publicación y App Store Connect son pasos distintos

El titular ha autorizado una web pública independiente. La publicación puede
servir para revisar su contenido, pero **no significa que esté lista para
App Review** mientras conserve el correo de ejemplo, el aviso de preparación
o cualquier requisito pendiente de la matriz de Apple.

`soporte@frontera.example` es un marcador visible y no operativo. No se debe
sustituir por una dirección privada encontrada en metadatos de Git o del proyecto.
Solo el titular puede aprobar qué dirección se hace pública.

Antes de enviar la app:

```sh
python3 scripts/check-site.py --release
```

Esta comprobación falla deliberadamente mientras existan avisos o marcadores.
No es una certificación legal ni garantiza la aprobación de Apple.

## GitHub Pages

El sitio servido debe contener **solo los archivos de `website/`**. No publicar
la raíz del repositorio privado de la app, su documentación, sus exportaciones
ni sus fixtures. La rama de despliegue `gh-pages` contiene únicamente esos
archivos públicos; la configuración de Pages usa `gh-pages` y la carpeta `/`.

La primera publicación se puede hacer desde el contenido revisado de una PR
sin fusionarla, creando un commit de artefactos en `gh-pages`. Las PR del sitio
siguen abiertas hasta que el titular autorice su fusión; publicar la web no
autoriza a fusionar cambios de la app ni a cambiar su visibilidad.

Para actualizar después de revisar una PR, copiar únicamente `website/` a la
rama de publicación, ejecutar los checks y publicar ese commit. La rama fuente
y el commit desplegado deben quedar identificados en la PR. Revisar las URL
HTTPS resultantes sin sesión iniciada antes de introducirlas en App Store Connect.

La integración continua de este repositorio solo valida archivos y enlaces.
No publica cambios automáticamente ni utiliza permisos de escritura de Pages.

Documentación oficial de [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
