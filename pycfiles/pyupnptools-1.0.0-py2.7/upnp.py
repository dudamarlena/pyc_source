# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyupnptools/upnp.py
# Compiled at: 2018-09-02 06:58:36
from .upnp_model import *
from .http_server import *
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class USN:

    def __init__(self, udn, st):
        self._udn = udn
        self._st = st

    def udn(self):
        return self._udn

    def st(self):
        return self._st

    def __str__(self):
        if self._st:
            return ('{}::{}').format(self._udn, self._st)
        return self._udn

    @staticmethod
    def read(text):
        tokens = text.split('::', 1)
        if len(tokens) < 2:
            udn = text
            st = ''
        else:
            udn = tokens[0]
            st = tokens[1]
        return USN(udn, st)


class UPnPRequest:

    def request(self):
        raise Exception('Not implemented')


class UPnPResponse:

    def __init__(self):
        self._data = None
        self._headers = {}
        return

    def header(self, name, value=None):
        if value is not None:
            self._headers[name.upper()] = (
             name, value)
        else:
            return self._headers[name.upper()][1]
        return

    def data(self, dx=None):
        if dx is not None:
            self._data = dx
        else:
            return self._data
        return


class UPnPDeviceListener:

    def on_device_added(self, device):
        pass

    def on_device_removed(self, device):
        pass