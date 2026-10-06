"""Headless browser options for the executable local example."""

import os

from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service

CHROME_OPTIONS = ChromeOptions()
CHROME_OPTIONS.add_argument("--headless=new")
CHROME_OPTIONS.add_argument("--no-sandbox")
CHROME_OPTIONS.add_argument("--disable-dev-shm-usage")
if os.getenv("MARKA_CHROME_BINARY"):
    CHROME_OPTIONS.binary_location = os.environ["MARKA_CHROME_BINARY"]
CHROME_SERVICE = (
    Service(os.environ["MARKA_CHROMEDRIVER"]) if os.getenv("MARKA_CHROMEDRIVER") else Service()
)
