# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ube/common/settings.py
# Compiled at: 2011-10-29 17:14:06
"""
Created on May 8, 2010

@author: Nicklas Boerjesson
"""
import configparser

class UBPMSettings(object):

    def reload(self, filename):
        self.Parser.read(filename)

    def get(self, _section, _option, _default=None):
        if _default != None and not self.Parser.has_option(_section, _option):
            return _default
        else:
            return self.Parser.get(_section, _option)
            return

    def __init__(self, filename):
        """
        Constructor
        """
        self.Parser = configparser.ConfigParser()
        if filename != '':
            self.reload(filename)