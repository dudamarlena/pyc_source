# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/conda/lib/python3.7/site-packages/smoothnlp_api/api/investment_api.py
# Compiled at: 2019-09-17 09:18:30
# Size of source mod 2**32: 4307 bytes
"""
    Investment

    * 默认域名： service-m5j3awiv-1259459016.ap-shanghai.apigateway.myqcloud.com/release * 自定义域名： data.service.invest.smoothnlp.com/   # noqa: E501
"""
from __future__ import absolute_import
import six
from smoothnlp_api.api_client import ApiClient
import smoothnlp_api
from smoothnlp_api import getSimpleSign
HOST = 'http://data.service.invest.smoothnlp.com/'

class InvestmentApi(object):

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_investment(self, **kwargs):
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return (self.get_investment_with_http_info)(**kwargs)
        data = (self.get_investment_with_http_info)(**kwargs)
        data = eval(data)
        return data

    def get_investment_with_http_info(self, **kwargs):
        all_params = [
         'cate1', 'cate2', 'company_name', 'product_name', 'year']
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')
        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method get_investment" % key)
            params[key] = val

        del params['kwargs']
        collection_formats = {}
        path_params = {}
        query_params = []
        if 'cate1' in params:
            query_params.append(('cate1', params['cate1']))
        if 'cate2' in params:
            query_params.append(('cate2', params['cate2']))
        if 'company_name' in params:
            query_params.append(('company_name', params['company_name']))
        if 'product_name' in params:
            query_params.append(('product_name', params['product_name']))
        if 'year' in params:
            query_params.append(('year', params['year']))
        header_params = {}
        form_params = []
        local_var_files = {}
        body_params = None
        header_params['Accept'] = self.api_client.select_header_accept([
         'HTML'])
        header_params['Content-Type'] = self.api_client.select_header_content_type([
         'application/json'])
        auth_settings = []
        Source = 'AndriodApp'
        sign, dateTime = getSimpleSign(Source, smoothnlp_api.config.SECRET_ID, smoothnlp_api.config.SECRET_KEY)
        header_params['Date'] = dateTime
        header_params['Authorization'] = sign
        header_params['Source'] = Source
        return self.api_client.call_api(HOST,
          '/investment',
          'GET',
          path_params,
          query_params,
          header_params,
          body=body_params,
          post_params=form_params,
          files=local_var_files,
          response_type='str',
          auth_settings=auth_settings,
          _async=(params.get('async')),
          _return_http_data_only=(params.get('_return_http_data_only')),
          _preload_content=(params.get('_preload_content', True)),
          _request_timeout=(params.get('_request_timeout')),
          collection_formats=collection_formats)