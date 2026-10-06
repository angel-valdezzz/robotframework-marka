"""Browser annotations using the existing Selenium driver."""

from __future__ import annotations

import math
import uuid
from importlib.resources import files
from pathlib import Path

SCRIPT = files("marka").joinpath("overlay.js").read_text(encoding="utf-8")


class Annotator:
    """Overlay highlights and annotations without changing original element styles.

    Operations target Selenium's currently selected window/frame. Navigation drops
    that document's annotations. IDs and groups allow selective cleanup.
    """

    def __init__(self, driver):
        self.driver = driver
        self.owner = uuid.uuid4().hex

    def add(
        self,
        element,
        *,
        kind="highlight",
        color="#F06445",
        background="transparent",
        width=3,
        style="solid",
        radius=6,
        text="",
        text_color="#253044",
        size=28,
        position="top",
        group="default",
    ):
        if kind not in {"highlight", "dot", "label", "note"}:
            raise ValueError("Unknown annotation kind")
        if position not in {"top", "bottom", "left", "right", "center"}:
            raise ValueError("position must be top, bottom, left, right or center")
        if style not in {"solid", "dashed", "dotted", "double"}:
            raise ValueError("Unsupported border style")
        values = {"width": float(width), "radius": float(radius), "size": float(size)}
        if any(not math.isfinite(v) or v < 0 or v > 256 for v in values.values()):
            raise ValueError("Annotation dimensions must be finite and between 0 and 256")
        if values["size"] < 12:
            raise ValueError("Dot size must be at least 12 pixels")
        options = dict(
            kind=kind,
            color=str(color),
            background=str(background),
            style=style,
            text=str(text),
            text_color=str(text_color),
            position=position,
            group=str(group),
            id=uuid.uuid4().hex,
            **values,
        )
        return self.driver.execute_script(SCRIPT, self.owner, "add", element, options)

    def clear(self, *, annotation_id=None, group=None):
        """Remove selected annotations in the current window/frame."""
        return self.driver.execute_script(
            SCRIPT, self.owner, "clear", None, {"id": annotation_id, "group": group}
        )

    def capture(self, path, *, clear=True, group=None):
        """Capture the viewport, optionally clearing marks even when capture fails."""
        target = Path(path).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            if not self.driver.save_screenshot(str(target)):
                raise OSError("Selenium could not save the screenshot")
            return str(target)
        finally:
            if clear:
                self.clear(group=group)
