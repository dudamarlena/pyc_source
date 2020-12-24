# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mcazurerm\amsrp.py
# Compiled at: 2017-08-11 23:27:04
# Size of source mod 2**32: 3554 bytes
from .restfns import do_get, do_post, do_put, do_delete
from .settings import azure_rm_endpoint, MEDIA_API

def check_media_service_name_availability(access_token, subscription_id, name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/microsoft.media/CheckNameAvailability?api-version=', MEDIA_API])
    body = '{"name": "' + name + '", "type":"mediaservices"}'
    return do_post(endpoint, body, access_token)


def create_media_service_rg(access_token, subscription_id, rgname, location, stoname, name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', rgname,
     '/providers/microsoft.media/mediaservices/' + name + '?api-version=', MEDIA_API])
    body = '{"name":"' + name + '", "location":"' + location + '", "properties":{  "storageAccounts":[  {  "id":"/subscriptions/' + subscription_id + '/resourceGroups/' + rgname + '/providers/Microsoft.Storage/storageAccounts/' + stoname + '", "isPrimary":true } ] } }'
    return do_put(endpoint, body, access_token)


def delete_media_service_rg(access_token, subscription_id, rgname, location, stoname, name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', rgname,
     '/providers/microsoft.media/mediaservices/' + name + '?api-version=', MEDIA_API])
    return do_delete(endpoint, access_token)


def list_media_endpoint_keys(access_token, subscription_id, rgname, msname):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', rgname,
     '/providers/microsoft.media/',
     '/mediaservices/', msname,
     '/listKeys?api-version=', MEDIA_API])
    return do_get(endpoint, access_token)


def list_media_services(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/microsoft.media/mediaservices?api-version=', MEDIA_API])
    return do_get(endpoint, access_token)


def list_media_services_rg(access_token, subscription_id, rgname):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', rgname,
     '/providers/microsoft.media/mediaservices?api-version=', MEDIA_API])
    return do_get(endpoint, access_token)