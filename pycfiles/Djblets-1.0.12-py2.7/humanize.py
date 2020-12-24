# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/humanize.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals

def humanize_list(value):
    """
    Humanizes a list of values, inserting commas and "and" where appropriate.

      ========================= ======================
      Example List              Resulting string
      ========================= ======================
      ``["a"]``                 ``"a"``
      ``["a", "b"]``            ``"a and b"``
      ``["a", "b", "c"]``       ``"a, b and c"``
      ``["a", "b", "c", "d"]``  ``"a, b, c, and d"``
      ========================= ======================
    """
    if len(value) == 0:
        return b''
    if len(value) == 1:
        return value[0]
    s = (b', ').join(value[:-1])
    if len(value) > 3:
        s += b','
    return b'%s and %s' % (s, value[(-1)])