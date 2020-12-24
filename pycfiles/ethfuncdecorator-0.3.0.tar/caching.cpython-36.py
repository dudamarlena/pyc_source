# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/utils/caching.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 1067 bytes
import hashlib
from eth_utils import is_boolean, is_bytes, is_dict, is_list_like, is_null, is_number, is_text, to_bytes
from .six import Generator

def generate_cache_key(value):
    """
    Generates a cache key for the *args and **kwargs
    """
    if is_bytes(value):
        return hashlib.md5(value).hexdigest()
    else:
        if is_text(value):
            return generate_cache_key(to_bytes(text=value))
        else:
            if is_boolean(value) or is_null(value) or is_number(value):
                return generate_cache_key(repr(value))
            if is_dict(value):
                return generate_cache_key((key, value[key]) for key in sorted(value.keys()))
        if is_list_like(value) or isinstance(value, Generator):
            return generate_cache_key(''.join(generate_cache_key(item) for item in value))
    raise TypeError('Cannot generate cache key for value {0} of type {1}'.format(value, type(value)))