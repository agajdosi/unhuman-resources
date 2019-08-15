import aiohttp
import asyncio
import time

async def getPages():
    session = aiohttp.ClientSession(loop=loop, connector=aiohttp.TCPConnector(ssl=False))

    tasks = [getPage(session) for x in range(10)]
    await asyncio.wait(tasks)

    await session.close()

async def getPage(session):
    print("getting page")
    #url = "http://localhost:8080"
    #url = "http://favu.vut.cz"
    url = "https://l-dnes.cz"
    async with session.get(url) as resp:
        r = await resp.text()
        print("got the page")
        return


loop = asyncio.get_event_loop()
loop.run_until_complete(getPages())
loop.close()

    




