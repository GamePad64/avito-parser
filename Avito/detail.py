import base64
import io

from PIL import Image
from bs4 import BeautifulSoup
from pytesseract import image_to_string
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from urllib3.exceptions import ProtocolError, MaxRetryError

from Avito.request import get_html
from . import proxies


driver = None


def init_driver():
    global driver
    driver = _make_selenium_driver()


def deinit_driver():
    global driver
    if driver:
        driver.quit()


def _make_selenium_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument(f'--proxy-server={proxies.get_working_proxy()}')
    return webdriver.Chrome(chrome_options=chrome_options)


def get_phone_number(url):
    try:
        driver.get(url)

        _button_click(driver)
        b64_image = _get_coded_image(driver)

        image_in_bytes = base64.b64decode(b64_image)

        # return _recognize_phone_image(image_in_bytes)

    except (ProtocolError, MaxRetryError):
        print('Error conecting:', url)
        return None


def _button_click(driver):
    """ Метод кликает на кнопку для получения номера телефона. """
    while True:
        try:
            button = driver.find_element_by_xpath(
                '//a[@class="button item-phone-button js-item-phone-button button-origin button-origin-blue button-origin_full-width button-origin_large-extra item-phone-button_hide-phone item-phone-button_card js-item-phone-button_card"]')
            button.click()
            break
        except NoSuchElementException:
            continue


def _get_coded_image(driver):
    while True:
        try:
            coded_image = driver.find_element_by_xpath(
                '//div[@class="item-phone-big-number js-item-phone-big-number"]/img').get_attribute('src').split(',')[1]
            return coded_image
        except NoSuchElementException:
            continue


# ---------------------
def parse_url(url):
    h = get_html(url)
    soup = BeautifulSoup(h, 'lxml')

    offer = soup.find(attrs={'itemtype': 'http://schema.org/Product'})

    name = offer.find(attrs={'itemprop': 'name'})
    images = [('https:' + elem.get('data-url')) for elem in offer.find_all(class_='gallery-img-frame')]
    data = {
        'name': name.text,
        'images': images,
        # 'phone': get_phone_number(url)
    }

    item_params = {}
    item_params_html = soup.find_all('li', class_='item-params-list-item')
    for item_param in item_params_html:
        param_text_normalized = item_param.text.strip()
        param_value_sp = param_text_normalized.split(': ', 1)
        item_params[param_value_sp[0]] = param_value_sp[1]

    data['params'] = item_params

    return data
