# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\azurerm\resourcegroups.py
# Compiled at: 2018-11-06 13:51:27
# Size of source mod 2**32: 4173 bytes
"""resourcegroups.py - azurerm functions for Resource Groups."""
import json
from .restfns import do_delete, do_get, do_post, do_put
from .settings import get_rm_endpoint, RESOURCE_API

def create_resource_group(access_token, subscription_id, rgname, location):
    """Create a resource group in the specified location.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.
        location (str): Azure data center location. E.g. westus.

    Returns:
        HTTP response. JSON body.
    """
    endpoint = ''.join([get_rm_endpoint(),
     '/subscriptions/', subscription_id,
     '/resourcegroups/', rgname,
     '?api-version=', RESOURCE_API])
    rg_body = {'location': location}
    body = json.dumps(rg_body)
    return do_put(endpoint, body, access_token)


def delete_resource_group(access_token, subscription_id, rgname):
    """Delete the named resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.

    Returns:
        HTTP response.
    """
    endpoint = ''.join([get_rm_endpoint(),
     '/subscriptions/', subscription_id,
     '/resourcegroups/', rgname,
     '?api-version=', RESOURCE_API])
    return do_delete(endpoint, access_token)


def export_template(access_token, subscription_id, rgname):
    """Capture the specified resource group as a template

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.

    Returns:
        HTTP response. JSON body.
    """
    endpoint = ''.join([get_rm_endpoint(),
     '/subscriptions/', subscription_id,
     '/resourcegroups/', rgname,
     '/exportTemplate',
     '?api-version=', RESOURCE_API])
    rg_body = {'options':'IncludeParameterDefaultValue',  'resources':['*']}
    body = json.dumps(rg_body)
    return do_post(endpoint, body, access_token)


def get_resource_group(access_token, subscription_id, rgname):
    """Get details about the named resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.

    Returns:
        HTTP response. JSON body.
    """
    endpoint = ''.join([get_rm_endpoint(),
     '/subscriptions/', subscription_id,
     '/resourceGroups/', rgname,
     '?api-version=', RESOURCE_API])
    return do_get(endpoint, access_token)


def get_resource_group_resources(access_token, subscription_id, rgname):
    """Get the resources in the named resource group.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rgname (str): Azure resource group name.

    Returns:
        HTTP response. JSON body.
    """
    endpoint = ''.join([get_rm_endpoint(),
     '/subscriptions/', subscription_id,
     '/resourceGroups/', rgname,
     '/resources?api-version=', RESOURCE_API])
    return do_get(endpoint, access_token)


def list_resource_groups(access_token, subscription_id):
    """List the resource groups in a subscription.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.

    Returns:
        HTTP response.
    """
    endpoint = ''.join([get_rm_endpoint(),
     '/subscriptions/', subscription_id,
     '/resourceGroups/',
     '?api-version=', RESOURCE_API])
    return do_get(endpoint, access_token)