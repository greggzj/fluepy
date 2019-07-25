# Example A-10 flag2_common.py

"""Utilities for second set of flag examples.
"""

import os
import time
import sys
import string
import argparse
from collections import namedtuple
from enum import Enum

Result = namedtuple('Result', 'status data')

HTTPStatus = Enum('Status', 'ok not_found error')

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()

DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1

SERVERS = {
    'REMOTE':   'http://flupy.org/data/flags',
    'LOCAL':    'http://localhost:8001/flags',
    'DELAY':    'http://localhost:8002/flags',
    'ERROR':    'http://localhost:8003/flags',
}

DEFAULT_SERVER = 'LOCAL'

DEST_DIR = 'downloads/'
CONUTRY_CODES_FILE = 'country_codes.txt'

def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)

def initial_report(cc_list, actual_req, server_label):
    if len(cc_list) <= 10:
        cc_msg = ', '.join(cc_list)
    else:
        cc_msg = 'from {} to {}'.format(cc_list[0], cc_list[-1])
    print('{} site: {}'.format(server_label, SERVERS[server_label]))
    msg = 'Searching for {} flag{}: {}'
    plural = 's' if len(cc_list) != 1 else ''
    print(msg.format(len(cc_list), plural, cc_msg))
    plural = 's' if actual_req != 1 else ''
    msg = '{} concurrent connection{} will be used.'
    print(msg.format(actual_req, plural))


def final_report(cc_list, counter, start_time):
    elapsed = time.time() - start_time
    print('-' * 20)
    msg = '{} flag{} downloaded.'
    plural = 's' if counter[HTTPStatus.ok] != 1 else ''
    print(msg.format(counter[HTTPStatus.ok], plural))
    if counter[HTTPStatus.not_found]:
        print(counter[HTTPStatus.not_found], 'not found.')
    if counter[HTTPStatus.error]:
        plural = 's' if counter[HTTPStatus.error] != 1 else ''
        print('{} error {}.'.format(counter[HTTPStatus.error], plural))
    print('Elapsed time: {:.2f}s'.format(elapsed))

def expand_cc_args(every_cc, all_cc, cc_args, limit):
    codes = set()
    A_Z = string.ascii_uppercase
    if every_cc:
        codes.update(a+b for a in A_Z for b in A_Z)
    elif all_cc:
        with open(CONUTRY_CODES_FILE) as fp:
            text = fp.read()
        codes.update(text.split())
    else:
        for cc in (c.upper() for c in cc_args):
            if len(cc) == 1 and cc in A_Z:
                codes.update(cc+c for c in A_Z)
            elif len(cc) == 2 and all(c in A_Z for c in cc):
                codes.add(cc)
            else:
                msg = 'each CC argument must be A to Z or AA to ZZ'
                raise ValueError('*** Usage error: '+msg)
    return sorted(codes)[:limit]

def process_args(default_concur_req):
    server_options = ', '.join(sorted(SERVERS))
    parser = argparse.ArgumentParser(
                description='Download flags for country codes. '
                'Default: top 20 countries by population.')
    parser.add_argument('cc', metavar='CC', nargs='*',
                help='country code or 1st letter (eg. B for BA...BZ)')
    parser.add_argument('-a', '--all', action='store_true',
                help='get all available flags (AD to ZW)')
    parser.add_argument('-e', '--every', action='store_true',
                help='get flags for every possible code (AA...ZZ)')
    parser.add_argument('-l', '--limit', metavar='N', type=int,
                help='limit to N first codes', default=sys.maxsize)
    parser.add_argument('-m', '--max_req', metavar='CONCURRENT', type=int,
                default=default_concur_req,
                help='maximum concurrent requests (default={})'
                        .format(default_concur_req))
    parser.add_argument('-s', '--server', metavar='LABEL',
                default=DEFAULT_SERVER,
                help='Server to hit; one of {} (default={})'
                        .format(server_options, DEFAULT_SERVER))
    parser.add_argument('-v', '--verbose', action='store_true',
                help='output detailed progress info')
    args = parser.parse_args()
    if args.max_req < 1:
        print('*** Usage error: --max_req CONCURRENT must be >= 1')
        parser.print_usage()
        sys.exit()
    if args.limit < 1:
        print('*** Usage error: --limit N must be >= 1')
        parser.print_usage()
        sys.exit(1)

    args.server = args.server.upper()
    if args.server not in SERVERS:
        print('*** Usage error: --server LABEL must be one of',
                server_options)
        parser.print_usage()
        sys.exit(1)
    try:
        cc_list = expand_cc_args(args.every, args.all, args.cc, args.limit)
    except ValueError as exc:
        print(exc.args[0])
        parser.print_usage()
        sys.exit(1)
    
    if not cc_list:
        cc_list = sorted(POP20_CC)
    return args, cc_list


def main(download_many, default_concur_req, max_concur_req):
    args, cc_list = process_args(default_concur_req)
    actual_req = min(args.max_req, max_concur_req, len(cc_list))
    initial_report(cc_list, actual_req, args.server)
    base_url = SERVERS[args.server]
    t0 = time.time()
    counter = download_many(cc_list, base_url, args.verbose, actual_req)
    assert sum(counter.values()) == len(cc_list), \
        'some downloads are unaccounted for'
    final_report(cc_list, counter, t0)



'''
Output for python3 flags2_threadpool.py -h
    usage: flags2_sequential_6.py [-h] [-a] [-e] [-l N] [-m CONCURRENT] [-s LABEL]
                                [-v]
                                [CC [CC ...]]

    Download flags for country codes. Default: top 20 countries by population.

    positional arguments:
    CC                    country code or 1st letter (eg. B for BA...BZ)

    optional arguments:
    -h, --help            show this help message and exit
    -a, --all             get all available flags (AD to ZW)
    -e, --every           get flags for every possible code (AA...ZZ)
    -l N, --limit N       limit to N first codes
    -m CONCURRENT, --max_req CONCURRENT
                            maximum concurrent requests (default=1)
    -s LABEL, --server LABEL
                            Server to hit; one of DELAY, ERROR, LOCAL, REMOTE
                            (default=LOCAL)
    -v, --verbose         output detailed progress info



    All arguments are optional. The most important arguments are discussed next.
One option you can’t ignore is -s/--server: it lets you choose which HTTP server and
base URL will be used in the test. You can pass one of four strings to determine where
the script will look for the flags (the strings are case insensitive):
LOCAL
Use http://localhost:8001/flags; this is the default. You should configure a
local HTTP server to answer at port 8001. I used Nginx for my tests. The README.
rst file for this chapter’s example code explains how to install and configure
it.
REMOTE
Use http://flupy.org/data/flags; that is a public website owned by me, hosted
on a shared server. Please do not pound it with too many concurrent requests. The
flupy.org domain is handled by a free account on the Cloudflare CDN so you may
notice that the first downloads are slower, but they get faster when the CDN cache
warms up.6
DELAY
Use http://localhost:8002/flags; a proxy delaying HTTP responses should be
listening at port 8002. I used a Mozilla Vaurien in front of my local Nginx to introduce
delays. The previously mentioned README.rst file has instructions for running
a Vaurien proxy.


ERROR
Use http://localhost:8003/flags; a proxy introducing HTTP errors and delaying
responses should be installed at port 8003. I used a different Vaurien configuration
for this.

By default, each flags2 script will fetch the flags of the 20 most populous countries
from the LOCAL server (http://localhost:8001/flags) using a default number of
concurrent connections, which varies from script to script. Example 17-9 shows a sample
run of the flags2_sequential.py script using all defaults.
'''