# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mcazurerm\templates.py
# Compiled at: 2017-08-11 23:27:04
# Size of source mod 2**32: 3029 bytes
from .restfns import do_put
from .settings import azure_rm_endpoint, BASE_API

def deploy_template(access_token, subscription_id, resource_group, deployment_name, template, parameters):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourcegroups/', resource_group,
     '/providers/Microsoft.Resources/deployments/', deployment_name,
     '?api-version=', BASE_API])
    body = ''.join(['{   "properties": {     "template": ', template,
     ',     "mode": "Incremental",',
     '     "parameters": ', parameters,
     '}}'])
    return do_put(endpoint, body, access_token)


def deploy_template_uri(access_token, subscription_id, resource_group, deployment_name, template_uri, parameters):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourcegroups/', resource_group,
     '/providers/Microsoft.Resources/deployments/', deployment_name,
     '?api-version=', BASE_API])
    body = ''.join(['{   "properties": {     "templateLink": {       "uri": "', template_uri,
     '",       "contentVersion": "1.0.0.0"     },',
     '     "mode": "Incremental",',
     '     "parameters": ', parameters,
     '   } }'])
    return do_put(endpoint, body, access_token)


def deploy_template_uri_param_uri(access_token, subscription_id, resource_group, deployment_name, template_uri, parameters_uri):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourcegroups/', resource_group,
     '/providers/Microsoft.Resources/deployments/', deployment_name,
     '?api-version=', BASE_API])
    body = ''.join(['{   "properties": {     "templateLink": {       "uri": "', template_uri,
     '",       "contentVersion": "1.0.0.0"     },     "mode": "Incremental",     "parametersLink": {       "uri": "',
     parameters_uri, '",       "contentVersion": "1.0.0.0"           }   } }'])
    return do_put(endpoint, body, access_token)