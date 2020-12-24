# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_vendor/packaging/_compat.py
# Compiled at: 2019-09-10 15:18:29
from __future__ import absolute_import, division, print_function
import sys
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    string_types = (
     str,)
else:
    string_types = (
     basestring,)

def with_metaclass(meta, *bases):
    """
    Create a base class with a metaclass.
    """

    class metaclass(meta):

        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)

    return type.__new__(metaclass, 'temporary_class', (), {})