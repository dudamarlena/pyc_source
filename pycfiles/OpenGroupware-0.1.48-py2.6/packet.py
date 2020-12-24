# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/packet.py
# Compiled at: 2012-10-12 07:02:39
from uuid import uuid4
from time import time
from exception import CoilsException

class Packet(object):

    def __init__(self, source, target, data, qos=None, auth=None, kind=None):
        self._source = source
        self._target = target
        self._data = data
        self._uuid = ('{{{0}}}').format(str(uuid4()))
        self._reply_to = None
        self._qos = None
        self._auth = None
        self._time = float(time())
        if kind is None:
            self._kind = 'application/x-pickle-ascii.python'
        else:
            self._kind = kind
        return

    def __repr__(self):
        return ('<Packet source="{0}" target="{1}" UUID="{2}"/>').format(self.source, self.target, self.uuid)

    @property
    def data(self):
        return self._data

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    @property
    def uuid(self):
        return self._uuid

    @property
    def reply_to(self):
        return self._reply_to

    @property
    def time(self):
        return self._time

    @staticmethod
    def Reply(packet, data):
        m = Packet(packet.target, packet.source, data)
        m._reply_to = str(packet.uuid)
        return m

    @staticmethod
    def Service(name):
        if name is None:
            raise CoilsException('Request for service from NULL address')
        return name.split('/')[0].lower()

    @staticmethod
    def Method(name):
        if name is None:
            raise CoilsException('Request for method from NULL address')
        return name.split('/')[1].split(':')[0]

    @staticmethod
    def Parameter(name):
        if name is None:
            raise CoilsException('Request for parameter from NULL address')
        x = name.split('/')[1].split(':')
        if len(x) > 1:
            return x[1]
        else:
            return
            return