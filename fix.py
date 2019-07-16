"""
Package fixes concrete bugs on specific pages.
"""

from bs4 import BeautifulSoup

def fixIdnes(page):
    soup = BeautifulSoup(page, 'html.parser')

    try:
        div = soup.find("div", id="votwyrak")
        if div != None:
            imgDiv = div.find("div", class_="art-img")
            img = imgDiv.find("img")
            img["style"] = "height: 315px;"
    except:
        pass

    try:
        div = soup.find("a", class_="icon-unpack")
        div["style"] = "height: 37px;"
    except:
        pass

    return str(soup)

def fixLidovky(page):
    soup = BeautifulSoup(page, 'html.parser')

    try:
        header = soup.find(class_="adbox")
        header["class"] = "deadbox"
    except:
        pass

    return str(soup)

def fix(page, originalAddress):
    if originalAddress == "idnes.cz":
        page = fixIdnes(page)
    if originalAddress == "lidovky.cz":
        page = fixLidovky(page)

    return page