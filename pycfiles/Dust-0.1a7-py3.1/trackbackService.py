# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/services/tracker/trackbackService.py
# Compiled at: 2010-06-01 14:16:01
from dust.core.util import encodeAddress
from dust.util.jsonrpc.serviceHandler import ServiceHandler
from dust.services.tracker.trackbackHandler import TrackbackHandler

class TrackbackService:

    def __init__(self):
        self.router = None
        self.handler = TrackbackHandler()
        self.trackback = ServiceHandler(self.handler)
        return

    def setRouter(self, r):
        self.router = r

    def setPutPeerForEndpointCallback(self, key, callback):
        self.handler.setPutPeerForEndpointCallback(key, callback)

    def handle(self, msock, msg, addr):
        print('Trackback message from ' + encodeAddress(addr) + ':')
        self.trackback.handleRequest(msg.decode('utf-8'))