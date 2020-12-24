# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/system.py
# Compiled at: 2007-05-29 11:51:02
"""
Module to send queries to query the registry.

"""
__id__ = '$Id: system.py 97 2007-05-29 15:51:00Z eddie $'
import UserDict
from astrogrid import acr

class Configuration(UserDict.UserDict):
    __module__ = __name__

    def __init__(self):
        d = acr.system.configuration.list()
        self.data = {}
        for k in d.keys():
            self[k] = d[k]

    def update(self, dd):
        for key in dd:
            acr.system.configuration.setKey(key, dd[key])

        self[key] = dd[key]