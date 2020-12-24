# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/providers/rpc.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 1845 bytes
import logging, os
from eth_utils import to_dict
from web3.middleware import http_retry_request_middleware
from web3.utils.datastructures import NamedElementOnion
from web3.utils.http import construct_user_agent
from web3.utils.request import make_post_request
from .base import JSONBaseProvider
logger = logging.getLogger(__name__)

def get_default_endpoint():
    return os.environ.get('WEB3_HTTP_PROVIDER_URI', 'http://localhost:8545')


class HTTPProvider(JSONBaseProvider):
    endpoint_uri = None
    _request_args = None
    _request_kwargs = None
    _middlewares = NamedElementOnion([(http_retry_request_middleware, 'http_retry_request')])

    def __init__(self, endpoint_uri=None, request_kwargs=None):
        if endpoint_uri is None:
            self.endpoint_uri = get_default_endpoint()
        else:
            self.endpoint_uri = endpoint_uri
        self._request_kwargs = request_kwargs or {}
        super().__init__()

    def __str__(self):
        return 'RPC connection {0}'.format(self.endpoint_uri)

    @to_dict
    def get_request_kwargs(self):
        if 'headers' not in self._request_kwargs:
            yield (
             'headers', self.get_request_headers())
        for key, value in self._request_kwargs.items():
            yield (
             key, value)

    def get_request_headers(self):
        return {'Content-Type':'application/json', 
         'User-Agent':construct_user_agent(str(type(self)))}

    def make_request(self, method, params):
        request_data = self.encode_rpc_request(method, params)
        raw_response = make_post_request(
         (self.endpoint_uri), 
         request_data, **self.get_request_kwargs())
        response = self.decode_rpc_response(raw_response)
        return response