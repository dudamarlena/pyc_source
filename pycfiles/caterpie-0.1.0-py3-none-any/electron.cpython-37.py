# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/catenae/electron.py
# Compiled at: 2019-08-07 08:55:15
# Size of source mod 2**32: 1401 bytes
import copy

class Electron:

    def __init__(self, key=None, value=None, topic=None, previous_topic=None, unpack_if_string=False, callbacks=None, timestamp=None):
        self.key = key
        self.value = value
        self.topic = topic
        self.previous_topic = previous_topic
        self.unpack_if_string = unpack_if_string
        if callbacks is None:
            self.callbacks = []
        else:
            self.callbacks = callbacks
        self.timestamp = timestamp

    def __bool__(self):
        if self.value != None:
            return True
        return False

    def get_sendable(self):
        copy = self.copy()
        copy.topic = None
        copy.previous_topic = None
        copy.unpack_if_string = False
        copy.callbacks = []
        copy.timestamp = None
        return copy

    def copy(self):
        electron = Electron()
        electron.key = self.key
        electron.value = copy.deepcopy(self.value)
        electron.topic = self.topic
        electron.previous_topic = self.previous_topic
        electron.unpack_if_string = self.unpack_if_string
        electron.callbacks = self.callbacks
        electron.timestamp = self.timestamp
        return electron