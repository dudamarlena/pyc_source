# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sci_api_req/config.py
# Compiled at: 2019-08-25 12:00:50
# Size of source mod 2**32: 254 bytes
_api_keys = {'NASA': ''}

def set_api_keys(api_and_key: tuple) -> None:
    if len(api_and_key) > 2:
        raise Exception('Too many args')
    api, key = api_and_key
    _api_keys[api] = key


def get_api_keys(k) -> str:
    return _api_keys[k]