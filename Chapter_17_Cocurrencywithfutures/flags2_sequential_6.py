# Example A-11. flags2_sequential.py

"""Download flags of countries (with error handling).

Sequential version

Sample run::

    $ python3 flags2_sequential.py -s DELAY b
    DELAY site: http://localhost:8002/flags
    Searching for 26 flags: from BA to BZ
    1 concurrent connection will be used.
    --------------------
    17 flags downloaded.
    9 not found.
    Elapsed time: 13.36s


    Or

    $ python3 flags2_sequential.py
    LOCAL site: http://localhost:8001/flags
    Searching for 20 flags: from BD to VN
    1 concurrent connection will be used.
    --------------------
    20 flags downloaded.
    Elapsed time: 0.10s
"""

import collections

import requests
import tqdm

from flags2_common_5 import main, save_flag, HTTPStatus, Result

DEFAULT_CONCUR_REQ = 1

MAX_CONCUR_REQ = 1

# BEGIN FLAG2_BASIC_HTTP_FUNCTIONS
def get_flag(base_url, cc):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    resp = requests.get(url)
    # 这里没有error handling，如果返回的status code不是200，调用
    # requests.Response.raise_for_status来raise 一个exception
    if resp.status_code != 200: 
        resp.raise_for_status()
    return resp.content


def download_one(cc, base_url, verbose=False):
    try:
        image = get_flag(base_url, cc)
    # 2 使用requests.exceptions.HTTPError来catch可能的HTTP错误，比如404
    except requests.exceptions.HTTPError as exc:
        res = exc.response
        if res.status_code == 404:
            # 3 如果返回404，本地status替换为HTTPStatus.not_found，
            # HTTPStatus是一个Enum类型
            status = HTTPStatus.not_found
            msg = 'not found'
        else: # Any other HTTPError exception is re-raised; other exceptions 
              # will just propagate to the caller.
            # 除了400之外的其余HTTPError 会被reraise
            # 除了HTTPError之外的其余exception会被传递到caller
            # 想问下reraise和传递到caller两者的区别在哪里？？？？？？
            raise
    else:
        save_flag(image, cc.lower() + '.gif')
        status = HTTPStatus.ok
        msg = 'OK'

    if verbose:
        print(cc, msg)

    # 6 返回namedtuple Result, 携带自定义的status和country code
    return Result(status, cc)
# END FLAG2_BASIC_HTTP_FUNCTIONS


# BEGIN FLAGS_DOWNLOAD_MANY_SEQUENTIAL
def download_many(cc_list, base_url, verbose, max_req):
    # 1 counter对象用于记录 HTTPStatus.ok,
    # HTTPStatus.not_found, or HTTPStatus.error 的个数
    counter = collections.Counter()
    # 2 
    cc_iter = sorted(cc_list)
    if not verbose:
        '''
        如果不在verbose模式，
        tqdm function consumes任意的iterable，produce一个iterator，当这个Iterator被
        consume时，会显示progress bar并计算剩余的item
        '''
        cc_iter = tqdm.tqdm(cc_iter)
    # 4
    for cc in cc_iter:
        try:
            # 5 
            res = download_one(cc, base_url, verbose)
        # 6 处理download_one中没有处理的error exception
        except requests.exceptions.HTTPError as exc:
            error_msg = 'HTTP error {res.status_code} - {res.reason}'
            error_msg = error_msg.format(res=exc.response)
        # 7
        except requests.exceptions.ConnectionError as exc:
            error_msg = 'Connection error'
        # 8
        else:
            error_msg = ''
            status = res.status
        
        if error_msg:
            status = HTTPStatus.error   # 9
            
        # 10
        counter[status] += 1
        # 11
        if verbose and error_msg:
            print('*** Error for {}: {}'.format(cc, error_msg))
    # 12
    return counter
# END FLAGS_DOWNLOAD_MANY_SEQUENTIAL


if __name__ == "__main__":
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)

































