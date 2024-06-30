from bs4 import BeautifulSoup
import requests


def get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        raise Exception(f"unable to get {url}")


def find_all_anchor_href(soup: BeautifulSoup) -> list:
    return [a.get('href') for a in soup.find_all("a")]


def find_class(soup: BeautifulSoup, _class: str):
    return soup.find(class_=_class)