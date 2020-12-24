# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marc/workspace/tapioca-disqus/tapioca_disqus/tapioca_disqus.py
# Compiled at: 2015-08-19 05:06:55
# Size of source mod 2**32: 1181 bytes
from tapioca import TapiocaAdapter, generate_wrapper_from_adapter, JSONAdapterMixin
from .resource_mapping import RESOURCE_MAPPING

class DisqusClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    api_root = 'https://disqus.com/api/3.0/'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(DisqusClientAdapter, self).get_request_kwargs(api_params, *args, **kwargs)
        if 'params' in params:
            params['params'].update({'api_secret': api_params.get('api_secret')})
        else:
            params['params'] = {'api_secret': api_params.get('api_secret')}
        return params

    def get_iterator_list(self, response_data):
        return response_data['response']

    def get_iterator_next_request_kwargs(self, iterator_request_kwargs, response_data, response):
        cursor = response_data.get('cursor')
        if not cursor or not cursor.get('hasNext'):
            return
        next_val = cursor.get('next')
        if next_val:
            return {'url': '{}&cursor='.format(response.url, next_val)}


Disqus = generate_wrapper_from_adapter(DisqusClientAdapter)