# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/btp/util/fetcher.py
# Compiled at: 2017-11-04 01:43:23
# Size of source mod 2**32: 652 bytes
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from btp.util import req
MAX_RETRIES = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
HTTP_ADAPTER = HTTPAdapter(max_retries=MAX_RETRIES)

def __get_session(url):
    session = requests.Session()
    session.mount(url, HTTP_ADAPTER)
    return session


def get_trackers_content(url, proxy=None):
    return __get_session(url).get(url, proxies=(req.build_proxies(proxy))).text


def parse_content(content):
    return [item.strip() for item in content.split('\n') if item.strip()]