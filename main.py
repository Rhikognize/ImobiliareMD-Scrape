from requests import Session
import requests
from bs4 import BeautifulSoup
from time import sleep
from math import ceil
from random import uniform

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


url = "https://immobiliare.md/place/casa-cu-3-niveluri-r-nul-grigoriopol-loc-taslic/"
s = Session()
s.headers.update(HEADERS)
response = s.get(url, headers=HEADERS)
soup = BeautifulSoup(response.text, "lxml")
data = soup.find_all(
    "li", class_="d-flex align-items-center")

print(data)
