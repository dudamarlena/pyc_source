# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/borg.py
# Compiled at: 2010-12-12 18:24:12
"""
Created on Dec 6, 2010

@author: eric
"""

class Borg:
    """ pseudo singleton
                Use this as a base class to make a singleton type object.
                In your __init__ method, do this:
                Borg.__init__(self)
        """
    _shred_state = {}

    def __init__(self):
        self.__dict__ = self._shred_state