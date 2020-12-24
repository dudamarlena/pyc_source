# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/utils/request.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 607 bytes
import lru, requests
from web3.utils.caching import generate_cache_key
_session_cache = lru.LRU(8)

def _get_session(*args, **kwargs):
    cache_key = generate_cache_key((args, kwargs))
    if cache_key not in _session_cache:
        _session_cache[cache_key] = requests.Session()
    return _session_cache[cache_key]


def make_post_request(endpoint_uri, data, *args, **kwargs):
    kwargs.setdefault('timeout', 10)
    session = _get_session(endpoint_uri)
    response = (session.post)(endpoint_uri, *args, data=data, **kwargs)
    response.raise_for_status()
    return response.content