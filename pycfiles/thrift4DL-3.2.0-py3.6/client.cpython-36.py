# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thrift4DL/client/client.py
# Compiled at: 2020-01-12 21:21:44
# Size of source mod 2**32: 1889 bytes
import traceback, json
from .thrift4DL.ttypes import *
from .thrift4DL import Thrift4DLService
from thrift.protocol.TJSONProtocol import TJSONProtocol
from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from thrift.transport import TTransport, TSocket, TSSLSocket, THttpClient
import sys
if sys.version_info[0] > 2:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse

class BaseClient:

    def predict(self, x):
        pass

    def ping(self):
        pass


class Client(BaseClient):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = TSocket.TSocket(host, port)
        self.transport = TTransport.TFramedTransport(self.socket)
        self.protocol = TBinaryProtocol(self.transport)
        self.client = Thrift4DLService.Client(self.protocol)

    def predict(self, x):
        self.transport.open()
        ret = None
        try:
            request_dict = {'value': x}
            request_json = json.dumps(request_dict)
            ret = self.client.predict(request_json)
        except Exception as e:
            print(traceback.format_exc())

        self.transport.close()
        return ret

    def ping(self):
        self.transport.open()
        ret = None
        try:
            ret = self.client.ping()
        except Exception as e:
            print(traceback.format_exc())

        self.transport.close()
        return ret


class VisionClient(Client):

    def predict(self, image_binary):
        self.transport.open()
        ret = None
        try:
            ret = self.client.predict(image_binary)
        except Exception as e:
            print(traceback.format_exc())

        self.transport.close()
        return ret