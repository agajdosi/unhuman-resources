import requests
from bs4 import BeautifulSoup
from replace import *
from adds import *

def downloadPage(url, headers):
    r = requests.get(url, headers=headers)

    return r.text

def getPage(url, originalAddress, newAddress, headers):
    page = downloadPage(url, headers)
    
    page = replaceBabis(page)
    page = replaceANO(page)
    page = addAdds(page)

    soup = BeautifulSoup(page, 'html.parser')
    for tag in soup.find_all():
        if tag.name == "a":
            if tag.has_attr("href"):
                tag["href"] = replaceLink(tag["href"], originalAddress, newAddress)


    #taeyyng
    page = str(soup)
    return page