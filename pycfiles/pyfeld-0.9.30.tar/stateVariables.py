# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyfeld/stateVariables.py
# Compiled at: 2017-11-23 08:41:51
from __future__ import unicode_literals
from pyfeld.didlInfo import DidlInfo

class StateVariables:

    def __init__(self, udn):
        self.udn = udn
        self.state_dict = dict()

    def set_states(self, items_dict):
        for key, value in items_dict.items():
            self.set_state(key, value)

        try:
            didlinfo = DidlInfo(items_dict[b'AVTransportURIMetaData'], False)
            self.state_dict[b'didlextractUri'] = didlinfo.get_items()
        except:
            pass

        try:
            didlinfo = DidlInfo(items_dict[b'TrackMetaData'], False)
            self.state_dict[b'didlextract'] = didlinfo.get_items()
        except:
            pass

    def set_state(self, key, value):
        self.state_dict[key] = value

    def get_state(self, key):
        if key in self.state_dict:
            return self.state_dict[key]
        else:
            return
            return

    def get_states(self, key):
        return self.state_dict

    def get_info(self):
        result = b'udn:' + self.udn
        for item in self.state_dict:
            result += b'\n' + item.first + b':' + item.second

        return result