# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/panipuri/backends/CacheBackend.py
# Compiled at: 2014-04-27 07:42:47


class CacheBackend(object):

    def put(self, key, val):
        raise NotImplemented

    def get(self, key):
        raise NotImplemented