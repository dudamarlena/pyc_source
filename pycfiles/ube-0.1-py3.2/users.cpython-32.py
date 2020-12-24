# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ube/common/users.py
# Compiled at: 2012-09-09 15:30:11
"""
Created on May 8, 2010

@author: Nicklas Boerjesson
"""
from configparser import SafeConfigParser

class user(object):
    pass


class users(object):

    def reload(self, filename):
        self.Parser.read(filename)

    def __init__(self, filename):
        """
        Constructor
        """
        self.Parser = SafeConfigParser()
        if filename != '':
            self.reload(filename)