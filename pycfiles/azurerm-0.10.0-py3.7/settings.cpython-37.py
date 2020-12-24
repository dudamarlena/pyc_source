# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\azurerm\settings.py
# Compiled at: 2019-05-01 13:41:42
# Size of source mod 2**32: 2386 bytes
"""settings.py - place to store constants for azurerm"""
import os
ams_auth_endpoint = 'https://wamsprodglobal001acs.accesscontrol.windows.net/v2/OAuth2-13'
ams_rest_endpoint = 'https://media.windows.net/API'
AZURE_RM_ENDPOINT = 'https://management.azure.com'
AZURE_AUTH_ENDPOINT = 'https://login.microsoftonline.com/'
AZURE_RESOURCE_ENDPOINT = 'https://management.core.windows.net/'
GRAPH_RESOURCE_HOST = 'graph.microsoft.com'
ACS_API = '2017-01-31'
BASE_API = '2016-06-01'
COMP_API = '2019-03-01'
CONTAINER_API = '2017-08-01-preview'
COSMOSDB_API = '2015-04-08'
DEPLOYMENTS_API = '2018-05-01'
INSIGHTS_API = '2015-04-01'
INSIGHTS_COMPONENTS_API = '2015-05-01'
INSIGHTS_METRICS_API = '2016-03-01'
INSIGHTS_PREVIEW_API = '2016-06-01'
KEYVAULT_API = '2018-02-14'
MEDIA_API = '2015-10-01'
NETWORK_API = '2018-08-01'
RESOURCE_API = '2017-05-10'
STORAGE_API = '2018-07-01'
json_only_acceptformat = 'application/json'
json_acceptformat = 'application/json;odata=verbose'
xml_acceptformat = 'application/atom+xml'
batch_acceptformat = 'multipart/mixed'
xmsversion = '2.13'
dsversion_min = '3.0;NetFx'
dsversion_max = '3.0;NetFx'
charset = 'UTF-8'

def get_rm_endpoint():
    """Set Azure Resource Manager endpoint by environment variable, else return default value.

    These functions facilitate the use of national and isolated clouds by allowing endpoints to
    be set dynamically. The default settings, if no environment varibles are used,
    are for public cloud.
    """
    rm_endpoint = os.environ.get('AZURE_RM_ENDPOINT')
    if rm_endpoint is None:
        return AZURE_RM_ENDPOINT
    return rm_endpoint


def get_auth_endpoint():
    """Set Azure auth endpoint by environment variable, else return default value.
    """
    auth_endpoint = os.environ.get('AZURE_AUTH_ENDPOINT')
    if auth_endpoint is None:
        return AZURE_AUTH_ENDPOINT
    return auth_endpoint


def get_resource_endpoint():
    """Set Azure reosurce endpoint by environment variable, else return default value.
    """
    resource_endpoint = os.environ.get('AZURE_RESOURCE_ENDPOINT')
    if resource_endpoint is None:
        return AZURE_RESOURCE_ENDPOINT
    return resource_endpoint