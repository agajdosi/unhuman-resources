import aiohttp
import time
from bs4 import BeautifulSoup
from replace import *
from fix import *

proxies = [
        {'proxy': "", "score": 200.0},
        {'proxy': "", "score": 200.0},
        {'proxy': "", "score": 200.0},
        {'proxy': "", "score": 200.0},
        {'proxy': "", "score": 200.0},
        {'proxy': "socks4://91.217.96.25:56636", "score": 100.0},
        {'proxy': "socks4://109.238.223.1:51372", "score": 100.0},
        {'proxy': "socks4://62.201.17.103:51178", "score": 100.0},
        {'proxy': "socks4://46.183.56.107:39799", "score": 100.0},
        {'proxy': "socks4://82.142.70.244:4145", "score": 100.0},
        {'proxy': "socks4://93.185.0.45:43398", "score": 100.0},
        {'proxy': "socks4://185.131.62.244:10080", "score": 100.0},
        {'proxy': "socks4://77.48.137.65:50523", "score": 100.0},
        {'proxy': "socks4://109.238.208.138:51372", "score": 100.0},
        {'proxy': "socks4://109.238.223.67:61150", "score": 100.0},
        {'proxy': "socks4://84.242.123.220:4145", "score": 100.0},
        {'proxy': "socks4://194.228.84.10:4145", "score": 100.0},
        {'proxy': "socks4://91.217.96.1:56636", "score": 100.0},
        {'proxy': "socks4://80.95.109.6:4145", "score": 100.0},
        {'proxy': "socks4://93.99.193.13:46380", "score": 100.0},
        {'proxy': "socks4://91.217.96.130:56636", "score": 100.0},
        {'proxy': "socks4://89.102.198.78:45399", "score": 100.0},
        {'proxy': "socks4://195.39.6.80:4145", "score": 100.0},
        {'proxy': "socks4://93.99.193.45:37503", "score": 100.0},
        {'proxy': "socks4://109.238.220.225:61221", "score": 100.0},
        {'proxy': "socks4://90.181.150.211:4145", "score": 100.0},
        {'proxy': "socks4://85.163.0.37:4145", "score": 100.0},
        {'proxy': "socks4://93.99.53.201:48577", "score": 100.0},
        {'proxy': "socks4://94.138.96.150:60883", "score": 100.0},
        {'proxy': "socks4://85.135.95.218:4145", "score": 100.0},
        {'proxy': "socks4://188.75.188.26:10801", "score": 100.0},
        {'proxy': "socks4://77.48.29.70:45709", "score": 100.0},
        {'proxy': "socks4://185.131.61.114:4145", "score": 100.0},
        {'proxy': "socks4://89.24.119.126:4145", "score": 100.0},
        {'proxy': "socks4://90.181.236.217:54495", "score": 100.0},
        {'proxy': "socks4://109.238.222.1:4153", "score": 100.0},
        {'proxy': "socks4://109.164.113.55:4145", "score": 100.0},
        {'proxy': "socks4://217.77.171.114:4145", "score": 100.0},
        {'proxy': "socks4://62.168.57.109:41983", "score": 100.0},
        {'proxy': "socks4://82.142.87.2:4145", "score": 100.0}
          ]

async def handleA(tag, originalAddress, newAddress):
    if tag.has_attr("href"):
        tag["href"] = await replaceLink(tag["href"], originalAddress, newAddress)
    return tag

async def handleBase(tag, originalAddress, newAddress):
    if tag.has_attr("href"):
        tag["href"] = await replaceLink(tag["href"], originalAddress, newAddress)
    return tag

async def handleLink(tag, originalAddress, newAddress):
    if tag.has_attr("href"):
        tag["href"] = await replaceLink(tag["href"], originalAddress, newAddress)
    return tag

async def handleMeta(tag, originalAddress, newAddress):
    if tag.has_attr("content"):
        tag["content"] = await replaceLink(tag["content"], originalAddress, newAddress)
    return tag

def getProxyScore(item):
    return item["score"]

async def downloadPage(url, headers):
    proxies.sort(key=getProxyScore, reverse=True)
    order = list(range(len(proxies)-1))
    temp = order[:5]
    random.shuffle(temp)
    order[:5] = temp
    tried = 0

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            r = await resp.text()
    return r
    
    """
    while True:
        #TODO handle absolute disaster: when tried > 100 report 404 or something
        try:
            x = tried % len(proxies)
            x = order[x]
            proxy = {"http" : proxies[x]["proxy"], "https" : proxies[x]["proxy"]}
            r = requests.get(url, headers=headers, proxies=proxy, timeout=2)
            proxies[x]["score"] += 1
            return r.text
        except:
            proxies[x]["score"] /= 2
            print("proxy request failed:", proxy)
        finally:
            tried += 1
    """

async def getPage(url, originalAddress, newAddress, headers):
    start = time.time()
    page = await downloadPage(url, headers)
    print("download took", time.time() - start)

    start = time.time()
    page = await replaceBabis(page)
    print("replacing babis took", time.time() - start)

    start = time.time()
    page = await replaceANO(page)
    print("replacing ano took", time.time() - start)
    
    start = time.time()
    soup = BeautifulSoup(page, 'html.parser')
    print("making soop took", time.time() - start)

    start = time.time()
    await addChants(soup)
    print("adding chants took", time.time() - start)
    
    start = time.time()
    fix(soup, originalAddress)
    print("fixing html took", time.time() - start)
    
    start = time.time()
    for tag in soup.find_all():
        if tag.name == "a":
            tag = await handleA(tag, originalAddress, newAddress)
        if tag.name == "meta":
            tag = await handleMeta(tag, originalAddress, newAddress)
        if tag.name == "base":
            tag = await handleBase(tag, originalAddress, newAddress)
        if tag.name == "link":
            tag = await handleLink(tag, originalAddress, newAddress)
    print("replacing links took", time.time() - start)
    
    start = time.time()
    page = str(soup)
    print("converting to string took", time.time() - start)

    return page

session = aiohttp.ClientSession()
