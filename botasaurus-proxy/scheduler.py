import os
from pathlib import Path
from botasaurus.task import task
import schedule
import time
import pymongo
from botasaurus import bt

from botasaurus.browser import browser, Driver
from botasaurus_driver import Wait, ElementWithSelectorNotFoundException
import shutil


def move_file_to_import(_path):
    (_dir, _filename) = os.path.split(_path)
    _destination_dir = _dir.replace("download", "import")
    dst_path = Path(_destination_dir, _filename)
    Path(_destination_dir).mkdir(parents=True, exist_ok=True)
    Path.rmdir(Path(_dir))


def write_and_move_output(data, result):
    _download_dir_path = Path("./download")
    _download_dir_path.mkdir(parents=True, exist_ok=True)
    _import_dir_path = Path("./import")
    _import_dir_path.mkdir(parents=True, exist_ok=True)

    _filename = f"{data['userId']}__{data['providerId']}__{data['id']}.html"
    _full_path = Path(_download_dir_path, _filename)

    bt.write_file(result, _full_path)
    shutil.move(_full_path, f"./import/{_filename}")


@browser(
    headless=False,
    block_images=False,
    reuse_driver=True,
    close_on_crash=True,
    output=write_and_move_output
)
def scrape_html(driver: Driver, data):
    driver.google_get(data["url"])

    time.sleep(1)
    cookies_ = driver.get_cookies_dict()
    now = time.time()
    while not cookies_.get("eveD"):
        time.sleep(0.5)
        cookies_ = driver.get_cookies_dict()
        if time.time() - now > Wait.VERY_LONG:
            raise ElementWithSelectorNotFoundException("cookie 'eveD' not found")

    return driver.page_html


def run():
    client = pymongo.MongoClient(
        "mongodb+srv://fredydb:XXodLb0MeZvgXVXS@fredycluster.lgslkfa.mongodb.net/?retryWrites=true&w=majority/")

    jobs = client.fredy.jobs
    for job in jobs.find():
        print(job["userId"])
        for provider in job["provider"]:
            print(f"now handling {provider['id']} with {provider['url']}")
            scrape_html({
                **provider,
                **job
            })
    scrape_html.close()
    client.close()


schedule.every(10).seconds.do(run)


while True:
    schedule.run_pending()
    time.sleep(10)
