# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/mailhandler/adapters.py
# Compiled at: 2019-09-10 05:47:40
# Size of source mod 2**32: 910 bytes
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

import requests

class BaseAdapter:
    base_url = 'https://api.mailhandler.ru/'
    default_headers = {'Content-Type':'application/json', 
     'Accept':'application/json'}

    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.headers = self.default_headers.copy()
        self.headers.update(kwargs.get('headers', {}))

    def get_url(self, url):
        return urljoin(self.base_url, url)

    def _post(self, url, data, **kwargs):
        with self.session as (s):
            return (s.post)(url=url, json=data, headers=self.headers, verify=False, **kwargs)

    def _get(self, url, params=None, **kwargs):
        with self.session as (s):
            return (s.get)(url=url, params=params, headers=self.headers, verify=False, **kwargs)