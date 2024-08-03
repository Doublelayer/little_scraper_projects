from soup.souper import get_soup
import re

targest = [
    {
        "url": "https://www.petotal.de/mac-s-dog-mono-sensitive-400g-dose-hundenassfutter-38482?attribute[zoo_sorte]=zoo_6_x_400_gramm_kaninchen",
        "container": "div.product-base-price",
        "regex": r'\((\d+,\d+)\s*(€/kg)\)'
    },{
        "url": "https://www.zoo24.de/products/macs-dog-monoprotein-kaninchen-400-g?variant=47665621205317",
        "container": "unit-price",
        "regex": r'€(\d+,\d+)/(kg)'
    },{
        "url": "https://zoo.de/products/macs-dog-mono-kaninchen?variant=44407725097227",
        "container": ".product__price--unit",
        "regex": r'€([\d,]+)'
    }
]



def run():
    for target in targest:
        soup = get_soup(target.get("url"))
        container = soup.select_one(target.get("container"))
        match = re.search(target.get("regex"), container.text)
        #print("Container Text:", container.text)
        zahl = match.group(1)
        #einheit = match.group(2)
        print("Title:", soup.title.text.strip())
        print("€/kg:", zahl)
        print("")
        #print("Gefundene Einheit:", einheit)


if __name__ == '__main__':
    run()
