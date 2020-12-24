# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\azurerm\vmimages.py
# Compiled at: 2018-11-06 13:51:27
# Size of source mod 2**32: 3837 bytes
"""vmimages.py - azurerm functions for Microsoft.Compute RP publishers and images"""
from .restfns import do_get
from .settings import get_rm_endpoint, COMP_API

def list_offers(access_token, subscription_id, location, publisher):
    """List available VM image offers from a publisher.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        location (str): Azure data center location. E.g. westus.
        publisher (str): Publisher name, e.g. Canonical.

    Returns:
        HTTP response with JSON list of image offers.
    """
    endpoint = ''.join([get_rm_endpoint(),
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Compute/',
     'locations/', location,
     '/publishers/', publisher,
     '/artifacttypes/vmimage/offers?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def list_publishers(access_token, subscription_id, location):
    """List available image publishers for a location. E.g. MicrosoftWindowsServer.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        location (str): Azure data center location. E.g. westus.

    Returns:
        HTTP response with JSON list of publishers.
    """
    endpoint = ''.join([get_rm_endpoint(),
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Compute/',
     'locations/', location,
     '/publishers?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def list_skus(access_token, subscription_id, location, publisher, offer):
    """List available VM image skus for a publisher offer.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        location (str): Azure data center location. E.g. westus.
        publisher (str): VM image publisher. E.g. MicrosoftWindowsServer.
        offer (str): VM image offer. E.g. WindowsServer.

    Returns:
        HTTP response with JSON list of skus.
    """
    endpoint = ''.join([get_rm_endpoint(),
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Compute/',
     'locations/', location,
     '/publishers/', publisher,
     '/artifacttypes/vmimage/offers/', offer,
     '/skus?api-version=', COMP_API])
    return do_get(endpoint, access_token)


def list_sku_versions(access_token, subscription_id, location, publisher, offer, sku):
    """List available versions for a given publisher's sku.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        location (str): Azure data center location. E.g. westus.
        publisher (str): VM image publisher. E.g. MicrosoftWindowsServer.
        offer (str): VM image offer. E.g. WindowsServer.
        sku (str): VM image sku. E.g. 2016-Datacenter.

    Returns:
        HTTP response with JSON list of versions.
    """
    endpoint = ''.join([get_rm_endpoint(),
     '/subscriptions/', subscription_id,
     '/providers/Microsoft.Compute/',
     'locations/', location,
     '/publishers/', publisher,
     '/artifacttypes/vmimage/offers/', offer,
     '/skus/', sku,
     '/versions?api-version=', COMP_API])
    return do_get(endpoint, access_token)