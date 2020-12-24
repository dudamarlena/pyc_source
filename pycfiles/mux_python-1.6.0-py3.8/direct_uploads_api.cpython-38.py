# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/api/direct_uploads_api.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 16232 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
from __future__ import absolute_import
import re, six
from mux_python.api_client import ApiClient

class DirectUploadsApi(object):

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def cancel_direct_upload(self, upload_id, **kwargs):
        """Cancel a direct upload  # noqa: E501

        Cancels a direct upload and marks it as cancelled. If a pending upload finishes after this request, no asset will be created. This request will only succeed if the upload is still in the `waiting` state.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.cancel_direct_upload(upload_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str upload_id: ID of the Upload (required)
        :return: UploadResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.cancel_direct_upload_with_http_info)(upload_id, **kwargs)
        data = (self.cancel_direct_upload_with_http_info)(upload_id, **kwargs)
        return data

    def cancel_direct_upload_with_http_info(self, upload_id, **kwargs):
        """Cancel a direct upload  # noqa: E501

        Cancels a direct upload and marks it as cancelled. If a pending upload finishes after this request, no asset will be created. This request will only succeed if the upload is still in the `waiting` state.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.cancel_direct_upload_with_http_info(upload_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str upload_id: ID of the Upload (required)
        :return: UploadResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'upload_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method cancel_direct_upload" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            if 'upload_id' not in local_var_params or local_var_params['upload_id'] is None:
                raise ValueError('Missing the required parameter `upload_id` when calling `cancel_direct_upload`')
            collection_formats = {}
            path_params = {}
            if 'upload_id' in local_var_params:
                path_params['UPLOAD_ID'] = local_var_params['upload_id']
            query_params = []
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            header_params['Accept'] = self.api_client.select_header_accept([
             'application/json'])
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/uploads/{UPLOAD_ID}/cancel',
              'PUT', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='UploadResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)

    def create_direct_upload(self, create_upload_request, **kwargs):
        """Create a new direct upload URL  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_direct_upload(create_upload_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateUploadRequest create_upload_request: (required)
        :return: UploadResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.create_direct_upload_with_http_info)(create_upload_request, **kwargs)
        data = (self.create_direct_upload_with_http_info)(create_upload_request, **kwargs)
        return data

    def create_direct_upload_with_http_info(self, create_upload_request, **kwargs):
        """Create a new direct upload URL  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_direct_upload_with_http_info(create_upload_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateUploadRequest create_upload_request: (required)
        :return: UploadResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'create_upload_request']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method create_direct_upload" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            if 'create_upload_request' not in local_var_params or local_var_params['create_upload_request'] is None:
                raise ValueError('Missing the required parameter `create_upload_request` when calling `create_direct_upload`')
            collection_formats = {}
            path_params = {}
            query_params = []
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            if 'create_upload_request' in local_var_params:
                body_params = local_var_params['create_upload_request']
            header_params['Accept'] = self.api_client.select_header_accept([
             'application/json'])
            header_params['Content-Type'] = self.api_client.select_header_content_type([
             'application/json'])
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/uploads',
              'POST', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='UploadResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)

    def get_direct_upload(self, upload_id, **kwargs):
        """Retrieve a single direct upload's info  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_direct_upload(upload_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str upload_id: ID of the Upload (required)
        :return: UploadResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.get_direct_upload_with_http_info)(upload_id, **kwargs)
        data = (self.get_direct_upload_with_http_info)(upload_id, **kwargs)
        return data

    def get_direct_upload_with_http_info(self, upload_id, **kwargs):
        """Retrieve a single direct upload's info  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_direct_upload_with_http_info(upload_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str upload_id: ID of the Upload (required)
        :return: UploadResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'upload_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method get_direct_upload" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            if 'upload_id' not in local_var_params or local_var_params['upload_id'] is None:
                raise ValueError('Missing the required parameter `upload_id` when calling `get_direct_upload`')
            collection_formats = {}
            path_params = {}
            if 'upload_id' in local_var_params:
                path_params['UPLOAD_ID'] = local_var_params['upload_id']
            query_params = []
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            header_params['Accept'] = self.api_client.select_header_accept([
             'application/json'])
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/uploads/{UPLOAD_ID}',
              'GET', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='UploadResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)

    def list_direct_uploads(self, **kwargs):
        """List direct uploads  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_direct_uploads(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int limit: Number of items to include in the response
        :param int page: Offset by this many pages, of the size of `limit`
        :return: ListUploadsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.list_direct_uploads_with_http_info)(**kwargs)
        data = (self.list_direct_uploads_with_http_info)(**kwargs)
        return data

    def list_direct_uploads_with_http_info(self, **kwargs):
        """List direct uploads  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_direct_uploads_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int limit: Number of items to include in the response
        :param int page: Offset by this many pages, of the size of `limit`
        :return: ListUploadsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'limit', 'page']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method list_direct_uploads" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            collection_formats = {}
            path_params = {}
            query_params = []
            if 'limit' in local_var_params:
                query_params.append(('limit', local_var_params['limit']))
            if 'page' in local_var_params:
                query_params.append(('page', local_var_params['page']))
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            header_params['Accept'] = self.api_client.select_header_accept([
             'application/json'])
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/uploads',
              'GET', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='ListUploadsResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)