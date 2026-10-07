---
tags:
  - Usage
---

# User guide

## Install

```bash
pip install "robotframework-marka[robot]"
```

Python users can install `robotframework-marka` without the Robot adapter dependencies.

## Annotate your existing browser

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

## Behavior and limits

Open the browser with SeleniumLibrary first; Marka does not open another session.
If SeleniumLibrary has an alias, use `Library    Marka    selenium_library=Web`.
Marks are separate pointer-transparent overlays: original styles and layout are preserved.
They follow scrolling, resizing and moving elements. Removed elements hide their marks.
`Highlight Elements` marks every match; singular keywords use the first match.
Dots accept text/number, CSS color, size and position. Notes have a pointer; labels are plain text.
Border style supports solid, dashed, dotted and double; backgrounds accept CSS colors including RGBA.
Use returned IDs with `Remove Annotation`, or `Clear Annotations    group=profile`.

**Window/frame scope:** select the desired window or iframe before annotating. Cleanup affects that current document only. Select each annotated frame to clean it. Reload/navigation discards its marks. Robot performs best-effort cleanup in each driver's current frame at test end; use explicit cleanup for other frames.

`Capture Annotated Screenshot` captures the viewport, returns an absolute PNG path and clears by default. Set `clear=${False}` to retain marks. It writes a file without adding a duplicate image to the Robot log; SeleniumLibrary's capture keyword remains usable.
Screenshots inside iframes should use the normal page capture after the marks are added.
Very long notes should be shortened to fit the viewport. Full-page stitching, arrows and region cropping are future features.
