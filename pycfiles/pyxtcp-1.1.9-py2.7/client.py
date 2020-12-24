# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyxtcp/http/client.py
# Compiled at: 2015-11-02 22:15:14
import json, functools, requests
from .util import server_log

class RPCRequestError(Exception):
    pass


class RPCClient(object):

    def __init__(self, address):
        self.address = address
        self.address_prefix = 'http://' + self.address

    def service_name(self, service_name):
        return _RPCClientServiceHandler(self, service_name)


class _RPCClientServiceHandler(object):

    def __init__(self, client, service_name):
        self._client = client
        self._service_name = service_name
        self._server_address_prefix = self._client.address_prefix + '/' + self._service_name

    def ___handler_request(self, func_name, **kwargs):
        kwargs_v = ''
        if kwargs:
            kwargs_v = json.dumps(kwargs)
        server_log.debug(('Request To {}.{}({})').format(self._service_name, func_name, kwargs))
        request_params = {'v': kwargs_v}
        try:
            content = requests.post(self._server_address_prefix + '/' + func_name, data=request_params).json()
            result = content['v']
            status = content['s']
        except:
            raise RPCRequestError('Request invalid')

        if status:
            return result
        raise RPCRequestError('Request Error, %s ' % (result,))

    def __getattr__(self, func):
        try:
            return self.__dict__[func]
        except KeyError:
            return functools.partial(self.___handler_request, func)