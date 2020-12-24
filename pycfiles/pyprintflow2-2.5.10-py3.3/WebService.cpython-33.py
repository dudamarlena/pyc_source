# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/printflow2/WebService.py
# Compiled at: 2014-04-03 03:33:52
# Size of source mod 2**32: 566 bytes
"""
Created on Oct 1, 2013

@author: "Colin Manning"
"""
import os, socket
from .JDs import JDs

class WebService(object):
    __doc__ = '\n    Provide simple web service access to the PrintFlow data stores and files\n    '
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