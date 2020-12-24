# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/request/patch/hook_request_redirect.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 558 bytes
import requests
from requests._internal_utils import to_native_string
from requests.compat import is_py3

def get_redirect_target(self, resp):
    """hook requests.Session.get_redirect_target method"""
    if resp.is_redirect:
        location = resp.headers['location']
        if is_py3:
            location = location.encode('latin1')
        encoding = resp.encoding if resp.encoding else 'utf-8'
        return to_native_string(location, encoding)


def patch_redirect():
    requests.Session.get_redirect_target = get_redirect_target