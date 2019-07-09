import requests
from bs4 import BeautifulSoup
from replace import *
from adds import *

def handleA(tag, originalAddress, newAddress):
    if tag.has_attr("href"):
        tag["href"] = replaceLink(tag["href"], originalAddress, newAddress)
    return tag

def handleBase(tag, originalAddress, newAddress):
    if tag.has_attr("href"):
        tag["href"] = replaceLink(tag["href"], originalAddress, newAddress)
    return tag

def handleLink(tag, originalAddress, newAddress):
    if tag.has_attr("href"):
        tag["href"] = replaceLink(tag["href"], originalAddress, newAddress)
    return tag

def handleMeta(tag, originalAddress, newAddress):
    if tag.has_attr("content"):
        tag["content"] = replaceLink(tag["content"], originalAddress, newAddress)
    return tag


def downloadPage(url, headers):
    r = requests.get(url, headers=headers)

    return r.text

def getPage(url, originalAddress, newAddress, headers):
    page = downloadPage(url, headers)
    
    page = replaceBabis(page)
    page = replaceANO(page)
    #page = addAdds(page)

    soup = BeautifulSoup(page, 'html.parser')
    for tag in soup.find_all():
        if tag.name == "a":
            tag = handleA(tag, originalAddress, newAddress)
        if tag.name == "meta":
            tag = handleMeta(tag, originalAddress, newAddress)
        if tag.name == "base":
            tag = handleBase(tag, originalAddress, newAddress)
        if tag.name == "link":
            tag = handleLink(tag, originalAddress, newAddress)
                    
    #taeyyng
    page = str(soup)
    return page