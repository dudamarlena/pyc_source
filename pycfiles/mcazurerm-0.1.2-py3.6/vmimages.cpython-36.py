# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mcazurerm\vmimages.py
# Compiled at: 2017-08-11 23:27:04
# Size of source mod 2**32: 2584 bytes
from .restfns import do_get
from .settings import azure_rm_endpoint, COMP_API

def list_offers(access_token, subscription_id, location, publisher):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Compute/',
     'locations/', location,
     '/publishers/', publisher,
     '/artifacttypes/vmimage/offers?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def list_publishers(access_token, subscription_id, location):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Compute/',
     'locations/', location,
     '/publishers?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def list_skus(access_token, subscription_id, location, publisher, offer):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Compute/',
     'locations/', location,
     '/publishers/', publisher,
     '/artifacttypes/vmimage/offers/', offer,
     '/skus?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def list_sku_versions(access_token, subscription_id, location, publisher, offer, sku):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Compute/',
     'locations/', location,
     '/publishers/', publisher,
     '/artifacttypes/vmimage/offers/', offer,
     '/skus/', sku,
     '/versions?api-version=', COMP_API])
    return do_get(endpoint, access_token)