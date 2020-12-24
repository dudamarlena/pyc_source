# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/api/filters_api.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 9818 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
from __future__ import absolute_import
import re, six
from mux_python.api_client import ApiClient

class FiltersApi(object):

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def list_filter_values(self, filter_id, **kwargs):
        """Lists values for a specific filter  # noqa: E501

        Lists the values for a filter along with a total count of related views   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_filter_values(filter_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str filter_id: ID of the Filter (required)
        :param int limit: Number of items to include in the response
        :param int page: Offset by this many pages, of the size of `limit`
        :param list[str] filters: Filter key:value pairs. Must be provided as an array query string parameter (e.g. filters[]=operating_system:windows&filters[]=country:US).  Possible filter names are the same as returned by the List Filters endpoint. 
        :param list[str] timeframe: Timeframe window to limit results by. Must be provided as an array query string parameter (e.g. timeframe[]=). Accepted formats are...   * array of epoch timestamps e.g. timeframe[]=1498867200&timeframe[]=1498953600    * duration string e.g. timeframe[]=24:hours or timeframe[]=7:days. 
        :return: ListFilterValuesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.list_filter_values_with_http_info)(filter_id, **kwargs)
        data = (self.list_filter_values_with_http_info)(filter_id, **kwargs)
        return data

    def list_filter_values_with_http_info(self, filter_id, **kwargs):
        """Lists values for a specific filter  # noqa: E501

        Lists the values for a filter along with a total count of related views   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_filter_values_with_http_info(filter_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str filter_id: ID of the Filter (required)
        :param int limit: Number of items to include in the response
        :param int page: Offset by this many pages, of the size of `limit`
        :param list[str] filters: Filter key:value pairs. Must be provided as an array query string parameter (e.g. filters[]=operating_system:windows&filters[]=country:US).  Possible filter names are the same as returned by the List Filters endpoint. 
        :param list[str] timeframe: Timeframe window to limit results by. Must be provided as an array query string parameter (e.g. timeframe[]=). Accepted formats are...   * array of epoch timestamps e.g. timeframe[]=1498867200&timeframe[]=1498953600    * duration string e.g. timeframe[]=24:hours or timeframe[]=7:days. 
        :return: ListFilterValuesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'filter_id', 'limit', 'page', 'filters', 'timeframe']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method list_filter_values" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            if 'filter_id' not in local_var_params or local_var_params['filter_id'] is None:
                raise ValueError('Missing the required parameter `filter_id` when calling `list_filter_values`')
            collection_formats = {}
            path_params = {}
            if 'filter_id' in local_var_params:
                path_params['FILTER_ID'] = local_var_params['filter_id']
            query_params = []
            if 'limit' in local_var_params:
                query_params.append(('limit', local_var_params['limit']))
            if 'page' in local_var_params:
                query_params.append(('page', local_var_params['page']))
            if 'filters' in local_var_params:
                query_params.append(('filters[]', local_var_params['filters']))
                collection_formats['filters[]'] = 'multi'
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
            return self.api_client.call_api('/data/v1/filters/{FILTER_ID}',
              'GET', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='ListFilterValuesResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)

    def list_filters(self, **kwargs):
        """List Filters  # noqa: E501

        Lists all the filters broken out into basic and advanced   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_filters(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: ListFiltersResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.list_filters_with_http_info)(**kwargs)
        data = (self.list_filters_with_http_info)(**kwargs)
        return data

    def list_filters_with_http_info(self, **kwargs):
        """List Filters  # noqa: E501

        Lists all the filters broken out into basic and advanced   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_filters_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: ListFiltersResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = []
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method list_filters" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            collection_formats = {}
            path_params = {}
            query_params = []
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            header_params['Accept'] = self.api_client.select_header_accept([
             'application/json'])
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/data/v1/filters',
              'GET', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='ListFiltersResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)