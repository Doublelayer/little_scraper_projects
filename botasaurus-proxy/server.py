import time

from botasaurus.browser import browser, Driver
from botasaurus_driver import Wait, ElementWithSelectorNotFoundException
from flask import Flask, request


@browser(
    headless=True,
    block_images=False,
    reuse_driver=True
)
def scrape_html(driver: Driver, url):
    driver.google_get(url)

    time.sleep(1)
    # cookies_ = driver.get_cookies_dict()
    # now = time.time()
    # while not cookies_.get("eveD"):
    #     time.sleep(0.5)
    #     cookies_ = driver.get_cookies_dict()
    #     if time.time() - now > Wait.VERY_LONG:
    #         raise ElementWithSelectorNotFoundException("cookie 'eveD' not found")

    return driver.page_html


app = Flask(__name__)


@app.route("/")
def get():
    return scrape_html(request.args.get('url'))


app.run(debug=False, port=5000)
