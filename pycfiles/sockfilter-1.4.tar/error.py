# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/sockfilter/sockfilter/error.py
# Compiled at: 2014-07-08 15:52:13
__all__ = [
 'SockFilterError']
import collections

class SockFilterError(Exception):
    Tuple = collections.namedtuple('SockFilterError', ['address'])

    def __init__(self, address):
        self.address = address

    def __repr__(self):
        return repr(self._tuple)

    def __str__(self):
        return str(self._tuple)

    def __unicode__(self):
        return unicode(self._tuple)

    def __eq__(self, other):
        if not hasattr(other, '_tuple'):
            return False
        return self._tuple == other._tuple

    def __ne__(self, other):
        if not hasattr(other, '_tuple'):
            return False
        return self._tuple != other._tuple

    @property
    def _tuple(self):
        return self.Tuple(address=self.address)