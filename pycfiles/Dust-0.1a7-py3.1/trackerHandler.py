# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/services/tracker/trackerHandler.py
# Compiled at: 2010-06-01 14:16:01
from dust.util.ymap import YamlMap
from dust.services.tracker.trackbackClient import TrackbackClient

class TrackerHandler:

    def __init__(self, router, addr):
        print('new TrackerHandler ' + str(addr))
        self.router = router
        self.addr = addr
        self.state = YamlMap('config/tracker.yaml')

    def getPeerForEndpoint(self, key):
        print('getPeerForEndpoint(' + str(key) + ')')
        try:
            map = self.state['endpoints']
            value = map[key]
            trackback = TrackbackClient(self.router, self.addr)
            trackback.putPeerForEndpoint(key, value)
        except Exception as e:
            print('exception: ' + str(e))

    def putPeerForEndpoint(self, key, value):
        print('putPeerForEndpoint(' + str(key) + ',' + str(value) + ')')
        try:
            map = self.state['endpoints']
            map[key] = value
            self.state.save()
        except Exception as e:
            map = {key: value}
            self.state['endpoints'] = map