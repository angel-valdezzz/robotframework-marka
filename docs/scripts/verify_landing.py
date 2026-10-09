"""Verify the editorial landing, meaningful motion and native documentation controls."""

import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import Page, expect, sync_playwright

ROOT = Path(__file__).resolve().parents[2]
MOUNT = "robotframework-marka"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def frame_geometry(page: Page, index: int) -> None:
    """A settled frame must surround the actual text with balanced side margins."""
    page.wait_for_function(
        "index => {const h=document.querySelector('[data-mk-hero]');"
        "return h.dataset.mkStage===String(index) && h.dataset.mkPhase==='hold';}",
        arg=index,
    )
    geometry = page.evaluate(
        """index => {
          const target=document.querySelectorAll('[data-mk-target]')[index];
          const frame=document.querySelector('.mk-marker').getBoundingClientRect();
          const r=target.getBoundingClientRect();
          const range=document.createRange(); range.selectNodeContents(target);
          const text=range.getBoundingClientRect();
          const spacing=parseFloat(getComputedStyle(target).letterSpacing)||0;
          const right=index===2?r.right:text.right-spacing;
          return {left:(index===2?r.left:text.left)-frame.left,
            right:frame.right-right, top:r.top-frame.top, bottom:frame.bottom-r.bottom};
        }""",
        index,
    )
    assert min(geometry.values()) >= 7, geometry
    assert abs(geometry["left"] - geometry["right"]) < 1, geometry
    assert abs(geometry["top"] - geometry["bottom"]) < 1, geometry


def check_documentation(page: Page, base: str) -> None:
    page.goto(base)
    page.locator(".mk-search-trigger").focus()
    page.keyboard.press("Enter")
    query = page.locator('[data-md-component="search-query"]')
    query.fill("Highlight Element")
    expect(page.locator(".md-search-result__link").first).to_be_visible(timeout=30000)
    page.keyboard.press("Escape")
    page.locator(".mk-primary").click()
    page.wait_for_url("**/guide/")
    expect(page.locator("[data-mk-hero]")).to_have_count(0)
    page.locator('label[for="__palette_1"]').click()
    expect(page.locator("body")).to_have_attribute("data-md-color-scheme", "slate")
    page.locator(".md-select button").click()
    page.locator('[data-doc-language="es"]').click()
    page.wait_for_url("**/es/guide/")
    expect(page.locator("body")).to_have_attribute("data-md-color-scheme", "slate")
    assert page.evaluate(
        """() => {
          const header=document.querySelector('.md-header'),tabs=document.querySelector('.md-tabs');
          const a=getComputedStyle(header),b=getComputedStyle(tabs);
          return a.animationName==='mk-header-flow' && b.animationName===a.animationName &&
            a.backgroundImage===b.backgroundImage && a.backgroundPosition===b.backgroundPosition &&
            Math.abs(header.getAnimations()[0].currentTime-tabs.getAnimations()[0].currentTime)<1;
        }"""
    )
    page.screenshot(path=str(ROOT / "build/landing-checks/docs-es-header.png"))
    # Return through Material's instant navigation, then leave again to check cleanup.
    page.locator(".md-logo").first.click()
    expect(page.locator("[data-mk-pause]")).to_be_visible()
    page.locator("[data-mk-pause]").click()
    expect(page.locator("[data-mk-hero]")).to_have_attribute("data-mk-paused", "true")
    page.locator(".mk-scroll").click()
    expect(page.locator("#mk-content")).to_be_focused()
    page.wait_for_function("scrollY>100")
    expect(page.locator(".mk-real-example img")).to_be_visible()
    assert page.locator(".mk-real-example img").evaluate("el=>el.complete && el.naturalWidth>0")
    page.screenshot(path=str(ROOT / "build/landing-checks/es-real-example.png"))
    page.locator('.mk-real-example a[href$="examples/"]').click()
    page.wait_for_url("**/es/examples/")
    expect(page.locator("[data-mk-hero]")).to_have_count(0)
    page.locator(".md-select button").click()
    page.locator('[data-doc-language="en"]').click()
    page.wait_for_url("**/examples/")
    assert "/es/" not in page.url
    expect(page.locator("body")).to_have_attribute("data-md-color-scheme", "slate")


