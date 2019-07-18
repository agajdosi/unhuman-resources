import requests
from bs4 import BeautifulSoup
from replace import *
from fix import *

proxies = [
        {'https': "socks4://91.217.96.25:56636", 'http': "socks4://91.217.96.25:56636"},
        {'https': "socks4://109.238.223.1:51372", 'http': "socks4://109.238.223.1:51372"},
        {'https': "socks4://62.201.17.103:51178", 'http': "socks4://62.201.17.103:51178"},
        {'https': "socks4://46.183.56.107:39799", 'http': "socks4://46.183.56.107:39799"},
        {'https': "socks4://82.142.70.244:4145", 'http': "socks4://82.142.70.244:4145"},
        {'https': "socks4://93.185.0.45:43398", 'http': "socks4://93.185.0.45:43398"},
        {'https': "socks4://185.131.62.244:10080", 'http': "socks4://185.131.62.244:10080"},
        {'https': "socks4://77.48.137.65:50523", 'http': "socks4://77.48.137.65:50523"},
        {'https': "socks4://109.238.208.138:51372", 'http': "socks4://109.238.208.138:51372"},
        {'https': "socks4://109.238.223.67:61150", 'http': "socks4://109.238.223.67:61150"},
        {'https': "socks4://84.242.123.220:4145", 'http': "socks4://84.242.123.220:4145"},
        {'https': "socks4://194.228.84.10:4145", 'http': "socks4://194.228.84.10:4145"},
        {'https': "socks4://91.217.96.1:56636", 'http': "socks4://91.217.96.1:56636"},
        {'https': "socks4://80.95.109.6:4145", 'http': "socks4://80.95.109.6:4145"},
        {'https': "socks4://93.99.193.13:46380", 'http': "socks4://93.99.193.13:46380"},
        {'https': "socks4://91.217.96.130:56636", 'http': "socks4://91.217.96.130:56636"},
        {'https': "socks4://89.102.198.78:45399", 'http': "socks4://89.102.198.78:45399"},
        {'https': "socks4://195.39.6.80:4145", 'http': "socks4://195.39.6.80:4145"},
        {'https': "socks4://93.99.193.45:37503", 'http': "socks4://93.99.193.45:37503"},
        {'https': "socks4://109.238.220.225:61221", 'http': "socks4://109.238.220.225:61221"},
        {'https': "socks4://90.181.150.211:4145", 'http': "socks4://90.181.150.211:4145"},
        {'https': "socks4://85.163.0.37:4145", 'http': "socks4://85.163.0.37:4145"},
        {'https': "socks4://93.99.53.201:48577", 'http': "socks4://93.99.53.201:48577"},
        {'https': "socks4://94.138.96.150:60883", 'http': "socks4://94.138.96.150:60883"},
        {'https': "socks4://85.135.95.218:4145", 'http': "socks4://85.135.95.218:4145"},
        {'https': "socks4://188.75.188.26:10801", 'http': "socks4://188.75.188.26:10801"},
        {'https': "socks4://77.48.29.70:45709", 'http': "socks4://77.48.29.70:45709"},
        {'https': "socks4://185.131.61.114:4145", 'http': "socks4://185.131.61.114:4145"},
        {'https': "socks4://89.24.119.126:4145", 'http': "socks4://89.24.119.126:4145"},
        {'https': "socks4://90.181.236.217:54495", 'http': "socks4://90.181.236.217:54495"},
        {'https': "socks4://109.238.222.1:4153", 'http': "socks4://109.238.222.1:4153"},
        {'https': "socks4://109.164.113.55:4145", 'http': "socks4://109.164.113.55:4145"},
        {'https': "socks4://217.77.171.114:4145", 'http': "socks4://217.77.171.114:4145"},
        {'https': "socks4://62.168.57.109:41983", 'http': "socks4://62.168.57.109:41983"},
        {'https': "socks4://82.142.87.2:4145", 'http': "socks4://82.142.87.2:4145"}
          ]

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
    while True:
        x = 0
        try:
            x = random.randint(0,len(proxies)-1)
            r = requests.get(url, headers=headers, proxies=proxies[x], timeout=5)
            break
        except:
            print("proxy failed:", proxies[x])

    return r.text

def getPage(url, originalAddress, newAddress, headers):
    page = downloadPage(url, headers)
    
    page = replaceBabis(page)
    page = replaceANO(page)

    page = fix(page, originalAddress)

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
    page = str(soup)
    return page