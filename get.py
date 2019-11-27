import aiohttp
import time
from bs4 import BeautifulSoup
import tornado

from replace import *
import settings

proxies = [
	{'proxy': "", "score": 200.0},
        {'proxy': "", "score": 200.0},
        {'proxy': "", "score": 200.0},
        {'proxy': "http://185.219.164.139:8080", "score": 100.0},
        {'proxy': "http://46.28.108.251:3128", "score": 100.0},
        {'proxy': "http://80.250.20.190:8080", "score": 100.0},
        {'proxy': "http://77.48.22.59:38415", "score": 100.0},
        {'proxy': "http://46.227.14.107:52689", "score": 100.0},
        {'proxy': "http://193.165.152.110:8080", "score": 100.0},
        {'proxy': "http://79.110.39.161:8080", "score": 100.0},
        {'proxy': "http://82.100.63.181:51719", "score": 100.0},
        {'proxy': "http://89.187.181.123:3128", "score": 100.0},
        {'proxy': "http://178.77.238.2:8080", "score": 100.0},
        {'proxy': "http://88.146.168.15:60381", "score": 100.0},
        {'proxy': "http://77.48.23.181:38813", "score": 100.0},
        {'proxy': "http://46.227.169.206:8888", "score": 100.0},
        {'proxy': "http://46.183.56.107:49725", "score": 100.0},
        {'proxy': "http://84.42.253.252:52854", "score": 100.0},
        {'proxy': "http://89.248.244.182:8080", "score": 100.0},
        {'proxy': "http://78.108.110.113:8080", "score": 100.0},
        {'proxy': "http://185.47.223.53:8080", "score": 100.0},
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
    
    # disable evil script
    page = page.replace("//1gr.cz/js/uni/uni.js", "uni.js")

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
