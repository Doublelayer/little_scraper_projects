from dotenv import load_dotenv

from db import file_provider
from pushover import po_params
from pushover.invoker import Pushover
from soup import souper

load_dotenv()

db_name = "schenefelder-bote.txt"


def get_unknown_hrefs(found_hrefs: list):
    return list(set(found_hrefs) - set(file_provider.get_file_content_as_list(db_name)))


def send_notification(url_):
    po = Pushover("")
    po.user("")

    msg = po.msg(f"Der neue Schenefelder Bote: {url_}")
    msg.set_data(po_params.TITLE, url_.split("/")[:-1])

    po.send(msg)


if __name__ == '__main__':
    soup = souper.get_soup("https://schenefelder-bote.de/archiv/")
    hrefs = souper.find_all_anchor_href(soup)
    filtered_href = list(filter(lambda href: href.endswith("pdf"), hrefs))
    unknown_hrefs = get_unknown_hrefs(filtered_href)
    if len(unknown_hrefs) > 0:
        print(f"found new newspaper")
        send_notification(unknown_hrefs[-1])
        file_provider.write_hrefs(unknown_hrefs, db_name)
