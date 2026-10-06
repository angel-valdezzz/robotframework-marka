# Guía de usuario

## Instalación

```bash
pip install "robotframework-marka[robot]"
```

Para Python puedes instalar `robotframework-marka` sin las dependencias del adaptador de Robot.

## Anota sobre tu navegador actual

```robotframework hl_lines="7-10"
*** Settings ***
Library    SeleniumLibrary
Library    Marka

*** Test Cases ***
Show Changes
    Highlight Element    id:email    color=coral    background=rgba(240,100,69,0.12)    group=profile
    Add Dot    id:email    text=1    position=left    group=profile
    Add Note    id:save    text=Save changes    position=right    group=profile
    Capture Annotated Screenshot    ${OUTPUT DIR}/changes.png
```

```python hl_lines="7-9"
from marka import Annotator
from selenium.webdriver.common.by import By

# driver is your existing Selenium WebDriver.
marks = Annotator(driver)
email = driver.find_element(By.ID, "email")
marks.add(email, color="coral", background="rgba(240,100,69,0.12)")
marks.add(email, kind="dot", text="1", color="#FFBF47", position="left")
marks.capture("output/changes.png")  # clears marks by default
```

## Comportamiento y límites

Abre primero el navegador con SeleniumLibrary; Marka no crea otra sesión.
Si tiene un alias, usa `Library    Marka    selenium_library=Web`.
Las marcas son capas independientes que permiten clics: los estilos y el diseño originales no cambian.
Siguen el scroll, el redimensionamiento y los movimientos. Al eliminar un elemento su marca se oculta.
`Highlight Elements` marca todas las coincidencias; las keywords singulares usan la primera.
Los dots admiten texto/número, color CSS, tamaño y posición. Las notas tienen indicador; las etiquetas son texto sencillo.
Los bordes admiten solid, dashed, dotted y double; el fondo admite colores CSS, incluidos RGBA.
Usa los IDs devueltos con `Remove Annotation`, o `Clear Annotations    group=profile`.

**Ventana/iframe:** selecciona la ventana o iframe antes de anotar. La limpieza afecta solo al documento seleccionado. Selecciona cada iframe anotado para limpiarlo. Recargar o navegar descarta sus marcas. Robot limpia lo que puede en el iframe actual de cada driver al terminar la prueba; limpia explícitamente los otros frames.

`Capture Annotated Screenshot` captura el viewport, devuelve una ruta PNG absoluta y limpia por defecto. Usa `clear=${False}` para conservar las marcas. Guarda el archivo sin duplicar imágenes en el log de Robot; puedes seguir usando la captura de SeleniumLibrary.
Para capturas de iframes, usa la captura normal de página después de anotar.
Acorta las notas largas para que quepan. Capturas de página completa, flechas y recortes quedan para una entrega posterior.
