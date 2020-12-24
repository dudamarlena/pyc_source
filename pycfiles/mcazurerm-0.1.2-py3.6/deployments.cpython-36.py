# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mcazurerm\deployments.py
# Compiled at: 2017-08-11 23:27:04
# Size of source mod 2**32: 1184 bytes
from .restfns import do_get
from .settings import azure_rm_endpoint, BASE_API

def list_deployment_operations(access_token, subscription_id, rg_name, deployment_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourcegroups/', rg_name,
     '/providers/Microsoft.Resources/deployments/', deployment_name,
     '/operations',
     '?api-version=', BASE_API])
    return do_get(endpoint, access_token)


def show_deployment(access_token, subscription_id, rg_name, deployment_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourcegroups/', rg_name,
     '/providers/microsoft.resources/deployments/', deployment_name,
     '?api-version=', BASE_API])
    return do_get(endpoint, access_token)