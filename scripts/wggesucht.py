import requests
import os

from bs4 import BeautifulSoup

def run():
    # Site name
    url  = 'https://www.wg-gesucht.de/'
    response =  requests.get(url)

    htmlPath = 'html/wggesucht/'

    text = response.text

    # TODO submit initial form and be redirected
    print()
    payload = {

    }

    # TODO filename could be the combination of date, state or city name
    fileName = 'testing.html'
    filePath = htmlPath + fileName

    # Check if the directory is already created or not
    os.makedirs(os.path.dirname(filePath), exist_ok=True)

    with open(filePath, "w") as f:
        f.write(text)
