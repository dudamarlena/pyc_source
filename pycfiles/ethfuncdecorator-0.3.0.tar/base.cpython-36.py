# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/providers/base.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 2291 bytes
import itertools, json
from eth_utils import to_bytes, to_text
from web3.middleware import combine_middlewares

class BaseProvider:
    _middlewares = ()
    _request_func_cache = (None, None)

    @property
    def middlewares(self):
        return self._middlewares

    @middlewares.setter
    def middlewares(self, values):
        self._middlewares = tuple(values)

    def request_func(self, web3, outer_middlewares):
        """
        @param outer_middlewares is an iterable of middlewares, ordered by first to execute
        @returns a function that calls all the middleware and eventually self.make_request()
        """
        all_middlewares = tuple(outer_middlewares) + tuple(self.middlewares)
        cache_key = self._request_func_cache[0]
        if cache_key is None or cache_key != all_middlewares:
            self._request_func_cache = (all_middlewares,
             self._generate_request_func(web3, all_middlewares))
        return self._request_func_cache[(-1)]

    def _generate_request_func(self, web3, middlewares):
        return combine_middlewares(middlewares=middlewares,
          web3=web3,
          provider_request_fn=(self.make_request))

    def make_request(self, method, params):
        raise NotImplementedError('Providers must implement this method')

    def isConnected(self):
        raise NotImplementedError('Providers must implement this method')


class JSONBaseProvider(BaseProvider):

    def __init__(self):
        self.request_counter = itertools.count()

    def decode_rpc_response(self, response):
        return json.loads(to_text(response))

    def encode_rpc_request(self, method, params):
        return to_bytes(text=(json.dumps({'jsonrpc':'2.0', 
         'method':method, 
         'params':params or [], 
         'id':next(self.request_counter)})))

    def isConnected(self):
        try:
            response = self.make_request('web3_clientVersion', [])
        except IOError:
            return False
        else:
            if not response['jsonrpc'] == '2.0':
                raise AssertionError
            elif not 'error' not in response:
                raise AssertionError
            return True
            if not False:
                raise AssertionError