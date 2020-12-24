# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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