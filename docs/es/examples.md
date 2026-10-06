# Ejemplos visuales

## Explicar un flujo con colores y pasos

Combina un borde azul más grueso, un fondo azul translúcido, puntos numerados y una nota verde. Los elementos conservan su interacción.

```robotframework
*** Settings ***
Library    SeleniumLibrary
Library    Marka

*** Test Cases ***
Explain Profile Changes
    # Browser is already open on the profile form.
    Highlight Element    id:email    color=\#2673D9    background=rgba(38,115,217,0.12)    width=5    group=profile
    Add Dot    id:email    text=1    color=\#2673D9    position=left    group=profile
    Add Dot    id:save    text=2    color=\#2673D9    position=left    group=profile
    Add Note    id:save    text=Save profile changes    color=\#567344    position=right    group=profile
    Click Element    id:save
    Capture Annotated Screenshot    ${OUTPUT DIR}/profile.png
```

## Capturar desde Python

Usa el mismo navegador abierto por tus pruebas. La captura devuelve una ruta absoluta y limpia las anotaciones por defecto.

```python
from marka import Annotator
from selenium.webdriver.common.by import By

marks = Annotator(driver)  # existing Selenium WebDriver
email = driver.find_element(By.ID, "email")
marks.add(email, color="#2673D9", background="rgba(38,115,217,0.12)", width=5)
marks.add(email, kind="dot", text="1", color="#2673D9", position="left")
path = marks.capture("output/profile.png")
```

## Captura anotada y procesamiento

Esta captura de la demo usa el mismo overlay.js que distribuye Marka: color y fondo coherentes, puntos separados y notas con color propio.

1. Localizar los elementos en la ventana/frame seleccionado.
2. Crear overlays independientes que siguen la posición del elemento y permiten clics.
3. Capturar el viewport como PNG y limpiar las anotaciones; usa clear=${False} para conservarlas.

La captura no recorta regiones ni une una página completa. Puedes agregar el PNG a Evidence Reporter como evidencia.

## Demo interactiva

El idioma sigue la documentación. Elige colores para resaltado, puntos y notas, y ajusta el grosor del borde. Limpia antes de probar otra combinación.

[Abrir demo ↗](assets/demo/index.html){ target="_blank" rel="noopener noreferrer" .md-button }

<iframe src="../assets/demo/index.html" title="Marka demo" style="width:100%;height:1100px;border:0;border-radius:12px" loading="lazy"></iframe>
