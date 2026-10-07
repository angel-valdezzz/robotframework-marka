---
template: home.html
title: Marka
description: Add highlights, numbered dots and notes to your Selenium browser. Give screenshots the context your team needs.
---

<div id="overview"></div>

## Make the evidence easy to follow

<div class="grid cards" markdown>

- **Highlight**

    Point to the field or component that matters.

- **Explain**

    Guide the reader with numbered dots and short notes.

- **Capture**

    Save the annotated viewport and clear the marks by default.

</div>

Use it from Python or Robot Framework with the same behavior. MIT licensed, with source and executable examples on GitHub.

## What it does

- Keep highlights visible until explicitly cleared.
- Explain a sequence with numbered dots and notes.
- Capture a PNG and clean marks automatically, including on capture failure.
- Work with your existing SeleniumLibrary browser.

## See the annotation flow

```mermaid
flowchart TD
    B[Selenium browser] --> H[Highlight Element]
    H --> N[Add Dot / Add Note]
    N --> C[Capture Annotated Screenshot]
    C --> P[PNG]
    C --> X[Clear annotations]
```

[Explore real screenshots](examples.md){ data-preview }
