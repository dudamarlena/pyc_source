# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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