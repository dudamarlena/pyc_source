# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/utils/request.py
# Compiled at: 2018-07-30 04:17:15
# Size of source mod 2**32: 639 bytes
from django.http import HttpRequest
import workon
__all__ = [
 'contribute_to_request']

def get_memoized_method(r, method, attr_name):
    if not hasattr(r, attr_name):
        setattr(r, attr_name, method(r))
    return getattr(r, attr_name)


def contribute_to_request(name, method, cache=None, memoized=True):
    if memoized == True:
        setattr(HttpRequest, name, lambda r: get_memoized_method(r, method, f"{name}__memoized_result"))
    else:
        if cache:
            setattr(HttpRequest, name, lambda r: workon.cache_get_or_set(f"workon_httprequest_cached_{name}", method(r), cache))
        else:
            setattr(HttpRequest, name, method)