# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mcazurerm\subfns.py
# Compiled at: 2017-08-11 23:27:04
# Size of source mod 2**32: 852 bytes
from .restfns import do_get
from .settings import azure_rm_endpoint, BASE_API

def list_locations(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/locations?api-version=', BASE_API])
    return do_get(endpoint, access_token)


def list_subscriptions(access_token):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/',
     '?api-version=', BASE_API])
    return do_get(endpoint, access_token)