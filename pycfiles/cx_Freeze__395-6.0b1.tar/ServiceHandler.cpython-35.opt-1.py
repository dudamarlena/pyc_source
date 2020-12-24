# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \.\cx_Freeze\samples\service\ServiceHandler.py
# Compiled at: 2019-08-29 22:24:39
# Size of source mod 2**32: 1098 bytes
__doc__ = '\nImplements a simple service using cx_Freeze.\n\nSee below for more information on what methods must be implemented and how they\nare called.\n'
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