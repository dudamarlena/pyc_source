# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/aam/options.py
# Compiled at: 2014-06-05 07:01:35
import os

class DictSpace(dict):

    def __getattr__(self, key):
        if key in self:
            return self[key]
        raise AttributeError

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except:
            raise AttributeError


hub = DictSpace()
hub.root = DictSpace()
hub.site = DictSpace()