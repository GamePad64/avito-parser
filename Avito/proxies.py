import requests
from bs4 import BeautifulSoup

proxy_list = []


def _renew_proxy_list():
    html = requests.get('https://www.sslproxies.org/')
    soup = BeautifulSoup(html.text, "lxml")
    elements = soup.find("tbody").find_all("tr")
    for element in elements:
        ip = element.find_all("td")[0].text
        port = element.find_all("td")[1].text
        proxy = f'https://{ip}:{port}'
        proxy_list.append(proxy)
    return proxy_list


def get_proxy_list():
    """ Функция возвращает список https прокси. """
    if not proxy_list:
        _renew_proxy_list()

    return proxy_list


def get_working_proxy():
    return proxy_list[0]


def remove_proxy(url):
    proxy_list.remove(url)
