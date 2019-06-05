import requests
from bs4 import BeautifulSoup
from replace import *

def downloadPage(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)

    return r.text

def getPage(url, originalAddress, newAddress):
    page = downloadPage(url)

    soup = BeautifulSoup(page, 'html.parser')
    for tag in soup.find_all():
        if tag.name == "a":
            tag["href"] = replaceLink(tag["href"], originalAddress, newAddress)

    page = str(soup)
    page = replaceBabis(page)
    page = replaceANO(page)

    return page