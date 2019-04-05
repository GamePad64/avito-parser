# -*- coding: utf-8 -*-
import json
import re
import urllib.parse as urlparse
from urllib.parse import urlencode

import scrapy
from bs4 import BeautifulSoup

from avito.site import phone

BASEURL = 'https://www.avito.ru'
POPULAR_UA = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.79',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.107',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 YaBrowser/19.3.0.2485 Yowser/2.5 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (iPad; CPU OS 12_1_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15',
]


class AvitoproductsSpider(scrapy.Spider):
    name = 'avitoproducts'
    allowed_domains = ['avito.ru']
    start_urls = [
        'https://www.avito.ru/balashiha/kvartiry?p=1',
        # 'https://www.avito.ru/balashiha/kvartiry?p=2',
        # 'https://www.avito.ru/balashiha/kvartiry?p=3',
        # 'https://www.avito.ru/balashiha/kvartiry?p=4',
        # 'https://www.avito.ru/balashiha/kvartiry?p=5',
        # 'https://www.avito.ru/balashiha/kvartiry?p=6',
        # 'https://www.avito.ru/balashiha/kvartiry?p=7',
        # 'https://www.avito.ru/balashiha/kvartiry?p=8',
        # 'https://www.avito.ru/balashiha/kvartiry?p=9',
        # 'https://www.avito.ru/balashiha/kvartiry?p=10',
    ]

    def _extract_id(self, offer):
        elem = offer.find(class_='title-info-metadata-item')
        m = re.match("№ (\d+)", elem.text.strip())
        return int(m.group(1))

    def _extract_phone_hash(self, response):
        m = re.findall(r"avito\.item\.phone\s\=\s\'(.+)\'", response.text)
        return m[0]

    def parse_phone(self, response):
        response_json = json.loads(response.text)
        image_b64: str = response_json['image64']
        image_b64 = image_b64.replace('data:image/png;base64,', '', 1)

        phone_str = phone.recognize_phone_image(image_b64)
        print(phone_str)
        yield {
            'product_id': response.meta['product_id'],
            'phone': phone_str
        }

    def parse_productpage(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        product = soup.find(attrs={'itemtype': 'http://schema.org/Product'})

        name = product.find(attrs={'itemprop': 'name'})
        images = [('https:' + elem.get('data-url')) for elem in product.find_all(class_='gallery-img-frame')]
        product_id = self._extract_id(product)
        address = product.find(attrs={'itemprop': 'streetAddress'})
        description = product.find(class_=re.compile('item-description-.+'), attrs={'itemprop': 'description'})

        offer = soup.find(attrs={'itemtype': 'http://schema.org/Offer'})
        price = offer.find(attrs={'itemprop': 'price'}).get('content')
        currency = offer.find(attrs={'itemprop': 'priceCurrency'}).get('content')

        data = {
            'url': response.url,
            'name': name.text,
            'images': ';'.join(images),
            'product_id': product_id,
            'address': address.text.strip(),
            'description': description.text.strip(),
            'price': price,
            'currency': currency,
        }

        item_params = {}
        item_params_html = soup.find_all('li', class_='item-params-list-item')
        for item_param in item_params_html:
            param_text_normalized = item_param.text.strip()
            param_value_sp = param_text_normalized.split(': ', 1)
            item_params[param_value_sp[0]] = param_value_sp[1]

        pkey = phone.phone_demixer(product_id, self._extract_phone_hash(response))

        yield scrapy.Request(
            url=phone.make_phone_url(product_id, pkey),
            headers={'Referer': response.url},
            callback=self.parse_phone,
            meta={'product_id': product_id}
        )

        data.update(item_params)

        yield data

    def _get_last_page(self, html):
        soup = BeautifulSoup(html, "lxml")
        try:
            pages = soup.find("div", class_="pagination-pages clearfix").find_all("a", class_="pagination-page")
        except AttributeError:
            return 1

        last_page_url = pages[-1].get("href")
        last_page_num = urlparse.parse_qs(urlparse.urlparse(last_page_url)[4])['p'][0]
        return int(last_page_num)

    def _make_paged_url(self, url: str, page: int):
        url_parts = list(urlparse.urlparse(url))

        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update({'p': page})
        url_parts[4] = urlencode(query)

        return urlparse.urlunparse(url_parts)

    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")

        offers = soup.find_all(attrs={'itemtype': 'http://schema.org/Product'})
        for offer in offers:
            url = BASEURL + offer.find(attrs={'itemprop': 'url'}).get('href')
            yield response.follow(url, self.parse_productpage)

        # for page in range(1, self._get_last_page(response.text) + 1):
        #     yield response.follow(self._make_paged_url(url, page), self.parse)
