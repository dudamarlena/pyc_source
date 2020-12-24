# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\azurerm\deployments.py
# Compiled at: 2018-11-06 13:51:27
# Size of source mod 2**32: 1639 bytes
"""deployments.py - azurerm functions for Deployments"""
from .restfns import do_get
from .settings import get_rm_endpoint, BASE_API

def list_deployment_operations(access_token, subscription_id, rg_name, deployment_name):
    """List all operations involved in a given deployment.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rg_name (str): Azure resource group name.

    Returns:
        HTTP response. JSON body.
    """
    endpoint = ''.join([get_rm_endpoint(),
     '/subscriptions/', subscription_id,
     '/resourcegroups/', rg_name,
     '/providers/Microsoft.Resources/deployments/', deployment_name,
     '/operations',
     '?api-version=', BASE_API])
    return do_get(endpoint, access_token)


def show_deployment(access_token, subscription_id, rg_name, deployment_name):
    """Show details for a named deployment.abs

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        rg_name (str): Azure resource group name.

    Returns:
        HTTP response. JSON body.
    """
    endpoint = ''.join([get_rm_endpoint(),
     '/subscriptions/', subscription_id,
     '/resourcegroups/', rg_name,
     '/providers/microsoft.resources/deployments/', deployment_name,
     '?api-version=', BASE_API])
    return do_get(endpoint, access_token)