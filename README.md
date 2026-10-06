<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/angel-valdezzz/robotframework-marka/main/docs/assets/wordmark-dark.svg">
  <img src="https://raw.githubusercontent.com/angel-valdezzz/robotframework-marka/main/docs/assets/wordmark-light.svg" alt="Marka" width="360">
</picture>

# Marka

Persistent browser highlights, numbered dots, labels and notes for explanatory screenshots.

[![CI](https://github.com/angel-valdezzz/robotframework-marka/actions/workflows/ci.yml/badge.svg)](https://github.com/angel-valdezzz/robotframework-marka/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/robotframework-marka)](https://pypi.org/project/robotframework-marka/)

[User guide](https://angel-valdezzz.github.io/robotframework-marka/) · [Guía en español](https://angel-valdezzz.github.io/robotframework-marka/es/) · [Keyword reference ↗](https://angel-valdezzz.github.io/robotframework-marka/keywords/index.html) · [PyPI](https://pypi.org/project/robotframework-marka/) · [Live examples](https://angel-valdezzz.github.io/robotframework-marka/examples/)


![Python](https://img.shields.io/pypi/pyversions/robotframework-marka?logo=python)
![Robot Framework](https://img.shields.io/badge/Robot_Framework-compatible-00A6A6?logo=robotframework)
[![License](https://img.shields.io/github/license/angel-valdezzz/robotframework-marka)](LICENSE)

## Install

```bash
pip install "robotframework-marka[robot]"
```

Python users can install `robotframework-marka` without the Robot adapter dependencies.

## Annotate your existing browser

```robotframework
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

```python
from marka import Annotator
from selenium.webdriver.common.by import By

# driver is your existing Selenium WebDriver.
marks = Annotator(driver)
email = driver.find_element(By.ID, "email")
marks.add(email, color="coral", background="rgba(240,100,69,0.12)")
marks.add(email, kind="dot", text="1", color="#FFBF47", position="left")
marks.capture("output/changes.png")  # clears marks by default
```


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md), [CHANGELOG.md](CHANGELOG.md), and the [development guide](https://angel-valdezzz.github.io/robotframework-marka/development/).
