# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: bson/min_key.py
# Compiled at: 2014-03-05 17:52:04
"""Representation for the MongoDB internal MinKey type.
"""

class MinKey(object):
    """MongoDB internal MinKey type.

    .. versionchanged:: 2.7
       ``MinKey`` now implements comparison operators.
    """
    _type_marker = 255

    def __eq__(self, other):
        return isinstance(other, MinKey)

    def __ne__(self, other):
        return not self == other

    def __le__(self, dummy):
        return True

    def __lt__(self, other):
        return not isinstance(other, MinKey)

    def __ge__(self, other):
        return isinstance(other, MinKey)

    def __gt__(self, dummy):
        return False

    def __repr__(self):
        return 'MinKey()'