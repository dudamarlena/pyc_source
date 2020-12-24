# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/testing/util.py
# Compiled at: 2018-12-14 10:07:17
# Size of source mod 2**32: 2674 bytes
""" Utility functions. """
import sys, aiohttp, aiofiles, asyncio, requests
from functools import partial, wraps
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
__all__ = [
 'save_file',
 'load_file',
 'get_page',
 'threaded']

def threaded(func):

    @wraps(func)
    async def wrap(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))

    return wrap


async def save_file(file, data, binary=False):
    mode = 'w' if not binary else 'wb'
    async with aiofiles.open(file, mode=mode) as f:
        await f.write(data)


async def load_file(file, binary=False):
    mode = 'r' if not binary else 'rb'
    async with aiofiles.open(file, mode=mode) as f:
        return await f.read()


@threaded
def get_page_win(url, proxy=None, proxy_auth=None, binary=False, verify=False, timeout=300):
    proxies = None
    if proxy:
        if proxy_auth:
            proxy = proxy.replace('http://', '')
            username = proxy_auth['username']
            password = proxy_auth['password']
            proxies = {'http':f"http://{username}:{password}@{proxy}", 
             'https':f"http://{username}:{password}@{proxy}"}
        else:
            proxies = {'http':proxy, 
             'https':proxy}
    with requests.Session() as (session):
        response = session.get(url,
          proxies=proxies,
          verify=verify,
          timeout=timeout)
        if binary:
            return response.content
        return response.text


async def get_page(url, proxy=None, proxy_auth=None, binary=False, verify=False, timeout=300):
    if sys.platform == 'win32':
        return await get_page_win(url, proxy, proxy_auth, binary, verify, timeout)
    if proxy_auth:
        proxy_auth = aiohttp.BasicAuth(proxy_auth['username'], proxy_auth['password'])
    async with aiohttp.ClientSession() as session:
        async with session.get(url,
          proxy=proxy,
          proxy_auth=proxy_auth,
          verify_ssl=verify,
          timeout=timeout) as response:
            if binary:
                return await response.read()
            return await response.text()