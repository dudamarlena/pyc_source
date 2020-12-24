# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sfws/sfws.py
# Compiled at: 2020-05-06 13:25:20
# Size of source mod 2**32: 3433 bytes
import json, sys
from .client import Client
from .catalogs import Catalogs
from .products import Products
from .orders import Orders

class Service:
    client = None
    catalogs = None
    api_credentials = None

    def start_client(self, api_credentials, api_service='data_api'):
        self.client = Client(api_credentials)
        self.client.api_service = api_service
        self.api_credentials = api_credentials
        self.catalogs = Catalogs()
        self.catalogs.set_client(self.client)
        self.products = Products()
        self.products.set_client(self.client)
        self.orders = Orders()
        self.orders.set_client(self.client)

    def connect(self):
        if self.client:
            ocapi_response = self.client.do_OAuth()
            if 'access_token' in ocapi_response:
                self.response = {'state':'ok', 
                 'message':'connected',  'ocapi_response':ocapi_response}
            else:
                self.response = {'state':'fail', 
                 'message':ocapi_response['error_description'],  'ocapi_response':ocapi_response}
        return self.response

    def get_catalogs(self, access_token, params, order=None):
        return self.catalogs.get_catalogs(access_token, params, order)

    def get_catalog_categories(self, access_token, params, order=None):
        return self.catalogs.get_catalog_categories(access_token, params, order)

    def product_search(self, access_token, fields, phrase, order=None):
        return self.products.product_search(access_token, fields, phrase, order)

    def update_product_inventory_record(self, access_token, params):
        return self.products.update_product_inventory_record(access_token, params)

    def get_product_inventory_record(self, access_token, params):
        return self.products.get_product_inventory_record(access_token, params)

    def update_products_price(self, access_token, customs_objects):
        return self.products.update_products_price(access_token, customs_objects)

    def cron_run_osf_cron(self, access_token, execution):
        return self.products.cron_run_osf_cron(access_token, execution)

    def cron_get_osf_job_status(self, access_token, execution, job_id):
        return self.products.cron_get_osf_job_status(access_token, execution, job_id)

    def cron_replicate_stage_to_production(self, access_token, replication):
        return self.products.cron_replicate_stage_to_production(access_token, replication)

    def get_product(self, access_token, _id):
        return self.products.get_product(access_token, _id)

    def shop_product_search(self, access_token, fields, phrase, api, order=None):
        return self.products.shop_product_search(access_token, fields, phrase, api, order)

    def shop_product_search_prices(self, access_token, fields, phrase, api, order=None):
        return self.products.shop_product_search_prices(access_token, fields, phrase, api, order)

    def shop_orders_search(self, access_token, fields, phrase, api, order=None):
        return self.orders.shop_orders_search(access_token, fields, phrase, api, order)

    def shop_update_order_status(self, access_token, order_id, new_status, api):
        return self.orders.shop_update_order_status(access_token, order_id, new_status, api)