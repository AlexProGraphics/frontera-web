# Requisitos oficiales de Apple para la web de Frontera

Fuentes consultadas el 18 de noviembre de 2026. Esta matriz distingue los
requisitos documentados de Apple de las decisiones de implementación de la web.
No constituye una garantía de aprobación ni sustituye la revisión del binario.

## Fuentes y aplicación a esta web

| Requisito oficial | Aplicación en Frontera |
| --- | --- |
| [App Review 5.1.1(i)](https://developer.apple.com/app-store/review/guidelines/#data-collection-and-storage): política enlazada en los metadatos de App Store Connect y accesible dentro de la app. Debe identificar datos, recogida, usos, terceros y protección, conservación/borrado y retirada del consentimiento. | La ruta `/privacy/` describe tipos de HealthKit, datos manuales, cálculo y almacenamiento local, widget, permisos, exportación, copias y eliminación. **Pendiente fuera de esta web:** enlazar la URL real desde la app y App Store Connect. |
| [Campo Privacy Policy URL](https://developer.apple.com/help/app-store-connect/reference/app-information/app-privacy/): obligatorio para todas las apps. User Privacy Choices URL es opcional. | Usar la URL HTTPS real de `/privacy/`. Se puede usar `/privacy/#eliminar` para las opciones de privacidad. No introducir una URL provisional o inaccesible. |
| [Campo Support URL](https://developer.apple.com/help/app-store-connect/reference/app-information/platform-version-information/): debe llevar a información de contacto real —dirección legal, email o teléfono, según lo que exija la ley local— para problemas, comentarios y sugerencias. [App Review 1.5](https://developer.apple.com/app-store/review/guidelines/#developer-information) exige contacto fácil, exacto y actualizado. | `/support/` ofrece ayuda y el correo público de soporte y privacidad **amdelamorena@icloud.com**, aprobado por Alejandro y enlazado también en la política. Verificar además los datos legales de contacto exigibles según titular y territorios. |
| [App Review 2.1(a)](https://developer.apple.com/app-store/review/guidelines/#app-completeness): metadatos completos y URL funcionales; eliminar marcadores, webs vacías y contenido temporal antes de enviar. | Se han retirado el contacto de ejemplo y los avisos de preparación. `check-site.py --release` sigue bloqueando la reintroducción de marcadores; el resultado no sustituye la revisión del binario y sus metadatos. |
| [App Review 5.1.3(i)](https://developer.apple.com/app-store/review/guidelines/#health-and-health-research): no usar datos de salud para publicidad, marketing o minería de perfiles; declarar los datos específicos de salud que se obtienen. | La política enumera las categorías concretas, sus fines de bienestar y la ausencia de anuncios, venta, seguimiento o envío a servidores de Frontera. Revalidar con el binario final y sus SDK. |
| [App Review 5.1.3(ii)](https://developer.apple.com/app-store/review/guidelines/#health-and-health-research): no escribir datos falsos o inexactos en HealthKit ni almacenar información personal de salud en iCloud. | La web explica la escritura opcional y no promete exclusión de backups sin verificarla. **Pendiente en la app:** auditar persistencia, contenedor del widget y copias. No declarar cumplimiento de esta norma solo por tener una política. |
| [App Review 1.4.1](https://developer.apple.com/app-store/review/guidelines/#physical-harm): las afirmaciones de salud requieren metodología justificable y se debe recordar consultar al médico antes de tomar decisiones médicas. | Inicio, privacidad y soporte indican que Frontera es de bienestar, no un dispositivo médico, y que no sustituye al profesional sanitario. La web no hace promesas de diagnóstico ni de exactitud clínica. |
| [App Privacy Details](https://developer.apple.com/app-store/app-privacy-details/): las respuestas deben reflejar lo que la app y sus terceros realmente recogen. «Collect» se refiere a transmisión fuera del dispositivo con acceso por más tiempo que la petición en tiempo real. | No confundir uso local de HealthKit con recogida por un servidor, ni copiar «no recopila datos» sin auditar el binario, SDK y flujos opcionales. La etiqueta App Privacy es una declaración independiente de la web. |

## Lista antes de usar las URL en una entrega

- [x] Sustituir el correo de ejemplo por el contacto público aprobado: amdelamorena@icloud.com.
- [ ] Confirmar la identidad pública/legal del responsable y los datos exigibles.
- [x] Eliminar los avisos temporales de preparación y contacto pendiente.
- [ ] Aprobar la política final y su fecha de vigencia.
- [ ] Ejecutar `python3 scripts/check-site.py --release` con resultado correcto.
- [ ] Abrir las URL públicas HTTPS de privacidad y soporte sin iniciar sesión.
- [ ] Probar navegación móvil, enlaces, contacto y pasos de borrado contra la app final.
- [ ] Enlazar la política y soporte desde Ajustes de la app y desde App Store Connect.
- [ ] Auditar iCloud/backups, permisos efectivos y ausencia de SDK o envíos no declarados.
- [ ] Completar las respuestas de App Privacy y el manifiesto correspondiente al binario.

## Qué no afirma Apple en estas fuentes

No se exige un dominio propio ni alojar el código de la app en público. GitHub
Pages es una elección técnica para servir páginas HTTPS públicas y accesibles,
no una certificación de Apple. La política no autoriza prácticas que las normas
de HealthKit prohíben, aunque las describa con transparencia.

La eliminación de cuenta dentro de la app de 5.1.1(v) se aplica si la app permite
crear cuentas. Frontera no requiere una cuenta propia; eso no elimina la necesidad
de explicar cómo borrar datos locales, de Salud, exportados o de soporte.
