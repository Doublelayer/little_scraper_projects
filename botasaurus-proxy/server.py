import time

from botasaurus.browser import browser, Driver
from botasaurus_driver import Wait, ElementWithSelectorNotFoundException
from flask import Flask, request


@browser(
    headless=True,
    block_images_and_css=True,
    wait_for_complete_page_load=False,
    close_on_crash=True,
    reuse_driver=False,
    raise_exception=False

)
def get_immoscout_cookies(driver: Driver, url):
    driver.google_get(url)

    time.sleep(1)
    cookies_ = driver.get_cookies_dict()
    now = time.time()
    while not cookies_.get("eveD"):
        time.sleep(0.5)
        cookies_ = driver.get_cookies_dict()
        if time.time() - now > Wait.VERY_LONG:
            raise ElementWithSelectorNotFoundException("cookie 'eveD' not found")

    return driver.get_cookies_dict()


app = Flask(__name__)


@app.route("/immoscout")
def get():
    return get_immoscout_cookies(
        "https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-mieten?enteredFrom=one_step_search/")


app.run(debug=False, host="0.0.0.0", port=5111)
