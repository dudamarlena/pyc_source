# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/services/tracker/trackbackHandler.py
# Compiled at: 2010-06-01 14:15:46
from dust.util.ymap import YamlMap

class TrackbackHandler:

    def __init__(self):
        self.state = YamlMap('config/trackback.yaml')
        self.callbacks = {}

    def setPutPeerForEndpointCallback(self, key, callback):
        self.callbacks[key] = callback

    def putPeerForEndpoint(self, key, value):
        print('putPeerForEndpoint!!! ' + str(key) + ' ' + str(value))
        try:
            map = self.state['endpoints']
            map[key] = value
            self.state.save()
        except:
            map = {key: value}
            self.state['endpoints'] = map

        print('callbacks: ' + str(self.callbacks))
        callback = self.callbacks[key]
        callback(key, value)