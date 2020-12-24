# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vaitk/test/VSignalSpy.py
# Compiled at: 2015-05-02 14:14:14
# Size of source mod 2**32: 510 bytes
from ..core.VObject import VObject

class VSignalSpy(VObject):

    def __init__(self, signal):
        self._signal_params = []
        self._signal = signal
        self._signal.connect(self._signalReceived)

    def _signalReceived(self, *args, **kwargs):
        self._signal_params.append((args, kwargs))

    def count(self):
        return len(self._signal_params)

    def lastSignalParams(self):
        return self._signal_params[(-1)]

    def signalParams(self):
        return self._signal_params