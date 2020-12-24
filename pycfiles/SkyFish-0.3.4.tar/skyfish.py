# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fauzan/coral/skyfish-py-sdk/skyfish/skyfish.py
# Compiled at: 2016-08-15 04:39:04
"""
    Skyfish
    ~~~~~

    Official python SDK for skyfish chat to buy inventory integration

    :copyright: (c) 2016 by PT Koneksi Integrasi.
    :license: MIT, see LICENSE for more details.
"""
__version__ = '0.3.0'
import json, requests
from .models import ProductData, Response, Config

class SkyFishSDK(object):

    def __init__(self, configuration, request_module=requests):
        if not configuration:
            raise AttributeError('`configuration` parameter is required')
        if type(configuration) is not Config:
            raise TypeError('The parameter configuration only accepts Config object')
        self.config = configuration
        self.request_module = request_module

    def _generate_product_headers(self):
        return {'User-Agent': 'SFE Python SDK v%s' % __version__, 
           'Content-Type': 'application/json', 
           'Accept': 'application/json', 
           'X-Passport-ID': self.config.passport_id, 
           'X-Passport-Email': self.config.email}

    def create_product(self, sku, product_details):
        url = '%s/v1/products/%s?token=%s&client_key=%s' % (
         self.config.base_url, sku, self.config.token, self.config.client_key)
        product = ProductData(product_details)
        new_product = self.request_module.post(url, headers=self._generate_product_headers(), json=product.to_dict())
        response = Response()
        if new_product.status_code == 201:
            response.data = Response.build_from_json(new_product.json().get('data'))
        response.status_code = new_product.status_code
        response.status = new_product.json().get('status')
        response.message = new_product.json().get('message')
        return response

    def get_product(self, sku):
        url = '%s/v1/products/%s/merchant?token=%s' % (
         self.config.base_url, sku, self.config.token)
        product = self.request_module.get(url, headers=self._generate_product_headers())
        response = Response()
        if product.status_code == 200:
            response.data = Response.build_from_json(product.json().get('data'))
        response.status_code = product.status_code
        response.status = product.json().get('status')
        response.message = product.json().get('message')
        return response

    def update_product(self, sku, product_details):
        url = '%s/v1/products/%s?token=%s&client_key=%s' % (
         self.config.base_url, sku, self.config.token, self.config.client_key)
        product = ProductData(product_details)
        updated_product = self.request_module.put(url, headers=self._generate_product_headers, json=product.to_dict())
        response = Response()
        if updated_product.status_code == 200:
            response.data = Response.build_from_json(updated_product.json().get('data'))
        response.status_code = updated_product.status_code
        response.status = updated_product.json().get('status')
        response.message = updated_product.json().get('message')
        return response

    def delete_product(self, sku):
        url = '%s/v1/products/%s?token=%s&client_key=%s' % (
         self.config.base_url, sku, self.config.token, self.config.client_key)
        product = self.request_module.delete(url, headers=self._generate_product_headers())
        response = Response()
        response.status_code = product.status_code
        response.data = product.json().get('data')
        response.status = product.json().get('status')
        response.message = product.json().get('message')
        return response

    @staticmethod
    def user_response_is_valid(response_dictionary):
        if type(response_dictionary) is not dict:
            raise TypeError('`response_dictionary` must be dict')
        expected_root = [
         'status', 'message', 'data']
        for item in response_dictionary.keys():
            if item not in expected_root:
                raise KeyError('`%s` is not expected to be in the response root' % item)

        if type(response_dictionary.get('data')) is not dict:
            raise TypeError('`data` should be dict')
        if 'user_id' not in response_dictionary.get('data').keys():
            raise KeyError('`user_id` field should be in the data fields')
        if type(response_dictionary.get('data').get('user_id')) is not str and type(response_dictionary.get('data').get('user_id')) is not unicode:
            raise TypeError('`user_id` value should be str or unicode')
        return True

    @staticmethod
    def stock_response_is_valid(response_dictionary):
        if type(response_dictionary) is not dict:
            raise TypeError('`response_dictionary` must be dict')
        expected_root = [
         'status', 'message', 'data']
        for item in response_dictionary.keys():
            if item not in expected_root:
                raise KeyError('`%s` is not expected to be in the response root' % item)

        if type(response_dictionary.get('data')) is not list:
            raise TypeError('`data` should be list')
        for item in response_dictionary.get('data'):
            expected_fields = [
             'product_sku', 'current_stock', 'is_available']
            for field in item.keys():
                if field not in expected_fields:
                    raise KeyError('`%s` is not expected to be in the data fields' % field)

            if type(item.get('product_sku')) is not str:
                raise TypeError('`product_sku` should be str')
            if type(item.get('current_stock')) is not int:
                raise TypeError('`current_stock` should be int')
            if type(item.get('is_available')) is not bool:
                raise TypeError('`is_available` should be bool')

        return True

    @staticmethod
    def transaction_response_is_valid(response_dictionary):
        if type(response_dictionary) is not dict:
            raise TypeError('`response_dictionary` must be dict')
        expected_root = [
         'status', 'message', 'data']
        for item in response_dictionary.keys():
            if item not in expected_root:
                raise KeyError('`%s` is not expected to be in the response root' % item)

        if type(response_dictionary.get('data')) is not dict:
            raise TypeError('`data` should be dict')
        return True