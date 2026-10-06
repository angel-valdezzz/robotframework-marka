import os
from pathlib import Path

import pytest
from robot import run
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from marka import Annotator


@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if os.getenv("MARKA_CHROME_BINARY"):
        options.binary_location = os.environ["MARKA_CHROME_BINARY"]
    service = (
        Service(os.environ["MARKA_CHROMEDRIVER"]) if os.getenv("MARKA_CHROMEDRIVER") else Service()
    )
    browser = webdriver.Chrome(service=service, options=options)
    browser.set_window_size(1100, 800)
    yield browser
    browser.quit()


@pytest.fixture
def page(driver):
    driver.get((Path(__file__).parents[1] / "examples/page.html").resolve().as_uri())
    return driver


def test_persistence_clicks_groups_and_original_styles(page, tmp_path):
    marks = Annotator(page)
    email = page.find_element(By.ID, "email")
    before = email.get_attribute("style")
    first = marks.add(
        email, background="rgba(240,100,69,0.2)", text="<b>Updated</b>", group="profile"
    )
    marks.add(page.find_element(By.ID, "save"), kind="dot", text="2", group="action")
    page.find_element(By.ID, "save").click()
    assert page.find_element(By.ID, "result").text == "Saved"
    assert email.get_attribute("style") == before
    assert len(page.find_elements(By.CSS_SELECTOR, "[data-marka-id]")) == 2
    assert page.find_element(By.CSS_SELECTOR, "[data-marka-id] span").text == "<b>Updated</b>"
    assert marks.clear(annotation_id=first) == 1
    assert marks.clear(group="missing") == 0
    filename = marks.capture(tmp_path / "screenshot.png")
    assert Path(filename).read_bytes().startswith(b"\x89PNG")
    assert not page.find_elements(By.CSS_SELECTOR, "[data-marka-root]")


def test_tracks_scroll_resize_and_detached_elements(page):
    marks = Annotator(page)
    element = page.find_element(By.ID, "lower")
    identifier = marks.add(element)
    page.execute_script("arguments[0].scrollIntoView()", element)
    page.execute_async_script(
        "const done=arguments[arguments.length-1];requestAnimationFrame(()=>requestAnimationFrame(done));"
    )
    difference = page.execute_script(
        'const a=arguments[0].getBoundingClientRect(),b=document.querySelector("[data-marka-id]").getBoundingClientRect();return Math.abs(a.top-b.top);',
        element,
    )
    assert difference < 1
    page.execute_script("arguments[0].remove()", element)
    page.execute_async_script(
        "const done=arguments[arguments.length-1];requestAnimationFrame(()=>requestAnimationFrame(done));"
    )
    assert (
        page.find_element(By.CSS_SELECTOR, f'[data-marka-id="{identifier}"]').value_of_css_property(
            "display"
        )
        == "none"
    )
    assert marks.clear() == 1


def test_notes_dots_and_current_iframe_scope(page):
    marks = Annotator(page)
    save = page.find_element(By.ID, "save")
    marks.add(save, kind="note", text="Explanation", position="right")
    marks.add(save, kind="label", text="Label", position="bottom")
    page.execute_script(
        "const frame=document.createElement('iframe');frame.srcdoc='<button id=inner>Inside</button>';document.body.append(frame);"
    )
    page.switch_to.frame(page.find_element(By.TAG_NAME, "iframe"))
    marks.add(page.find_element(By.ID, "inner"), kind="dot", text="1")
    assert marks.clear() == 1
    page.switch_to.default_content()
    assert len(page.find_elements(By.CSS_SELECTOR, "[data-marka-id]")) == 2
    assert marks.clear() == 2


@pytest.mark.parametrize(
    "kwargs",
    [
        {"size": -1},
        {"width": "nan"},
        {"style": "unknown"},
        {"position": "unknown"},
        {"kind": "unknown"},
    ],
)
def test_invalid_options(page, kwargs):
    with pytest.raises(ValueError):
        Annotator(page).add(page.find_element(By.ID, "email"), **kwargs)


def test_invalid_color_does_not_leave_overlay(page):
    with pytest.raises(Exception, match="Invalid CSS color"):
        Annotator(page).add(page.find_element(By.ID, "email"), color="not-a-color")
    assert not page.find_elements(By.CSS_SELECTOR, "[data-marka-root]")


def test_capture_failure_still_cleans(page, tmp_path, monkeypatch):
    marks = Annotator(page)
    marks.add(page.find_element(By.ID, "email"))
    monkeypatch.setattr(page, "save_screenshot", lambda _: False)
    with pytest.raises(OSError):
        marks.capture(tmp_path / "failure.png")
    assert not page.find_elements(By.CSS_SELECTOR, "[data-marka-root]")


def test_real_robot_example(tmp_path):
    result = run(
        str(Path(__file__).parents[1] / "examples/quickstart.robot"), outputdir=str(tmp_path)
    )
    assert result == 0
    assert (tmp_path / "annotated.png").read_bytes().startswith(b"\x89PNG")
