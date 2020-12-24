# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ganesh/work/silota-python/silota/core.py
# Compiled at: 2013-11-29 21:49:23
from .api import API

def from_key(api_key):
    h = API()
    h.authenticate(api_key)
    return h