"""
Package fixes concrete bugs on specific pages.
"""

from bs4 import BeautifulSoup

def fixIdnes(soup):
    try:
        div = soup.find("div", id="votwyrak")
        if div != None:
            img = div.find("div", class_="art-img").find("img")
            img["style"] = "height: 315px;"
    except:
        pass

    try:
        div = soup.find("a", class_="icon-unpack")
        div["style"] = "height: 37px;"
    except:
        pass

    return

def fixLidovky(soup):
    try:
        header = soup.find(class_="adbox")
        header["class"] = "deadbox"
    except:
        pass

    return

def fix(soup, originalAddress):
    if originalAddress == "idnes.cz":
        fixIdnes(soup)
    if originalAddress == "lidovky.cz":
        fixLidovky(soup)

    return
