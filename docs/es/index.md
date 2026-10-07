---
template: home.html
title: Marka
description: Agrega resaltados, puntos numerados y notas a tu navegador Selenium. Dale a las capturas el contexto que tu equipo necesita.
---

<div id="overview"></div>

## Haz que la evidencia sea fácil de seguir

<div class="grid cards" markdown>

- **Resalta**

    Señala el campo o componente que importa.

- **Explica**

    Guía al lector con puntos numerados y notas breves.

- **Captura**

    Guarda el viewport anotado y limpia las marcas por defecto.

</div>

Úsala desde Python o Robot Framework con el mismo comportamiento. Licencia MIT, código y ejemplos ejecutables en GitHub.

## Qué hace

- Mantiene el resaltado hasta que lo retires.
- Explica una secuencia con puntos numerados y notas.
- Captura un PNG y limpia las marcas automáticamente, incluso si falla la captura.
- Usa el navegador que ya abriste con SeleniumLibrary.

## Conoce el flujo de anotación

```mermaid
flowchart TD
    B[Selenium browser] --> H[Highlight Element]
    H --> N[Add Dot / Add Note]
    N --> C[Capture Annotated Screenshot]
    C --> P[PNG]
    C --> X[Clear annotations]
```

[Explora capturas reales](examples.md){ data-preview }
