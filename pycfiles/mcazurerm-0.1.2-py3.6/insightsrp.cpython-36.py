# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mcazurerm\insightsrp.py
# Compiled at: 2017-08-11 23:27:04
# Size of source mod 2**32: 2816 bytes
from .restfns import do_get
from .settings import azure_rm_endpoint, INSIGHTS_API, INSIGHTS_PREVIEW_API

def list_autoscale_settings(access_token, subscription_id):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/providers/microsoft.insights/',
     '/autoscaleSettings?api-version=', INSIGHTS_API])
    return do_get(endpoint, access_token)


def list_insights_components(access_token, subscription_id, resource_group):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/microsoft.insights/',
     '/components?api-version=', INSIGHTS_API])
    return do_get(endpoint, access_token)


def list_metric_definitions_for_resource(access_token, subscription_id, resource_group, resource_provider, resource_type, resource_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/', resource_provider,
     '/', resource_type,
     '/', resource_name,
     '/providers/microsoft.insights',
     '/metricdefinitions?api-version=', INSIGHTS_API])
    return do_get(endpoint, access_token)


def get_metrics_for_resource(access_token, subscription_id, resource_group, resource_provider, resource_type, resource_name):
    endpoint = ''.join([azure_rm_endpoint,
     '/subscriptions/', subscription_id,
     '/resourceGroups/', resource_group,
     '/providers/', resource_provider,
     '/', resource_type,
     '/', resource_name,
     '/providers/microsoft.insights/',
     '/metrics?api-version=', INSIGHTS_PREVIEW_API])
    return do_get(endpoint, access_token)