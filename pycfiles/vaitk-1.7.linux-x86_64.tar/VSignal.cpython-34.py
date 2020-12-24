# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vaitk/core/VSignal.py
# Compiled at: 2015-05-02 14:14:14
# Size of source mod 2**32: 689 bytes


class VSignal(object):

    def __init__(self, sender):
        self._sender = sender
        self._slots = []
        self._enabled = True

    def connect(self, target):
        if isinstance(target, VSignal):
            slot = target.emit
        else:
            slot = target
        if target not in self._slots:
            self._slots.append(slot)

    def disconnect(self, target):
        if target in self._slots:
            self._slots.remove(target)

    def emit(self, *args, **kwargs):
        if not self._enabled:
            return
        for slot in self._slots:
            slot(*args, **kwargs)

    def setEnabled(self, enabled):
        self._enabled = enabled