# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yasyf/.virtualenvs/foxtrot-api-client/lib/python3.4/site-packages/foxtrot/client.py
# Compiled at: 2015-05-24 07:23:46
# Size of source mod 2**32: 3839 bytes
import requests, json, types, re, copy
from urllib.parse import urlencode
from .response import FoxtrotResponse
from .errors import ParameterError, APIJSONError

class Foxtrot(object):
    __doc__ = 'Foxtrot API Client'
    host = 'api.foxtrot.io'
    ssl = True
    api_root = ''

    def __init__(self, api_key, version='v1'):
        self.api_key = api_key
        self.version = version
        self.headers = {'content-type': 'application/json'}
        self._Foxtrot__set_methods(self._Foxtrot__fetch_methods())

    def _proto(self):
        if self.ssl:
            return 'https'
        return 'http'

    def _build_url(self, endpoint, args):
        args['key'] = self.api_key
        query = urlencode(args)
        return '{0}://{1}{2}/{3}/{4}?{5}'.format(self._proto(), self.host, self.api_root, self.version, endpoint, query)

    def __decode_json(self, response):
        try:
            return response.json()
        except:
            raise APIJSONError(response.text)

    def __make_request_no_data(self, method, endpoint, args):
        url = self._build_url(endpoint, args)
        response = getattr(requests, method)(url, headers=self.headers)
        return self._Foxtrot__decode_json(response)

    def __make_request_data(self, method, endpoint, data, args):
        url = self._build_url(endpoint, args)
        response = getattr(requests, method)(url, data=json.dumps(data), headers=self.headers)
        return self._Foxtrot__decode_json(response)

    def get(self, endpoint, data, args):
        args.update(data)
        return self._Foxtrot__make_request_no_data('get', endpoint, args)

    def delete(self, endpoint, data, args):
        args.update(data)
        return self._Foxtrot__make_request_no_data('delete', endpoint, args)

    def post(self, endpoint, data, args):
        return self._Foxtrot__make_request_data('post', endpoint, data, args)

    def put(self, endpoint, data, args):
        return self._Foxtrot__make_request_data('put', endpoint, data, args)

    def patch(self, endpoint, data, args):
        return self._Foxtrot__make_request_data('patch', endpoint, data, args)

    def poll(self, txid):
        return self.get_poll(txid=txid)

    def __fetch_methods(self):
        resp = requests.get('{0}://{1}{2}/{3}/endpoints'.format(self._proto(), self.host, self.api_root, self.version))
        return self._Foxtrot__decode_json(resp)['endpoints'][self.version]

    def __create_method(self, endpoint, original_endpoint_name, endpoint_method_name, http_method):
        url_params = re.findall('<(.*)>', endpoint['path'])

        def f(self, *args, **kwargs):
            if len(args) == 1:
                if len(kwargs) == 0:
                    kwargs = args[0]
            for param in endpoint['params'][http_method] + url_params:
                if param not in kwargs:
                    raise ParameterError(param)
                    continue

            endpoint_name = copy.copy(original_endpoint_name)
            for param in url_params:
                endpoint_name = endpoint_name.replace('_<{}>'.format(param), '/{}'.format(kwargs[param]))
                del kwargs[param]

            query = kwargs.pop('_query', {})
            resp = getattr(self, http_method.lower())(endpoint_name, kwargs, query)
            return FoxtrotResponse.response_for(endpoint_name, resp, self)

        f.__name__ = str(endpoint_method_name)
        f.__doc__ = endpoint['description'][http_method]
        return f

    def __set_method(self, endpoint):
        for http_method in endpoint['methods']:
            endpoint_name = endpoint['path'].replace(self.api_root, '', 1).replace('/{}/'.format(self.version), '', 1).replace('/', '_')
            endpoint_method_name = http_method.lower() + '_' + re.sub('_<(.*)>', '', endpoint_name)
            method = types.MethodType(self._Foxtrot__create_method(endpoint, endpoint_name, endpoint_method_name, http_method), self)
            setattr(self, endpoint_method_name, method)

    def __set_methods(self, endpoints):
        for endpoint in list(endpoints.values()):
            if 'url' in endpoint:
                self._Foxtrot__set_method(endpoint)
            else:
                self._Foxtrot__set_methods(endpoint)