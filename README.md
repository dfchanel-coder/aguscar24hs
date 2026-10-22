# AGUSCAR · Auxilio y traslado

Sitio estático en español y portugués. Se puede publicar directamente desde la raíz del repositorio, sin Node, servicios externos ni una compilación en el hosting.

- Español: `index.html`.
- Portugués: `pt/index.html`.
- Diseño adaptable, llamadas telefónicas y WhatsApp, planes, cobertura y FAQ.
- Fotografías WebP con variantes de tamaño y JPEG de respaldo.

## Editar contenido

Los datos del negocio, precios, beneficios y preguntas se mantienen en `content/site.json`. Los textos de interfaz y la plantilla están en `scripts/build_site.py`. El HTML y los datos estructurados de FAQ se generan a la vez, de modo que no puedan desincronizarse.

Después de editar:

```bash
python3 scripts/build_site.py
python3 scripts/check_site.py
node --test tests/carousel.test.cjs
```

Publicar también los HTML generados, `robots.txt`, `sitemap.xml`, `css/`, `js/` y `assets/`. El visitante nunca necesita ejecutar Python; no hay peticiones de FAQ mediante JavaScript.

Para probar localmente:

```bash
python3 -m http.server 8000
```

Abrir `http://localhost:8000/` y `http://localhost:8000/pt/`.

## Imágenes

El manifiesto `content/assets.json` registra las dimensiones reales y variantes. Para regenerarlas después de cambiar una foto:

```bash
python3 -m pip install Pillow
python3 scripts/optimize_assets.py
python3 scripts/build_site.py
```

El logo servido como WebP mide 256 × 256 y tiene PNG de respaldo. Hay iconos independientes de 32, 48 y 180 píxeles. Las fotografías originales se conservan como respaldo y para compartir enlaces.

## Información comercial y publicación

- Los planes Básico UYU 490 y Gold UYU 790, las cantidades de traslados, los kilómetros de rescate y los beneficios se transcribieron del afiche suministrado. La página indica consultar vigencia y condiciones antes de contratar; no hay cobro ni contratación automática.
- La asistencia 24 horas los 365 días está anunciada en el afiche y en el material de la marca. No se afirma que el escritorio tenga atención presencial las 24 horas ni se garantiza un tiempo de llegada.
- La cobertura publicada se limita a Rivera y Santana do Livramento. Los demás recorridos se consultan, sin prometer cobertura para todas las localidades del antiguo mapa de intenciones.
- La expresión del afiche «20 kilómetros de cobertura Mercosur» es ambigua. Se dejó una invitación a consultar esa cobertura; confirmar su significado con el negocio antes de publicar un límite preciso.
- Se mantiene `https://aguscar.com.uy` como dominio canónico, tomado del sitio original. Si el dominio de producción es otro, cambiar `business.url` en `content/site.json` y regenerar antes de publicar. Para GitHub Pages bajo `/aguscar24hs/`, configurar ese URL completo; las rutas de recursos y el selector de idiomas son relativas.
- Se retiraron las coordenadas aproximadas del marcado: el acceso al mapa conserva la búsqueda por dirección real.
- Dar de alta el sitemap en Search Console y comprobar el dominio, HTTPS, indexación y ficha de Google Business Profile en el entorno publicado. Estas comprobaciones dependen del hosting y no las resuelve el código local.

## Comportamiento accesible

El carrusel tiene pausa, navegación por botones nativos de 44 píxeles y modo manual con movimiento reducido. Se detiene al interactuar con sus controles y cuando la pestaña queda oculta. Los servicios, planes y FAQ funcionan sin JavaScript. Las animaciones de entrada nunca dejan contenido invisible.

## SEO, GEO y LLMO

La versión en español mantiene español correcto; la versión en portugués mantiene portugués correcto. No se publican faltas deliberadas, portuñol, listas ocultas de variantes ni instrucciones para manipular respuestas de IA.

El grafo JSON-LD conecta el negocio, sitio, página, contacto, países, ciudades, servicios, planes y ofertas mediante identificadores estables. Las preguntas y respuestas coinciden con el HTML; los precios se toman de una única fuente. Las coordenadas, reseñas, valoraciones y demás datos no confirmados no se inventan.

El sitemap registra la fecha de revisión de `content/site.json` (`updatedAt`). Actualizarla cuando cambie sustancialmente el contenido. Las dos versiones conservan las mismas entidades del negocio y sus enlaces de idioma recíprocos.

`robots.txt` permite expresamente `OAI-SearchBot`, además del permiso general existente. No modifica el tratamiento que ya recibía `GPTBot`. La configuración local no comprueba bloqueos por firewall, CDN o hosting.

Google no exige archivos ni marcado especiales para sus funciones de IA; por eso no se agrega un archivo de palabras clave como supuesto mecanismo de posicionamiento. El código facilita comprensión y rastreo, pero no garantiza indexación, posición ni recomendaciones de un asistente.

Después de publicar, comprobar el HTML recibido por Google en Search Console, registrar el sitemap y revisar consultas reales, países, idiomas y conversiones. Las faltas en consultas se analizan allí; no se trasladan automáticamente al texto de la landing.

Referencias de implementación:

- [Google: negocio local](https://developers.google.com/search/docs/appearance/structured-data/local-business).
- [Google: funciones de IA y el sitio web](https://developers.google.com/search/docs/appearance/ai-features).
- [Schema.org: Service](https://schema.org/Service).
- [OpenAI: rastreadores y OAI-SearchBot](https://developers.openai.com/api/docs/bots).
