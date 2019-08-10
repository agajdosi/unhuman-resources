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
        {'proxy': "http://51.79.26.40:80", "score": 100.0},
        {'proxy': "http://31.13.15.94:21776", "score": 100.0},
        {'proxy': "http://46.246.16.3:8118", "score": 100.0},
        {'proxy': "http://78.108.110.113:8080", "score": 100.0},
        {'proxy': "http://83.167.253.143:9401	", "score": 100.0},
        {'proxy': "http://78.41.19.181:8080", "score": 100.0},
        {'proxy': "http://89.248.244.182:8080	", "score": 100.0},
        {'proxy': "http://158.255.249.58:34593", "score": 100.0},
        {'proxy': "http://198.50.147.158:3128", "score": 100.0},
        {'proxy': "http://54.39.53.104:3128", "score": 100.0},
        {'proxy': "http://198.211.102.155:8080", "score": 100.0},
        {'proxy': "http://104.248.53.46:3128", "score": 100.0},
        {'proxy': "http://136.243.47.220:3128", "score": 100.0},
        {'proxy': "http://94.237.120.190:8080", "score": 100.0},
        {'proxy': "http://173.249.53.235:3128", "score": 100.0},
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
    addGAnalytics(soup)
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
