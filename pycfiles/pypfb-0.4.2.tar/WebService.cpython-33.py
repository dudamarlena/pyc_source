# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/printflow2/WebService.py
# Compiled at: 2014-04-03 03:33:52
# Size of source mod 2**32: 566 bytes
__doc__ = '\nCreated on Oct 1, 2013\n\n@author: "Colin Manning"\n'
import os, socket
from .JDs import JDs

class WebService(object):
    """WebService"""
    configData = None
    ready = False
    theSocket = None

    def __init__(self, configFile):
        """
        Constructor
        """
        self.ready = True

    def is_ready(self):
        return self.ready

    def start(self):
        self.theSocket = socket()

    def stop(self):
        self.theSocket.close()