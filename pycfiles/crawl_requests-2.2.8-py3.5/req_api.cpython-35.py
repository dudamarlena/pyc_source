# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\crawl_requests\req_api.py
# Compiled at: 2018-01-31 05:50:43
# Size of source mod 2**32: 1963 bytes
import random, requests

def req_get(url: str, headers: dict, UA_pool: list, proxy_pool: list, **kwargs):
    session = requests.Session()
    try:
        try:
            res = session.get(url, headers=headers, **kwargs)
            return res
        except:
            try:
                if headers:
                    headers.update({'User-Agent': random.choice(UA_pool)})
                else:
                    headers = {'User-Agent': random.choice(UA_pool)}
                res = session.get(url, headers=headers, **kwargs)
                return res
            except:
                if headers:
                    headers.update({'User-Agent': random.choice(UA_pool)})
                else:
                    headers = {'User-Agent': random.choice(UA_pool)}
                res = session.get(url, headers=headers, proxies=random.choice(proxy_pool), **kwargs)
                return res

    finally:
        session.close()


def req_post(url: str, headers: dict, UA_pool: list, proxy_pool: list, **kwargs):
    session = requests.Session()
    try:
        try:
            res = session.post(url, headers=headers, **kwargs)
            return res
        except:
            try:
                if headers:
                    headers.update({'User-Agent': random.choice(UA_pool)})
                else:
                    headers = {'User-Agent': random.choice(UA_pool)}
                res = session.post(url, headers=headers, **kwargs)
                return res
            except:
                if headers:
                    headers.update({'User-Agent': random.choice(UA_pool)})
                else:
                    headers = {'User-Agent': random.choice(UA_pool)}
                res = session.post(url, headers=headers, proxies=random.choice(proxy_pool), **kwargs)
                return res

    finally:
        session.close()