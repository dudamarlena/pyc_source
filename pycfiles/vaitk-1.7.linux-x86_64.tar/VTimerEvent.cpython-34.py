# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vaitk/core/VTimerEvent.py
# Compiled at: 2015-05-02 14:14:14
# Size of source mod 2**32: 128 bytes
from .VEvent import VEvent

class VTimerEvent(VEvent):

    def __init__(self):
        super().__init__(VEvent.EventType.Timer)