def main() -> None:
    server_root = ROOT / "build/docs-server"
    server_root.mkdir(parents=True, exist_ok=True)
    mount = server_root / MOUNT
    if not mount.exists():
        mount.symlink_to(ROOT / "site", target_is_directory=True)
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietHandler, directory=str(server_root))
    )
    Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}/{MOUNT}/"
    output = ROOT / "build/landing-checks"
    output.mkdir(parents=True, exist_ok=True)
    measurements = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(args=["--no-sandbox"])
            for lang in ("en", "es"):
                for width, height in (
                    (1440, 1024),
                    (1366, 625),
                    (820, 1180),
                    (390, 844),
                    (320, 900),
                ):
                    page = browser.new_page(viewport={"width": width, "height": height})
                    errors = []
                    page.on("pageerror", lambda error, found=errors: found.append(str(error)))
                    page.goto(base + ("es/" if lang == "es" else ""))
                    expect(page.locator("[data-mk-pause]")).to_be_visible()
                    page.evaluate("document.fonts.ready")
                    assert page.locator("h1").count() == 1
                    assert page.locator("canvas,.er-preview,.review-controls,#speed").count() == 0
                    assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
                    assert page.locator(".md-select button").evaluate(
                        "el=>el.getBoundingClientRect().right<="
                        "document.querySelector('.mk-search-trigger').getBoundingClientRect().left"
                    )
                    assert page.locator(".md-header").evaluate(
                        "el=>getComputedStyle(el).backgroundColor==='rgba(0, 0, 0, 0)'"
                    )
                    assert page.locator(".md-logo img").first.evaluate(
                        "el=>getComputedStyle(el).backgroundColor==='rgba(0, 0, 0, 0)'"
                    )
                    if width >= 1100:
                        assert page.locator(".mk-primary,.mk-secondary,.mk-scroll").evaluate_all(
                            "els=>els.every(el=>{const b=el.getBoundingClientRect();"
                            "return b.top>=0 && b.bottom<=innerHeight;})"
                        )
                    # A full cycle must visit all real targets, including a visible hold.
                    for index in range(3):
                        frame_geometry(page, index)
                        page.screenshot(
                            path=str(output / f"{lang}-{width}-{height}-focus-{index}.png")
                        )
                    page.wait_for_function(
                        "document.querySelector('[data-mk-hero]').dataset.mkPhase==='travel'"
                    )
                    page.wait_for_function(
                        "Number(document.querySelector('.mk-marker').style.opacity)<.5"
                    )
                    before = page.locator(".mk-marker").get_attribute("style")
                    page.wait_for_timeout(180)
                    assert before != page.locator(".mk-marker").get_attribute("style")
                    page.locator("[data-mk-pause]").click()
                    expect(page.locator("[data-mk-pause]")).to_have_attribute(
                        "aria-pressed", "true"
                    )
                    page.wait_for_timeout(40)
                    frozen = page.locator(".mk-marker").get_attribute("style")
                    page.wait_for_timeout(180)
                    assert frozen == page.locator(".mk-marker").get_attribute("style")
                    # Hovering a target must not change the paused geometry.
                    page.locator('[data-mk-target="1"]').hover()
                    assert frozen == page.locator(".mk-marker").get_attribute("style")
                    styles = []
                    for scheme in ("default", "slate"):
                        page.evaluate("scheme=>document.body.dataset.mdColorScheme=scheme", scheme)
                        styles.append(
                            page.locator("#mk-headline").evaluate("el=>getComputedStyle(el).color")
                        )
                        assert page.locator(".mk-lead,.mk-secondary").evaluate_all(
                            "els=>els.every(el=>getComputedStyle(el).color==='rgb(245, 238, 229)')"
                        )
                        page.screenshot(path=str(output / f"{lang}-{width}-{height}-{scheme}.png"))
                    assert styles[0] == styles[1]
                    measurements.append({"lang": lang, "width": width, "height": height})
                    page.emulate_media(reduced_motion="reduce")
                    expect(page.locator("[data-mk-pause]")).to_be_disabled()
                    assert page.locator(".mk-moving-dot").evaluate(
                        "el=>getComputedStyle(el).animationName==='none'"
                    )
                    assert not errors, errors
                    page.close()
            page = browser.new_page(viewport={"width": 1440, "height": 1024})
            check_documentation(page, base)
            page.close()
            context = browser.new_context(java_script_enabled=False)
            page = context.new_page()
            page.goto(base)
            expect(page.locator("[data-mk-pause]")).to_be_hidden()
            expect(page.locator(".mk-marker")).to_be_hidden()
            expect(page.locator(".mk-primary")).to_be_visible()
            page.locator(".mk-secondary").click()
            assert page.url.endswith("#overview")
            browser.close()
    finally:
        server.shutdown()
    (output / "measurements.json").write_text(json.dumps(measurements, indent=2))
    print(
        "Landing passed: EN/ES, five viewports, real example, balanced frames, motion, themes, search and navigation."
    )


if __name__ == "__main__":
    main()
