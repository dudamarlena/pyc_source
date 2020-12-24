# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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