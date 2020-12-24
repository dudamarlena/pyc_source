# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sfws/orders.py
# Compiled at: 2020-04-04 06:20:23
# Size of source mod 2**32: 2038 bytes


class Orders:
    client = None
    response = {'state':'fail',  'message':'no initialized'}

    def set_client(self, client):
        self.client = client

    def shop_orders_search(self, access_token, fields, phrase, url_params, order=None, api='/s/MasAbrazos_AR/dw/shop/'):
        if self.client:
            params = {'query':{'text_query': {'fields':fields, 
                             'search_phrase':phrase}}, 
             'sorts':[
              {'field':'customer_name', 
               'sort_order':'asc'}], 
             'select':'(**)'}
            request_end_point = str('order_search' + url_params)
            self.client.set_api(api)
            self.client.set_request_path(request_end_point, 'POST')
            ocapi_response = self.client.do_request(access_token, params)
            self.response = {'state':'ok',  'message':'orders fetched',  'ocapi_response':ocapi_response.json(),  'params':params}
        return self.response

    def shop_update_order_status(self, access_token, order_id, new_status, api='/s/MasAbrazos_AR/dw/shop/'):
        if self.client:
            client_id = self.client.api_credentials['client_id']
            request_end_point = str('orders') + str('/') + str(order_id) + str('?client_id=') + str(client_id)
            self.client.set_api(api)
            print(access_token)
            self.client.set_request_path(request_end_point, 'PATCH')
            ocapi_response = self.client.do_request(access_token, {'confirmation_status': new_status})
            self.response = {'state':'ok', 
             'message':'order updated',  'ocapi_response':ocapi_response.json()}
        return self.response