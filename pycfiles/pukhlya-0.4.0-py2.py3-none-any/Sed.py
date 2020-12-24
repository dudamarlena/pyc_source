# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: puke/Sed.py
# Compiled at: 2011-12-05 13:53:03
import hashlib

class Sed:

    def __init__(self):
        self._list = {}

    def add(self, search, replace):
        self._list[search] = replace

    def keys(self):
        t = []
        for k, v in self._list.items():
            t.append(k)

        return t

    def get(self, key):
        return self._list[key]

    def getSignature(self):
        sig = ''
        for k, v in self._list.items():
            sig += '%s' % hashlib.sha256('%s%s' % (k, v)).hexdigest()

        return hashlib.sha256(sig).hexdigest()