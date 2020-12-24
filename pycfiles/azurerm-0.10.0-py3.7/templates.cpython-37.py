# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\azurerm\templates.py
# Compiled at: 2018-11-06 13:55:21
# Size of source mod 2**32: 4083 bytes
"""templates.py - azurerm functions for deploying templates"""
import json
from .restfns import do_put
from .settings import get_rm_endpoint, DEPLOYMENTS_API

def deploy_template(access_token, subscription_id, resource_group, deployment_name, template, parameters):
    """Deploy a template referenced by a JSON string, with parameters as a JSON string.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        deployment_name (str): A name you give to the deployment.
        template (str): String representatipn of a JSON template body.
        parameters (str): String representation of a JSON template parameters body.

    Returns:
        HTTP response.
    """
    endpoint = ''.join([get_rm_endpoint(),
     '/subscriptions/', subscription_id,
     '/resourcegroups/', resource_group,
     '/providers/Microsoft.Resources/deployments/', deployment_name,
     '?api-version=', DEPLOYMENTS_API])
    properties = {'template': template}
    properties['mode'] = 'Incremental'
    properties['parameters'] = parameters
    template_body = {'properties': properties}
    body = json.dumps(template_body)
    return do_put(endpoint, body, access_token)


def deploy_template_uri(access_token, subscription_id, resource_group, deployment_name, template_uri, parameters):
    """Deploy a template referenced by a URI, with parameters as a JSON string.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        deployment_name (str): A name you give to the deployment.
        template_uri (str): URI which points to a JSON template (e.g. github raw location).
        parameters (str): String representation of a JSON template parameters body.

    Returns:
        HTTP response.
    """
    endpoint = ''.join([get_rm_endpoint(),
     '/subscriptions/', subscription_id,
     '/resourcegroups/', resource_group,
     '/providers/Microsoft.Resources/deployments/', deployment_name,
     '?api-version=', DEPLOYMENTS_API])
    properties = {'templateLink': {'uri': template_uri}}
    properties['mode'] = 'Incremental'
    properties['parameters'] = parameters
    template_body = {'properties': properties}
    body = json.dumps(template_body)
    return do_put(endpoint, body, access_token)


def deploy_template_uri_param_uri(access_token, subscription_id, resource_group, deployment_name, template_uri, parameters_uri):
    """Deploy a template with both template and parameters referenced by URIs.

    Args:
        access_token (str): A valid Azure authentication token.
        subscription_id (str): Azure subscription id.
        resource_group (str): Azure resource group name.
        deployment_name (str): A name you give to the deployment.
        template_uri (str): URI which points to a JSON template (e.g. github raw location).
        parameters_uri (str): URI which points to a JSON parameters file (e.g. github raw location).

    Returns:
        HTTP response.
    """
    endpoint = ''.join([get_rm_endpoint(),
     '/subscriptions/', subscription_id,
     '/resourcegroups/', resource_group,
     '/providers/Microsoft.Resources/deployments/', deployment_name,
     '?api-version=', DEPLOYMENTS_API])
    properties = {'templateLink': {'uri': template_uri}}
    properties['mode'] = 'Incremental'
    properties['parametersLink'] = {'uri': parameters_uri}
    template_body = {'properties': properties}
    body = json.dumps(template_body)
    return do_put(endpoint, body, access_token)