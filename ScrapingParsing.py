from requests import Session
import requests
from bs4 import BeautifulSoup
from time import sleep
from math import ceil
from random import uniform


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
BASE_URL = 'https://immobiliare.md/properties-2/'


def count_page():

    response = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "lxml")
    page_count = ceil(int(
        soup.find("div", class_="results-count").text.split()[5])/18)
    return page_count


def get_url():
    for count in range(1, count_page()+1):
        if count > 1:
            url = BASE_URL + 'page/' + str(count)
        else:
            url = BASE_URL
        s = Session()
        s.headers.update(HEADERS)
        response = s.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "lxml")

        data = soup.find_all(
            "div", class_="col-sm-6 col-md-6 col-lg-6 col-xl-6 col-ct-12 col-12")
        for i in data:
            url_page = i.find(
                "h2", class_="property-title").find("a").get("href")
            yield url_page


def get_info():
    for url_page in get_url():

        info = {}

        s = Session()

        response = s.get(url_page, headers=HEADERS)

        sleep(uniform(1, 1.5))

        soup = BeautifulSoup(response.text, "lxml")

        data = soup.find("div", id="apus-main-content")

        title = data.find("h1", class_="property-title").text
        location = data.find("div", class_="property-location").find("a").text

        additional = data.find_all("li", class_="d-flex align-items-center")
        for item in additional:

            key = item.find(
                "div", class_="text flex-shrink-0")
            if not key:
                key = item.find("div", class_="text")
            val = item.find("div", class_="value flex-grow-1")
            if not val:
                val = item.find("a", class_="type-property")
            if key and val:
                key = key.text.strip().replace(":", "")
                val = val.text.strip()
                info[key] = val

        rooms = info.get("Camere", "")
        shower_rooms = info.get("Camere de baie", "")
        area = info.get("Suprafața locuinței", "")
        type = info.get("Tipul", "")
        price = info.get("Prețul", "")
        status = info.get("Statut", "")
        living = info.get("Living", "")
        repair_type = info.get("Reparație", "")
        construction_type = info.get("Construcție", "")
        floor = info.get("Nivel", "")
        land = info.get("Teren (ari)", "")
        yield (title, location, rooms, shower_rooms, area, type, status, price, living, repair_type, construction_type, floor, land, url_page)
