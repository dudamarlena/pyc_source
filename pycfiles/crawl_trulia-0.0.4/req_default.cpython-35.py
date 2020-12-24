# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\crawl_requests\req_default.py
# Compiled at: 2018-01-31 06:24:40
# Size of source mod 2**32: 6581 bytes
import random, requests
from .config_UA import *
from .config_proxy import gen

class Req:

    def __init__(self, page=1):
        self.page_size = page + 1
        self.default_UA = PC_UA_POOL
        self.gen_proxy_pool = gen.gen_pool(self.page_size)
        self.default_PROXY = gen.test_pool(self.gen_proxy_pool)
        self.default_PROXY.insert(0, {})

    def _default_proxy(self):
        return self.default_PROXY

    def ua_req(self, method, url, UA_list=None, **kwargs):
        """
        :param method: str, 'get' or 'post'.
        :param url: str, eg: 'https://www.python.org'.
        :param UA_list: list or None. Default_use: self.default_UA.
        :param kwargs: like '**kwargs' of `requests`.
        :return: <Response> or None.
        """
        ss = requests.Session()
        if UA_list:
            ss.headers.update({'User-Agent': random.choice(UA_list)})
        else:
            ss.headers.update({'User-Agent': random.choice(self.default_UA)})
        try:
            if method == 'get':
                res = ss.get(url, **kwargs)
                return res
            if method == 'post':
                res = ss.post(url, **kwargs)
                return res
        finally:
            ss.close()

    def proxy_req(self, method, url, PROXY_list=None, **kwargs):
        """
        :param method: str, 'get' or 'post'.
        :param url: str, eg: 'https://www.python.org'.
        :param PROXY_list: list or None. Default_use: self.default_PROXY.
        :param kwargs: like '**kwargs' of `requests`.
        :return: <Response> or None.
        """
        ss = requests.Session()
        if PROXY_list:
            ss.proxies.update(random.choice(PROXY_list))
        else:
            ss.proxies.update(random.choice(self.default_PROXY))
        try:
            if method == 'get':
                res = ss.get(url, **kwargs)
                return res
            if method == 'post':
                res = ss.post(url, **kwargs)
                return res
        finally:
            ss.close()

    def _all_req(self, method, url, UA_list=None, PROXY_list=None, **kwargs):
        """
        :param method: str, 'get' or 'post'.
        :param url: str, eg: 'https://www.python.org'.
        :param UA_list: list or None. Default_use: self.default_UA.
        :param PROXY_list: list or None. Default_use: self.default_PROXY.
        :param kwargs: like '**kwargs' of `requests`.
        :return: <Response> or None.
        """
        global choice_proxy
        global choose_proxy
        ss = requests.Session()
        if UA_list:
            ss.headers.update({'User-Agent': random.choice(UA_list)})
        else:
            ss.headers.update({'User-Agent': random.choice(self.default_UA)})
        if PROXY_list:
            choose_proxy = random.choice(PROXY_list)
            ss.proxies.update(random.choice(choose_proxy))
        else:
            choice_proxy = random.choice(self.default_PROXY)
            ss.proxies.update(choice_proxy)
        try:
            try:
                if method == 'get':
                    res = ss.get(url, **kwargs)
                    return res
                if method == 'post':
                    res = ss.post(url, **kwargs)
                    return res
            except:
                if PROXY_list:
                    PROXY_list.remove(choose_proxy)
                else:
                    self.default_PROXY.remove(choice_proxy)
                    if not self.default_PROXY:
                        print('default_PROXY is None!')

        finally:
            ss.close()

    def _keep_req(self, method, url, timeout=60, **kwargs):
        """
        _test
        :param method: str, 'get' or 'post'.
        :param url: str, eg: 'https://www.python.org'.
        :param kwargs: like '**kwargs' of `requests`.
        :return: <Response> or None.
        """
        ss = requests.Session()
        real_PROXY = self.default_PROXY
        if {} in real_PROXY:
            real_PROXY.remove({})
        for pxy in real_PROXY:
            ss.headers.update({'User-Agent': random.choice(self.default_UA)})
            ss.proxies.update(pxy)
            try:
                try:
                    if method == 'get':
                        r = ss.get(url, timeout=timeout, **kwargs)
                        if r.status_code == requests.codes.ok:
                            pass
                        return r
                    if method == 'post':
                        r = ss.post(url, timeout=timeout, **kwargs)
                        if r.status_code == requests.codes.ok:
                            pass
                        return r
                except:
                    pass

            finally:
                ss.close()

    def keep_req(self, method, url, timeout=60, **kwargs):
        """
        :param method: str, 'get' or 'post'.
        :param url: str, eg: 'https://www.python.org'.
        :param kwargs: like '**kwargs' of `requests`.
        :return: <Response> or None.
        """
        ss = requests.Session()
        for pxy in self.default_PROXY:
            ss.headers.update({'User-Agent': random.choice(self.default_UA)})
            ss.proxies.update(pxy)
            try:
                try:
                    if method == 'get':
                        r = ss.get(url, timeout=timeout, **kwargs)
                        if r.status_code == requests.codes.ok:
                            pass
                        return r
                    if method == 'post':
                        r = ss.post(url, timeout=timeout, **kwargs)
                        if r.status_code == requests.codes.ok:
                            pass
                        return r
                except:
                    print('Warning: proxy `{}` does not work.'.format(pxy))

            finally:
                ss.close()