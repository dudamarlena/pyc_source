# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/mux_python/api/assets_api.py
# Compiled at: 2020-03-11 08:26:48
# Size of source mod 2**32: 53662 bytes
"""
Mux Python - Copyright 2019 Mux Inc.

NOTE: This class is auto generated. Do not edit the class manually.
"""
from __future__ import absolute_import
import re, six
from mux_python.api_client import ApiClient

class AssetsApi(object):

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_asset(self, create_asset_request, **kwargs):
        """Create an asset  # noqa: E501

        Create a new Mux Video asset.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_asset(create_asset_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateAssetRequest create_asset_request: (required)
        :return: AssetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.create_asset_with_http_info)(create_asset_request, **kwargs)
        data = (self.create_asset_with_http_info)(create_asset_request, **kwargs)
        return data

    def create_asset_with_http_info(self, create_asset_request, **kwargs):
        """Create an asset  # noqa: E501

        Create a new Mux Video asset.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_asset_with_http_info(create_asset_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateAssetRequest create_asset_request: (required)
        :return: AssetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'create_asset_request']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method create_asset" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            if 'create_asset_request' not in local_var_params or local_var_params['create_asset_request'] is None:
                raise ValueError('Missing the required parameter `create_asset_request` when calling `create_asset`')
            collection_formats = {}
            path_params = {}
            query_params = []
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            if 'create_asset_request' in local_var_params:
                body_params = local_var_params['create_asset_request']
            header_params['Accept'] = self.api_client.select_header_accept([
             'application/json'])
            header_params['Content-Type'] = self.api_client.select_header_content_type([
             'application/json'])
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/assets',
              'POST', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='AssetResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)

    def create_asset_playback_id(self, asset_id, create_playback_id_request, **kwargs):
        """Create a playback ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_asset_playback_id(asset_id, create_playback_id_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :param CreatePlaybackIDRequest create_playback_id_request: (required)
        :return: CreatePlaybackIDResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.create_asset_playback_id_with_http_info)(asset_id, create_playback_id_request, **kwargs)
        data = (self.create_asset_playback_id_with_http_info)(asset_id, create_playback_id_request, **kwargs)
        return data

    def create_asset_playback_id_with_http_info(self, asset_id, create_playback_id_request, **kwargs):
        """Create a playback ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_asset_playback_id_with_http_info(asset_id, create_playback_id_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :param CreatePlaybackIDRequest create_playback_id_request: (required)
        :return: CreatePlaybackIDResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'asset_id', 'create_playback_id_request']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method create_asset_playback_id" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            if 'asset_id' not in local_var_params or local_var_params['asset_id'] is None:
                raise ValueError('Missing the required parameter `asset_id` when calling `create_asset_playback_id`')
            if 'create_playback_id_request' not in local_var_params or local_var_params['create_playback_id_request'] is None:
                raise ValueError('Missing the required parameter `create_playback_id_request` when calling `create_asset_playback_id`')
            collection_formats = {}
            path_params = {}
            if 'asset_id' in local_var_params:
                path_params['ASSET_ID'] = local_var_params['asset_id']
            query_params = []
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            if 'create_playback_id_request' in local_var_params:
                body_params = local_var_params['create_playback_id_request']
            header_params['Accept'] = self.api_client.select_header_accept([
             'application/json'])
            header_params['Content-Type'] = self.api_client.select_header_content_type([
             'application/json'])
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/assets/{ASSET_ID}/playback-ids',
              'POST', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='CreatePlaybackIDResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)

    def create_asset_track(self, asset_id, create_track_request, **kwargs):
        """Create an asset track  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_asset_track(asset_id, create_track_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :param CreateTrackRequest create_track_request: (required)
        :return: CreateTrackResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.create_asset_track_with_http_info)(asset_id, create_track_request, **kwargs)
        data = (self.create_asset_track_with_http_info)(asset_id, create_track_request, **kwargs)
        return data

    def create_asset_track_with_http_info(self, asset_id, create_track_request, **kwargs):
        """Create an asset track  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_asset_track_with_http_info(asset_id, create_track_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :param CreateTrackRequest create_track_request: (required)
        :return: CreateTrackResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'asset_id', 'create_track_request']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method create_asset_track" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            if 'asset_id' not in local_var_params or local_var_params['asset_id'] is None:
                raise ValueError('Missing the required parameter `asset_id` when calling `create_asset_track`')
            if 'create_track_request' not in local_var_params or local_var_params['create_track_request'] is None:
                raise ValueError('Missing the required parameter `create_track_request` when calling `create_asset_track`')
            collection_formats = {}
            path_params = {}
            if 'asset_id' in local_var_params:
                path_params['ASSET_ID'] = local_var_params['asset_id']
            query_params = []
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            if 'create_track_request' in local_var_params:
                body_params = local_var_params['create_track_request']
            header_params['Accept'] = self.api_client.select_header_accept([
             'application/json'])
            header_params['Content-Type'] = self.api_client.select_header_content_type([
             'application/json'])
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/assets/{ASSET_ID}/tracks',
              'POST', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='CreateTrackResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)

    def delete_asset(self, asset_id, **kwargs):
        """Delete an asset  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_asset(asset_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.delete_asset_with_http_info)(asset_id, **kwargs)
        data = (self.delete_asset_with_http_info)(asset_id, **kwargs)
        return data

    def delete_asset_with_http_info(self, asset_id, **kwargs):
        """Delete an asset  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_asset_with_http_info(asset_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'asset_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method delete_asset" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            if 'asset_id' not in local_var_params or local_var_params['asset_id'] is None:
                raise ValueError('Missing the required parameter `asset_id` when calling `delete_asset`')
            collection_formats = {}
            path_params = {}
            if 'asset_id' in local_var_params:
                path_params['ASSET_ID'] = local_var_params['asset_id']
            query_params = []
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/assets/{ASSET_ID}',
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

    def delete_asset_playback_id(self, asset_id, playback_id, **kwargs):
        """Delete a playback ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_asset_playback_id(asset_id, playback_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :param str playback_id: The live stream's playback ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.delete_asset_playback_id_with_http_info)(asset_id, playback_id, **kwargs)
        data = (self.delete_asset_playback_id_with_http_info)(asset_id, playback_id, **kwargs)
        return data

    def delete_asset_playback_id_with_http_info(self, asset_id, playback_id, **kwargs):
        """Delete a playback ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_asset_playback_id_with_http_info(asset_id, playback_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :param str playback_id: The live stream's playback ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'asset_id', 'playback_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method delete_asset_playback_id" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            if 'asset_id' not in local_var_params or local_var_params['asset_id'] is None:
                raise ValueError('Missing the required parameter `asset_id` when calling `delete_asset_playback_id`')
            if 'playback_id' not in local_var_params or local_var_params['playback_id'] is None:
                raise ValueError('Missing the required parameter `playback_id` when calling `delete_asset_playback_id`')
            collection_formats = {}
            path_params = {}
            if 'asset_id' in local_var_params:
                path_params['ASSET_ID'] = local_var_params['asset_id']
            if 'playback_id' in local_var_params:
                path_params['PLAYBACK_ID'] = local_var_params['playback_id']
            query_params = []
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/assets/{ASSET_ID}/playback-ids/{PLAYBACK_ID}',
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

    def delete_asset_track(self, asset_id, track_id, **kwargs):
        """Delete an asset track  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_asset_track(asset_id, track_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :param str track_id: The track ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.delete_asset_track_with_http_info)(asset_id, track_id, **kwargs)
        data = (self.delete_asset_track_with_http_info)(asset_id, track_id, **kwargs)
        return data

    def delete_asset_track_with_http_info(self, asset_id, track_id, **kwargs):
        """Delete an asset track  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_asset_track_with_http_info(asset_id, track_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :param str track_id: The track ID. (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'asset_id', 'track_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method delete_asset_track" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            if 'asset_id' not in local_var_params or local_var_params['asset_id'] is None:
                raise ValueError('Missing the required parameter `asset_id` when calling `delete_asset_track`')
            if 'track_id' not in local_var_params or local_var_params['track_id'] is None:
                raise ValueError('Missing the required parameter `track_id` when calling `delete_asset_track`')
            collection_formats = {}
            path_params = {}
            if 'asset_id' in local_var_params:
                path_params['ASSET_ID'] = local_var_params['asset_id']
            if 'track_id' in local_var_params:
                path_params['TRACK_ID'] = local_var_params['track_id']
            query_params = []
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/assets/{ASSET_ID}/tracks/{TRACK_ID}',
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

    def get_asset(self, asset_id, **kwargs):
        """Retrieve an asset  # noqa: E501

        Retrieves the details of an asset that has previously been created. Supply the unique asset ID that was returned from your previous request, and Mux will return the corresponding asset information. The same information is returned when creating an asset.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_asset(asset_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :return: AssetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.get_asset_with_http_info)(asset_id, **kwargs)
        data = (self.get_asset_with_http_info)(asset_id, **kwargs)
        return data

    def get_asset_with_http_info(self, asset_id, **kwargs):
        """Retrieve an asset  # noqa: E501

        Retrieves the details of an asset that has previously been created. Supply the unique asset ID that was returned from your previous request, and Mux will return the corresponding asset information. The same information is returned when creating an asset.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_asset_with_http_info(asset_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :return: AssetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'asset_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method get_asset" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            if 'asset_id' not in local_var_params or local_var_params['asset_id'] is None:
                raise ValueError('Missing the required parameter `asset_id` when calling `get_asset`')
            collection_formats = {}
            path_params = {}
            if 'asset_id' in local_var_params:
                path_params['ASSET_ID'] = local_var_params['asset_id']
            query_params = []
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            header_params['Accept'] = self.api_client.select_header_accept([
             'application/json'])
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/assets/{ASSET_ID}',
              'GET', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='AssetResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)

    def get_asset_input_info(self, asset_id, **kwargs):
        """Retrieve asset input info  # noqa: E501

        Returns a list of the input objects that were used to create the asset along with any settings that were applied to each input.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_asset_input_info(asset_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :return: GetAssetInputInfoResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.get_asset_input_info_with_http_info)(asset_id, **kwargs)
        data = (self.get_asset_input_info_with_http_info)(asset_id, **kwargs)
        return data

    def get_asset_input_info_with_http_info(self, asset_id, **kwargs):
        """Retrieve asset input info  # noqa: E501

        Returns a list of the input objects that were used to create the asset along with any settings that were applied to each input.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_asset_input_info_with_http_info(asset_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :return: GetAssetInputInfoResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'asset_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method get_asset_input_info" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            if 'asset_id' not in local_var_params or local_var_params['asset_id'] is None:
                raise ValueError('Missing the required parameter `asset_id` when calling `get_asset_input_info`')
            collection_formats = {}
            path_params = {}
            if 'asset_id' in local_var_params:
                path_params['ASSET_ID'] = local_var_params['asset_id']
            query_params = []
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            header_params['Accept'] = self.api_client.select_header_accept([
             'application/json'])
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/assets/{ASSET_ID}/input-info',
              'GET', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='GetAssetInputInfoResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)

    def get_asset_playback_id(self, asset_id, playback_id, **kwargs):
        """Retrieve a playback ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_asset_playback_id(asset_id, playback_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :param str playback_id: The live stream's playback ID. (required)
        :return: GetAssetPlaybackIDResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.get_asset_playback_id_with_http_info)(asset_id, playback_id, **kwargs)
        data = (self.get_asset_playback_id_with_http_info)(asset_id, playback_id, **kwargs)
        return data

    def get_asset_playback_id_with_http_info(self, asset_id, playback_id, **kwargs):
        """Retrieve a playback ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_asset_playback_id_with_http_info(asset_id, playback_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :param str playback_id: The live stream's playback ID. (required)
        :return: GetAssetPlaybackIDResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'asset_id', 'playback_id']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method get_asset_playback_id" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            if 'asset_id' not in local_var_params or local_var_params['asset_id'] is None:
                raise ValueError('Missing the required parameter `asset_id` when calling `get_asset_playback_id`')
            if 'playback_id' not in local_var_params or local_var_params['playback_id'] is None:
                raise ValueError('Missing the required parameter `playback_id` when calling `get_asset_playback_id`')
            collection_formats = {}
            path_params = {}
            if 'asset_id' in local_var_params:
                path_params['ASSET_ID'] = local_var_params['asset_id']
            if 'playback_id' in local_var_params:
                path_params['PLAYBACK_ID'] = local_var_params['playback_id']
            query_params = []
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            header_params['Accept'] = self.api_client.select_header_accept([
             'application/json'])
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/assets/{ASSET_ID}/playback-ids/{PLAYBACK_ID}',
              'GET', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='GetAssetPlaybackIDResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)

    def list_assets(self, **kwargs):
        """List assets  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_assets(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int limit: Number of items to include in the response
        :param int page: Offset by this many pages, of the size of `limit`
        :return: ListAssetsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.list_assets_with_http_info)(**kwargs)
        data = (self.list_assets_with_http_info)(**kwargs)
        return data

    def list_assets_with_http_info(self, **kwargs):
        """List assets  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_assets_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int limit: Number of items to include in the response
        :param int page: Offset by this many pages, of the size of `limit`
        :return: ListAssetsResponse
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
                raise TypeError("Got an unexpected keyword argument '%s' to method list_assets" % key)
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
            return self.api_client.call_api('/video/v1/assets',
              'GET', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='ListAssetsResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)

    def update_asset_master_access(self, asset_id, update_asset_master_access_request, **kwargs):
        """Update master access  # noqa: E501

        Allows you add temporary access to the master (highest-quality) version of the asset in MP4 format. A URL will be created that can be used to download the master version for 24 hours. After 24 hours Master Access will revert to "none". This master version is not optimized for web and not meant to be streamed, only downloaded for purposes like archiving or editing the video offline.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_asset_master_access(asset_id, update_asset_master_access_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :param UpdateAssetMasterAccessRequest update_asset_master_access_request: (required)
        :return: AssetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.update_asset_master_access_with_http_info)(asset_id, update_asset_master_access_request, **kwargs)
        data = (self.update_asset_master_access_with_http_info)(asset_id, update_asset_master_access_request, **kwargs)
        return data

    def update_asset_master_access_with_http_info(self, asset_id, update_asset_master_access_request, **kwargs):
        """Update master access  # noqa: E501

        Allows you add temporary access to the master (highest-quality) version of the asset in MP4 format. A URL will be created that can be used to download the master version for 24 hours. After 24 hours Master Access will revert to "none". This master version is not optimized for web and not meant to be streamed, only downloaded for purposes like archiving or editing the video offline.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_asset_master_access_with_http_info(asset_id, update_asset_master_access_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :param UpdateAssetMasterAccessRequest update_asset_master_access_request: (required)
        :return: AssetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'asset_id', 'update_asset_master_access_request']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method update_asset_master_access" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            if 'asset_id' not in local_var_params or local_var_params['asset_id'] is None:
                raise ValueError('Missing the required parameter `asset_id` when calling `update_asset_master_access`')
            if 'update_asset_master_access_request' not in local_var_params or local_var_params['update_asset_master_access_request'] is None:
                raise ValueError('Missing the required parameter `update_asset_master_access_request` when calling `update_asset_master_access`')
            collection_formats = {}
            path_params = {}
            if 'asset_id' in local_var_params:
                path_params['ASSET_ID'] = local_var_params['asset_id']
            query_params = []
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            if 'update_asset_master_access_request' in local_var_params:
                body_params = local_var_params['update_asset_master_access_request']
            header_params['Accept'] = self.api_client.select_header_accept([
             'application/json'])
            header_params['Content-Type'] = self.api_client.select_header_content_type([
             'application/json'])
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/assets/{ASSET_ID}/master-access',
              'PUT', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='AssetResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)

    def update_asset_mp4_support(self, asset_id, update_asset_mp4_support_request, **kwargs):
        """Update MP4 support  # noqa: E501

        Allows you add or remove mp4 support for assets that were created without it. Currently there are two values supported in this request, `standard` and `none`. `none` means that an asset *does not* have mp4 support, so submitting a request with `mp4_support` set to `none` will delete the mp4 assets from the asset in question.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_asset_mp4_support(asset_id, update_asset_mp4_support_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :param UpdateAssetMP4SupportRequest update_asset_mp4_support_request: (required)
        :return: AssetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return (self.update_asset_mp4_support_with_http_info)(asset_id, update_asset_mp4_support_request, **kwargs)
        data = (self.update_asset_mp4_support_with_http_info)(asset_id, update_asset_mp4_support_request, **kwargs)
        return data

    def update_asset_mp4_support_with_http_info(self, asset_id, update_asset_mp4_support_request, **kwargs):
        """Update MP4 support  # noqa: E501

        Allows you add or remove mp4 support for assets that were created without it. Currently there are two values supported in this request, `standard` and `none`. `none` means that an asset *does not* have mp4 support, so submitting a request with `mp4_support` set to `none` will delete the mp4 assets from the asset in question.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_asset_mp4_support_with_http_info(asset_id, update_asset_mp4_support_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str asset_id: The asset ID. (required)
        :param UpdateAssetMP4SupportRequest update_asset_mp4_support_request: (required)
        :return: AssetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()
        all_params = [
         'asset_id', 'update_asset_mp4_support_request']
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method update_asset_mp4_support" % key)
            local_var_params[key] = val
        else:
            del local_var_params['kwargs']
            if 'asset_id' not in local_var_params or local_var_params['asset_id'] is None:
                raise ValueError('Missing the required parameter `asset_id` when calling `update_asset_mp4_support`')
            if 'update_asset_mp4_support_request' not in local_var_params or local_var_params['update_asset_mp4_support_request'] is None:
                raise ValueError('Missing the required parameter `update_asset_mp4_support_request` when calling `update_asset_mp4_support`')
            collection_formats = {}
            path_params = {}
            if 'asset_id' in local_var_params:
                path_params['ASSET_ID'] = local_var_params['asset_id']
            query_params = []
            header_params = {}
            form_params = []
            local_var_files = {}
            body_params = None
            if 'update_asset_mp4_support_request' in local_var_params:
                body_params = local_var_params['update_asset_mp4_support_request']
            header_params['Accept'] = self.api_client.select_header_accept([
             'application/json'])
            header_params['Content-Type'] = self.api_client.select_header_content_type([
             'application/json'])
            auth_settings = [
             'accessToken']
            return self.api_client.call_api('/video/v1/assets/{ASSET_ID}/mp4-support',
              'PUT', path_params,
              query_params,
              header_params,
              body=body_params,
              post_params=form_params,
              files=local_var_files,
              response_type='AssetResponse',
              auth_settings=auth_settings,
              async_req=(local_var_params.get('async_req')),
              _return_http_data_only=(local_var_params.get('_return_http_data_only')),
              _preload_content=(local_var_params.get('_preload_content', True)),
              _request_timeout=(local_var_params.get('_request_timeout')),
              collection_formats=collection_formats)