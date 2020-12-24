# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\samples\service\ServiceHandler.py
# Compiled at: 2016-04-18 03:12:47
# Size of source mod 2**32: 1098 bytes
"""
Implements a simple service using cx_Freeze.

See below for more information on what methods must be implemented and how they
are called.
"""
import threading

class Handler(object):

    def __init__(self):
        self.stopEvent = threading.Event()
        self.stopRequestedEvent = threading.Event()

    def Initialize(self, configFileName):
        pass

    def Run(self):
        self.stopRequestedEvent.wait()
        self.stopEvent.set()

    def Stop(self):
        self.stopRequestedEvent.set()
        self.stopEvent.wait()