# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/api/delivery_usage_api.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 5536 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
from __future__ import absolute_import
import re, six
from mux_python.api_client import ApiClient

class DeliveryUsageApi(object):

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def list_delivery_usage(self, **kwargs):
        """List Usage  # noqa: E501

        Returns a list of delivery usage records and their associated Asset IDs or Live Stream IDs.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_delivery_usage(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page: Offset by this many pages, of the size of `limit`
        :param int limit: Number of items to include in the response
        :param str asset_id: Filter response to return delivery usage for this asset only.
        :param list[str] timeframe: Time window to get delivery usage information. timeframe[0] indicates the start time, timeframe[1] indicates the end time in seconds since the Unix epoch. Default time window is 1 hour representing usage from 13th to 12th hour from when the request is made. 
        :return: ListDeliveryUsageResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.list_delivery_usage_with_http_info)(**kwargs)
        data = (self.list_delivery_usage_with_http_info)(**kwargs)
        return data

    def list_delivery_usage_with_http_info(self, **kwargs):
        """List Usage  # noqa: E501

        Returns a list of delivery usage records and their associated Asset IDs or Live Stream IDs.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_delivery_usage_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page: Offset by this many pages, of the size of `limit`
        :param int limit: Number of items to include in the response
        :param str asset_id: Filter response to return delivery usage for this asset only.
        :param list[str] timeframe: Time window to get delivery usage information. timeframe[0] indicates the start time, timeframe[1] indicates the end time in seconds since the Unix epoch. Default time window is 1 hour representing usage from 13th to 12th hour from when the request is made. 
        :return: ListDeliveryUsageResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'page', 'limit', 'asset_id', 'timeframe']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method list_delivery_usage" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            collection_formats = {}
            path_params = {}
            query_params = []
            if 'page' in local_var_params:
                query_params.append(('page', local_var_params['page']))
            if 'limit' in local_var_params:
                query_params.append(('limit', local_var_params['limit']))
            if 'asset_id' in local_var_params:
                query_params.append(('asset_id', local_var_params['asset_id']))
            if 'timeframe' in local_var_params:
                query_params.append(('timeframe[]', local_var_params['timeframe']))
                collection_formats['timeframe[]'] = 'multi'
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            header_params['Accept'] = self.api_client.select_header_accept([
             'application/json'])
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/delivery-usage',
              'GET', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='ListDeliveryUsageResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)