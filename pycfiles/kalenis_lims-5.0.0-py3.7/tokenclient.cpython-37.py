# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trytond/modules/lims_digital_sign/tokenclient.py
# Compiled at: 2019-01-16 09:41:20
# Size of source mod 2**32: 1059 bytes
import json, xmlrpc.client

class EchoClient:

    def __init__(self, listen, origin, target):
        self.listen = listen
        self.origin = origin
        self.target = target
        self.server = self._get_server(self.listen)

    def _get_server(self, listen):
        host, port = listen.split(':')
        return xmlrpc.client.Server('http://%s:%s/' % (host, port))

    def signDoc(self):
        data = json.dumps({'origin':self.origin, 
         'target':self.target})
        self.server.signDoc(data)


class GetToken:

    def __init__(self, listen, origin, target):
        self.listen = listen
        self.origin = origin
        self.target = target

    def signDoc(self, main=False):
        client = EchoClient(self.listen, self.origin, self.target)
        client.signDoc()
        return True