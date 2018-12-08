# coding=utf-8
from Avito.district import get_dict_district
from Avito.city import cities
from Avito.links import get_pages_by_url, get_links_goods
# from Avito.goods import get_goods
from Avito.category import get_dict_categories
# from Avito.threads import start_threads
# from Avito.subcategories import get_subcategories
# from Avito.metro import get_metro
from Avito.proxies import get_proxy_list
from . import detail
import csv
import toml


def main():
    detail.init_driver()

    # pages_links = get_pages_by_url('https://www.avito.ru/balashiha/kvartiry?p=1')
    goods_links = get_links_goods('https://www.avito.ru/balashiha/kvartiry?p=1')

    print(goods_links)

    with open('names.csv', 'w') as csvfile:
        for good_url in goods_links[2:]:
            data = detail.parse_url(good_url)
            toml.dump(data, csvfile)
    # print(links)

    detail.deinit_driver()


if __name__ == '__main__':
    main()
