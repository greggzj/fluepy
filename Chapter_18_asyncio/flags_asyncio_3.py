#from __future__ import absolute_import
import asyncio

import aiohttp # 1 需要安装， 非built-in library

from flags_1 import BASE_URL, save_flag, show, main

@asyncio.coroutine 
def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = yield from aiohttp.request('GET', url)
    image = yield from resp.read()
    return image

@asyncio.coroutine
def download_one(cc):
    image = yield from get_flag(cc)
    show(cc)
    save_flag(image, cc.lower()+'.gif')
    return cc

def download_many(cc_list):
    loop = asyncio.get_event_loop()
    to_do = [download_one(cc) for cc in sorted(cc_list)] #9
    wait_coro = asyncio.wait(to_do) #10
    res, _ = loop.run_until_complete(wait_coro) #11
    loop.close() #12

    return len(res)

if __name__ == "__main__":
    main(download_many)