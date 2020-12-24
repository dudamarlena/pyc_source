# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_api/mercury_clients.py
# Compiled at: 2018-06-20 15:42:58
# Size of source mod 2**32: 947 bytes
from mercury.common.clients.inventory import InventoryClient
from mercury.common.clients.rpc.frontend import RPCFrontEndClient
from mercury.common.exceptions import MercuryTransportError

def transceiver_decorator(f):

    def wrapper(self, *args, **kwargs):
        result = f(self, *args, **kwargs)
        if result['error']:
            raise MercuryTransportError(f"[{self.service_name}]Error communicating with service: {result['message']}")
        return result['message']

    return wrapper


class SimpleInventoryClient(InventoryClient):

    @transceiver_decorator
    def transceiver(self, payload):
        return super(InventoryClient, self).transceiver(payload)


class SimpleRPCFrontEndClient(RPCFrontEndClient):

    @transceiver_decorator
    def transceiver(self, payload):
        return super(RPCFrontEndClient, self).transceiver(payload)