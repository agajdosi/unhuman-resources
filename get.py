import aiohttp
import time
from bs4 import BeautifulSoup
import tornado

from replace import *
from fix import *
import settings

proxies = [
        {'proxy': "", "score": 200.0},
        {'proxy': "", "score": 200.0},
        {'proxy': "", "score": 200.0},
        {'proxy': "http://85.93.104.118:8080", "score": 100.0},
        {'proxy': "http://81.200.63.108:60579", "score": 100.0},
        {'proxy': "http://212.67.65.82:55532", "score": 100.0},
        {'proxy': "http://82.100.4.63:44348", "score": 100.0},
        {'proxy': "http://178.20.137.178:43980", "score": 100.0},
        {'proxy': "http://185.15.252.41:8080", "score": 100.0},
        {'proxy': "http://77.48.22.59:51359", "score": 100.0},
        {'proxy': "http://128.0.179.234:41258", "score": 100.0},
        {'proxy': "http://89.24.126.164:80", "score": 100.0},
        {'proxy': "http://89.248.244.182:8080", "score": 100.0},
        {'proxy': "http://84.42.253.252:52854", "score": 100.0},
        {'proxy': "http://93.99.176.84:3128", "score": 100.0},
        {'proxy': "http://78.108.110.113:8080", "score": 100.0},
        {'proxy': "http://95.80.252.189:52371", "score": 100.0},
        {'proxy': "http://85.207.44.10:53038", "score": 100.0},
        {'proxy': "http://185.199.84.161:53281", "score": 100.0},
        {'proxy': "http://89.102.2.149:8080", "score": 100.0},
        {'proxy': "http://78.41.19.181:8080", "score": 100.0},
          ]
random.shuffle(proxies)

def handleA(tag, originalAddress, newAddress):
    if tag.has_attr("href"):
        tag["href"] = replaceLink(tag["href"], originalAddress, newAddress)
    return

def handleBase(tag, originalAddress, newAddress):
    if tag.has_attr("href"):
        tag["href"] = replaceLink(tag["href"], originalAddress, newAddress)
    return

def handleLink(tag, originalAddress, newAddress):
    if tag.has_attr("href"):
        tag["href"] = replaceLink(tag["href"], originalAddress, newAddress)
    return

def handleMeta(tag, originalAddress, newAddress):
    if tag.has_attr("property") and tag["property"]=="og:image":
        return
    if tag.has_attr("content"):
        tag["content"] = replaceLink(tag["content"], originalAddress, newAddress)
    return

def getProxyScore(item):
    return item["score"]

async def downloadPage(url, headers):
    proxies.sort(key=getProxyScore, reverse=True)
    order = list(range(len(proxies)-1))
    temp = order[:3]
    random.shuffle(temp)
    order[:3] = temp

    for x in order:
        try:
            if settings.args.debug == True:
                print("using proxy: '{}'".format(proxies[x]["proxy"]))
            
            d = time.time()
            async with session.get(url, timeout=5, proxy=proxies[x]["proxy"], headers=headers) as resp:
                r = await resp.text()
                print("clean download took",time.time()-d)
                proxies[x]["score"] += 1
                return r
        except:
            proxies[x]["score"] /= 2
            if settings.args.debug == True:
                print("proxy request failed: '{}'".format(proxies[x]["proxy"]))
                print(proxies)

    raise tornado.web.HTTPError(status_code=503, log_message="unable to download pages")


async def getPage(url, originalAddress, newAddress, headers):
    start = time.time()
    page = await downloadPage(url, headers)
    print("download took", time.time() - start)

    start = time.time()
    page = replaceBabis(page)
    print("replacing babis took", time.time() - start)

    start = time.time()
    page = replaceANO(page)
    print("replacing ano took", time.time() - start)
    
    start = time.time()
    soup = BeautifulSoup(page, 'lxml')
    print("making soop took", time.time() - start)

    start = time.time()
    addChants(soup)
    addGAnalytics(soup, originalAddress)
    print("adding chants and GAnalytics took", time.time() - start)
    
    start = time.time()
    for tag in soup.find_all():
        if tag.name == "a":
            handleA(tag, originalAddress, newAddress)
        if tag.name == "meta":
            handleMeta(tag, originalAddress, newAddress)
        if tag.name == "base":
            handleBase(tag, originalAddress, newAddress)
        if tag.name == "link":
            handleLink(tag, originalAddress, newAddress)
    print("replacing links took", time.time() - start)
    
    start = time.time()
    page = str(soup)
    print("converting to string took", time.time() - start)

    return page

session = aiohttp.ClientSession()
