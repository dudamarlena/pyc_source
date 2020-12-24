# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/restapi/websocket.py
# Compiled at: 2019-05-25 07:28:23
from autobahn.twisted.websocket import WebSocketServerProtocol

class AnyDexWebsocketProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print ('Client connecting: {0}').format(request.peer)

    def onOpen(self):
        print 'WebSocket connection open.'

    def onMessage(self, payload, isBinary):
        if isBinary:
            print ('Binary message received: {0} bytes').format(len(payload))
        else:
            print ('Text message received: {0}').format(payload.decode('utf8'))
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print ('WebSocket connection closed: {0}').format(reason)