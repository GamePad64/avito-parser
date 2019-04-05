import base64
import io

from PIL import Image
from pytesseract import image_to_string
import re
import phonenumbers


def recognize_phone_image(image_b64: str):
    image_in_bytes = base64.b64decode(image_b64)
    img = Image.open(io.BytesIO(image_in_bytes))

    recognized = image_to_string(img, lang='eng')

    number = phonenumbers.parse(recognized, region='RU')
    return phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)


def phone_demixer(product_id: int, phone_hash: str):
    pre = re.findall(r'([\da-f]+)', phone_hash)

    if (product_id % 2) == 0:
        pre.reverse()
    mixed = ''.join(pre)
    s = len(mixed)
    i = ''

    for k in range(0, s):
        if (k % 3) == 0:
            i += mixed[k]
    return i


def make_phone_url(product_id: int, pkey: str):
    return f'https://www.avito.ru/items/phone/{product_id}?pkey={pkey}'
