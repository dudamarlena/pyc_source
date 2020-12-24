# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/api/url_signing_keys_api.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 16489 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
from __future__ import absolute_import
import re, six
from mux_python.api_client import ApiClient

class URLSigningKeysApi(object):

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_url_signing_key(self, **kwargs):
        """Create a URL signing key  # noqa: E501

        Creates a new signing key pair. When creating a new signing key, the API will generate a 2048-bit RSA key-pair and return the private key and a generated key-id; the public key will be stored at Mux to validate signed tokens.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_url_signing_key(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: SigningKeyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.create_url_signing_key_with_http_info)(**kwargs)
        data = (self.create_url_signing_key_with_http_info)(**kwargs)
        return data

    def create_url_signing_key_with_http_info(self, **kwargs):
        """Create a URL signing key  # noqa: E501

        Creates a new signing key pair. When creating a new signing key, the API will generate a 2048-bit RSA key-pair and return the private key and a generated key-id; the public key will be stored at Mux to validate signed tokens.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_url_signing_key_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: SigningKeyResponse
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
                raise TypeError("Got an unexpected keyword argument '%s' to method create_url_signing_key" % key)
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
            return self.api_client.call_api('/video/v1/signing-keys',
              'POST', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='SigningKeyResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)

    def delete_url_signing_key(self, signing_key_id, **kwargs):
        """Delete a URL signing key  # noqa: E501

        Deletes an existing signing key. Use with caution, as this will invalidate any existing signatures and no URLs can be signed using the key again.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_url_signing_key(signing_key_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str signing_key_id: The ID of the signing key. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.delete_url_signing_key_with_http_info)(signing_key_id, **kwargs)
        data = (self.delete_url_signing_key_with_http_info)(signing_key_id, **kwargs)
        return data

    def delete_url_signing_key_with_http_info(self, signing_key_id, **kwargs):
        """Delete a URL signing key  # noqa: E501

        Deletes an existing signing key. Use with caution, as this will invalidate any existing signatures and no URLs can be signed using the key again.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_url_signing_key_with_http_info(signing_key_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str signing_key_id: The ID of the signing key. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'signing_key_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method delete_url_signing_key" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            if 'signing_key_id' not in local_var_params or local_var_params['signing_key_id'] is None:
                raise ValueError('Missing the required parameter `signing_key_id` when calling `delete_url_signing_key`')
            collection_formats = {}
            path_params = {}
            if 'signing_key_id' in local_var_params:
                path_params['SIGNING_KEY_ID'] = local_var_params['signing_key_id']
            query_params = []
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/signing-keys/{SIGNING_KEY_ID}',
              'DELETE', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type=None,
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)

    def get_url_signing_key(self, signing_key_id, **kwargs):
        """Retrieve a URL signing key  # noqa: E501

        Retrieves the details of a URL signing key that has previously been created. Supply the unique signing key ID that was returned from your previous request, and Mux will return the corresponding signing key information. **The private key is not returned in this response.**   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_url_signing_key(signing_key_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str signing_key_id: The ID of the signing key. (required)
        :return: SigningKeyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.get_url_signing_key_with_http_info)(signing_key_id, **kwargs)
        data = (self.get_url_signing_key_with_http_info)(signing_key_id, **kwargs)
        return data

    def get_url_signing_key_with_http_info(self, signing_key_id, **kwargs):
        """Retrieve a URL signing key  # noqa: E501

        Retrieves the details of a URL signing key that has previously been created. Supply the unique signing key ID that was returned from your previous request, and Mux will return the corresponding signing key information. **The private key is not returned in this response.**   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_url_signing_key_with_http_info(signing_key_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str signing_key_id: The ID of the signing key. (required)
        :return: SigningKeyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'signing_key_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method get_url_signing_key" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            if 'signing_key_id' not in local_var_params or local_var_params['signing_key_id'] is None:
                raise ValueError('Missing the required parameter `signing_key_id` when calling `get_url_signing_key`')
            collection_formats = {}
            path_params = {}
            if 'signing_key_id' in local_var_params:
                path_params['SIGNING_KEY_ID'] = local_var_params['signing_key_id']
            query_params = []
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            header_params['Accept'] = self.api_client.select_header_accept([
             'application/json'])
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/signing-keys/{SIGNING_KEY_ID}',
              'GET', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='SigningKeyResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)

    def list_url_signing_keys(self, **kwargs):
        """List URL signing keys  # noqa: E501

        Returns a list of URL signing keys.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_url_signing_keys(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int limit: Number of items to include in the response
        :param int page: Offset by this many pages, of the size of `limit`
        :return: ListSigningKeysResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.list_url_signing_keys_with_http_info)(**kwargs)
        data = (self.list_url_signing_keys_with_http_info)(**kwargs)
        return data

    def list_url_signing_keys_with_http_info(self, **kwargs):
        """List URL signing keys  # noqa: E501

        Returns a list of URL signing keys.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_url_signing_keys_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int limit: Number of items to include in the response
        :param int page: Offset by this many pages, of the size of `limit`
        :return: ListSigningKeysResponse
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
                raise TypeError("Got an unexpected keyword argument '%s' to method list_url_signing_keys" % key)
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
            return self.api_client.call_api('/video/v1/signing-keys',
              'GET', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='ListSigningKeysResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)