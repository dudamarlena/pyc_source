# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mcazurerm\resourcegroups.py
# Compiled at: 2017-08-11 23:27:04
# Size of source mod 2**32: 1910 bytes
from .restfns import do_delete, do_get, do_put
from .settings import azure_rm_endpoint, BASE_API

def create_resource_group(access_token, subscription_id, rgname, location):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourcegroups/', rgname,
     '?api-version=', BASE_API])
    body = ''.join(['{\n   "location": "', location, '"\n}'])
    return do_put(endpoint, body, access_token)


def delete_resource_group(access_token, subscription_id, rgname):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourcegroups/', rgname,
     '?api-version=', BASE_API])
    return do_delete(endpoint, access_token)


def get_resource_group(access_token, subscription_id, rgname):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', rgname,
     '?api-version=', BASE_API])
    return do_get(endpoint, access_token)


def list_resource_groups(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/',
     '?api-version=', BASE_API])
    return do_get(endpoint, access_token)