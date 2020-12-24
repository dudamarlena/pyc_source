# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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