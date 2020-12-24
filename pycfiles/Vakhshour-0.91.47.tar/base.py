# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/Vakhshour/vakhshour/base.py
# Compiled at: 2012-09-01 11:39:39
import json, hashlib, logging
from threading import Thread
from OpenSSL import SSL
from argparse import ArgumentParser
from twisted.internet import ssl, defer
from twisted.internet.protocol import ClientCreator
from twisted.protocols import amp
from amp import ampy

class VObject(object):
    """
    Vakhshour objects base class.
    """
    logger = logging.getLogger('vakhshour')


class CtxFactory(ssl.ClientContextFactory):

    def __init__(self, key, cert):
        self.key = key
        self.cert = cert

    def getContext(self):
        self.method = SSL.SSLv23_METHOD
        ctx = ssl.ClientContextFactory.getContext(self)
        ctx.use_certificate_file(self.cert)
        ctx.use_privatekey_file(self.key)
        return ctx


class Node(object):

    def __init__(self, host='127.0.0.1', port='8888', secure=False, ssl_key=None, ssl_cert=None, expect_answer=False, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        self.host = host
        self.port = port
        self.secure = secure
        self.ssl_key = ssl_key
        self.ssl_cert = ssl_cert
        self.expect_answer = expect_answer

    def send_event(self, name, sender, **kwargs):
        proxy = ampy.Proxy(self.host, int(self.port), self.secure, ssl_key=self.ssl_key, ssl_cert=self.ssl_cert).connect()
        if self.expect_answer:
            response = proxy.callRemote(self.Event, name=name, sender=sender, kwargs=kwargs)
            responses = {}
            for k, v in response.items():
                responses[k] = v

            return responses
        proxy.callRemote(self.Event, name=name, sender=sender, kwargs=kwargs)
        return {}

    class Event(ampy.Command):

        class Json(ampy.String):
            """
            Json argument type.
            """

            def toString(self, inObject):
                return str(json.dumps(inObject))

            def fromString(self, inString):
                return json.loads(inString)

        commandName = 'Event'
        arguments = [
         (
          'name', ampy.Unicode()),
         (
          'sender', ampy.String()),
         (
          'kwargs', Json())]
        response = [
         (
          'status', ampy.Integer())]

        def deserializeResponse(cls, wireResponse):
            return wireResponse

        deserializeResponse = classmethod(deserializeResponse)