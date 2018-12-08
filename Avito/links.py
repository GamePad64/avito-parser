# coding=utf-8
from bs4 import BeautifulSoup
from Avito.request import get_html
import urllib.parse as urlparse
from urllib.parse import urlencode


BASEURL = 'https://www.avito.ru'


def _get_last_page(html):
    soup = BeautifulSoup(html, "lxml")
    try:
        pages = soup.find("div", class_="pagination-pages clearfix").find_all("a", class_="pagination-page")
    except AttributeError:
        return 1

    last_page_url = pages[-1].get("href")
    last_page_num = urlparse.parse_qs(urlparse.urlparse(last_page_url)[4])['p'][0]
    return int(last_page_num)


def _make_paged_url(url: str, page: int):
    url_parts = list(urlparse.urlparse(url))

    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update({'p': page})
    url_parts[4] = urlencode(query)

    return urlparse.urlunparse(url_parts)


def get_pages_by_url(url: str):
    html = get_html(url)
    return [_make_paged_url(url, page) for page in range(1, _get_last_page(html) + 1)]


def get_links_goods(url: str):
    html = get_html(url)
    soup = BeautifulSoup(html, "lxml")

    urls = []

    offers = soup.find_all(attrs={'itemtype': 'http://schema.org/Product'})
    for offer in offers:
        url = BASEURL + offer.find(attrs={'itemprop': 'url'}).get('href')
        urls.append(url)

    return urls
