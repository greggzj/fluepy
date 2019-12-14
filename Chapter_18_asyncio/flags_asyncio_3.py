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
    import pdb
    pdb.set_trace()
    main(download_many)



"""
@asyncio.coroutine 号称If the coroutine is not yielded from before it is destroyed,
    an error message is logged.
但从代码看，只有在打开_DEBUG开关情况下才会将被修饰函数包装为CoWrapper，在del时才会有error msg，
如果该开关不打开似乎就是一个正常的coroutine函数，仅作为标记使用。

author在总结@asyncio.coroutine好处时没有强调_DEBUG开关，不知道是不是之前python版本所致。



"""