# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/octodns/equality.py
# Compiled at: 2019-10-18 13:06:59
from __future__ import absolute_import, division, print_function, unicode_literals

class EqualityTupleMixin(object):

    def _equality_tuple(self):
        raise NotImplementedError(b'_equality_tuple method not implemented')

    def __eq__(self, other):
        return self._equality_tuple() == other._equality_tuple()

    def __ne__(self, other):
        return self._equality_tuple() != other._equality_tuple()

    def __lt__(self, other):
        return self._equality_tuple() < other._equality_tuple()

    def __le__(self, other):
        return self._equality_tuple() <= other._equality_tuple()

    def __gt__(self, other):
        return self._equality_tuple() > other._equality_tuple()

    def __ge__(self, other):
        return self._equality_tuple() >= other._equality_tuple()