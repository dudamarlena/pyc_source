# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mcazurerm\storagerp.py
# Compiled at: 2017-08-11 23:27:04
# Size of source mod 2**32: 4298 bytes
from .restfns import do_delete, do_get, do_put, do_post
from .settings import azure_rm_endpoint, STORAGE_API

def create_storage_account(access_token, subscription_id, rgname, account_name, location, storage_type='Standard_LRS'):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourcegroups/', rgname,
     '/providers/Microsoft.Storage/storageAccounts/', account_name,
     '?api-version=', STORAGE_API])
    body = ''.join(['{\n   "location": "', location, '",\n',
     '   "sku": {\n      "name": "', storage_type, '"\n   },\n',
     '   "kind": "Storage"\n}'])
    return do_put(endpoint, body, access_token)


def delete_storage_account(access_token, subscription_id, rgname, account_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourcegroups/', rgname,
     '/providers/Microsoft.Storage/storageAccounts/', account_name,
     '?api-version=', STORAGE_API])
    return do_delete(endpoint, access_token)


def get_storage_account(access_token, subscription_id, rgname, account_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourcegroups/', rgname,
     '/providers/Microsoft.Storage/storageAccounts/', account_name,
     '?api-version=', STORAGE_API])
    return do_get(endpoint, access_token)


def get_storage_account_keys(access_token, subscription_id, rgname, account_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourcegroups/', rgname,
     '/providers/Microsoft.Storage/storageAccounts/', account_name,
     '/listKeys',
     '?api-version=', STORAGE_API])
    return do_post(endpoint, '', access_token)


def get_storage_usage(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Storage/usages',
     '?api-version=', STORAGE_API])
    return do_get(endpoint, access_token)


def list_storage_accounts_rg(access_token, subscription_id, rgname):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourcegroups/', rgname,
     '/providers/Microsoft.Storage/storageAccounts',
     '?api-version=', STORAGE_API])
    return do_get(endpoint, access_token)


def list_storage_accounts_sub(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Storage/storageAccounts',
     '?api-version=', STORAGE_API])
    return do_get(endpoint, access_token)