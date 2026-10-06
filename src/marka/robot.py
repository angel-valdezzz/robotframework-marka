"""Use Marka with the browser already opened by SeleniumLibrary."""

from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

from . import Annotator, __version__


class Marka:
    """Highlight elements and annotate screenshots using SeleniumLibrary.

    Import ``Library    Marka`` alongside SeleniumLibrary. Marks persist until
    explicitly removed and never block pointer interactions. Annotations belong
    to the currently selected browser window/frame. Select each annotated frame
    before cleaning it; navigating/reloading removes marks in that document.

    Example:
    | Highlight Element | id:email | label=Updated |
    | Add Dot | id:save | text=1 |
    | Capture Page Screenshot | changes.png |
    | Clear Annotations |
    """

    ROBOT_LIBRARY_SCOPE = "TEST"
    ROBOT_AUTO_KEYWORDS = False
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, selenium_library="SeleniumLibrary"):
        """Use the named SeleniumLibrary instance, including a custom alias."""
        self.selenium_library = selenium_library
        self._engines = {}
        self.ROBOT_LIBRARY_LISTENER = self
        self.ROBOT_LISTENER_API_VERSION = 3

    def _engine(self):
        library = BuiltIn().get_library_instance(self.selenium_library)
        driver = library.driver
        key = id(driver)
        if key not in self._engines:
            self._engines[key] = Annotator(driver)
        return library, self._engines[key]

    @keyword
    def highlight_element(
        self,
        locator,
        color="#F06445",
        background="transparent",
        width=3,
        style="solid",
        radius=6,
        label="",
        group="default",
    ):
        """Add a persistent border and optional translucent background/label.

        Supports SeleniumLibrary locators and WebElement objects. Width and radius
        are in CSS pixels. Returns an annotation ID for selective removal.
        """
        library, engine = self._engine()
        return engine.add(
            library.find_element(locator),
            color=color,
            background=background,
            width=width,
            style=style,
            radius=radius,
            text=label,
            group=group,
        )

    @keyword
    def highlight_elements(self, locator, color="#F06445", group="default"):
        """Highlight every matching element; fail when no element matches."""
        library, engine = self._engine()
        elements = library.find_elements(locator)
        if not elements:
            raise ValueError(f"No elements match {locator}")
        return [engine.add(element, color=color, group=group) for element in elements]

    @keyword
    def add_dot(self, locator, text="", color="#FFBF47", size=28, position="top", group="default"):
        """Add a colored dot, optionally numbered; return its annotation ID."""
        library, engine = self._engine()
        return engine.add(
            library.find_element(locator),
            kind="dot",
            text=text,
            color=color,
            size=size,
            position=position,
            group=group,
        )

    @keyword
    def add_label(self, locator, text, color="#FFBF47", position="top", group="default"):
        """Add a short text label anchored to an element."""
        library, engine = self._engine()
        return engine.add(
            library.find_element(locator),
            kind="label",
            text=text,
            color=color,
            position=position,
            group=group,
        )

    @keyword
    def add_note(self, locator, text, color="#FFBF47", position="top", group="default"):
        """Add an explanatory note with an indicator anchored to an element."""
        library, engine = self._engine()
        return engine.add(
            library.find_element(locator),
            kind="note",
            text=text,
            color=color,
            position=position,
            group=group,
        )

    @keyword
    def remove_annotation(self, annotation_id):
        """Remove one annotation ID in the current window/frame."""
        return self._engine()[1].clear(annotation_id=annotation_id)

    @keyword
    def clear_annotations(self, group=None):
        """Remove all marks, or only those in a named group, in the current frame."""
        return self._engine()[1].clear(group=group)

    @keyword
    def capture_annotated_screenshot(self, path, clear=True, group=None):
        """Capture the current viewport and clear marks by default, even on failure.

        Returns the absolute PNG path. Unlike SeleniumLibrary's capture keyword,
        this writes the file without inserting a duplicate image into Robot's log.
        """
        if isinstance(clear, str):
            clear = clear.lower() not in {"false", "no", "0", "none", ""}
        return self._engine()[1].capture(path, clear=clear, group=group)

    def end_test(self, data, result):
        """Best-effort cleanup in each driver's selected frame at test end."""
        for engine in self._engines.values():
            try:
                engine.clear()
            except Exception:
                # Browser may already have been closed by the test teardown.
                pass
        self._engines.clear()
