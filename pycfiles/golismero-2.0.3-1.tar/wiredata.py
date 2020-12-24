# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/thirdparty_libs/dns/wiredata.py
# Compiled at: 2013-08-26 10:52:44
"""DNS Wire Data Helper"""
import sys, dns.exception

class WireData(str):

    def __getitem__(self, key):
        try:
            return WireData(super(WireData, self).__getitem__(key))
        except IndexError:
            raise dns.exception.FormError

    def __getslice__(self, i, j):
        try:
            if j == sys.maxint:
                j = len(self)
            if i < 0 or j < 0:
                raise dns.exception.FormError
            if i != j:
                super(WireData, self).__getitem__(i)
                super(WireData, self).__getitem__(j - 1)
            return WireData(super(WireData, self).__getslice__(i, j))
        except IndexError:
            raise dns.exception.FormError

    def __iter__(self):
        i = 0
        while 1:
            try:
                yield self[i]
                i += 1
            except dns.exception.FormError:
                raise StopIteration

    def unwrap(self):
        return str(self)


def maybe_wrap(wire):
    if not isinstance(wire, WireData):
        return WireData(wire)
    else:
        return wire