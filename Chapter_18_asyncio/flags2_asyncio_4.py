import asyncio
import collections

import aiohttp
from aiohttp import web
import tqdm

from .flags2_common import main, HTTPStatus, Result, save_flag

# default set low to avoid errors from remote site, such as 
# 503 - Service Temporarily Unavailable
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000

class FetchError(Exception):    # 1
    def __init__(self, country_code):
        self.country_code = country_code

@asyncio.coroutine
def get_flag(base_url, cc): # 2
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    resp = yield from aiohttp.request('GET', url)
    if resp.status == 200:
        image = yield from resp.read()
        return image
    elif resp.status == 404:
        raise web.HTTPNotFound()
    else:
        raise aiohttp.HttpProcessingError(
            code=resp.status, message=resp.reason,
            headers=resp.headers)

@asyncio.coroutine
def download_one(cc, base_url, semaphore, verbose): # 3
    try:
        with (yield from semaphore):    # 4
            image = yield from get_flag(base_url, cc)   # 5
    except web.HTTPNotFound:    # 6
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:
        raise FetchError(cc) from exc   # 7
    else:
        save_flag(image, cc.lower() + '.gif')   # 8
        status = HTTPStatus.ok
        msg = 'OK'
    
    if verbose and msg:
        print(cc, msg)
    
    return Result(status, cc)