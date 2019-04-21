FROM ubuntu:18.04

RUN apt-get update &&\
    apt-get install -y python3-dev python3-pip python3-venv tesseract-ocr tesseract-ocr-eng &&\
    pip3 install poetry

WORKDIR /srv

COPY pyproject.toml poetry.lock /srv/
RUN poetry install

COPY . /srv/

CMD poetry run scrapy crawl avitoproducts
