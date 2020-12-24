# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/types/newmemoryview.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 654 bytes
"""
A pretty lame implementation of a memoryview object for Python 2.6.
"""
from collections import Iterable
from numbers import Integral
import string
from future.utils import istext, isbytes, PY3, with_metaclass
from future.types import no, issubset

class newmemoryview(object):
    __doc__ = '\n    A pretty lame backport of the Python 2.7 and Python 3.x\n    memoryviewview object to Py2.6.\n    '

    def __init__(self, obj):
        return obj


__all__ = [
 'newmemoryview']