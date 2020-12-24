# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/protocol.py
# Compiled at: 2012-10-12 07:02:39


class Protocol(object):
    __xmlrpc__ = False

    def set_protocol_name(self, name):
        self._protocol_name = name

    @property
    def protocol_name(self):
        if hasattr(self, '_protocol_name'):
            return self._protocol_name
        return self.__pattern__[0]