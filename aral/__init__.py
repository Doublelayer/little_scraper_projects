import json

import requests
from dotenv import load_dotenv

from pushover import po_params
from pushover.invoker import Pushover

load_dotenv()


def send_msg(payload):
    po = Pushover("")
    po.user("")

    msg = po.msg(payload.get("last_price_update"))

    msg.set_data(po_params.TITLE, payload.get("title"))
    # msg.set_attachment(("image.jpg", open("DSC07245.JPG", "rb"), "image/jpeg"))

    po.send(msg)


def get_sprit_price():
    url = "https://api.tankstelle.aral.de/api/v3/stations/28133300/prices"
    payload = {}
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'de-DE,de;q=0.7',
        'cache-control': 'max-age=0'
    }
    response = requests.request("GET", url, headers=headers, data=payload, allow_redirects=False)
    json_ = json.loads(response.text)["data"]

    return {
        "title": "Aktueller Preis Ultimate Diesel: " + json_.get("prices").get("F00426"),
        "last_price_update": json_.get("last_price_update")
    }


if __name__ == '__main__':
    sprit_price = get_sprit_price()
    send_msg(sprit_price)
