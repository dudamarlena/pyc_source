# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sorno/mathlib.py
# Compiled at: 2020-03-16 00:44:32
# Size of source mod 2**32: 2471 bytes
"""A library for math related things

Copyright 2015 Heung Ming Tai

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from collections import namedtuple

class Interval(object):
    __doc__ = "An interval with a starting and a ending points, open or closed.\n\n    It's a read-only class.\n\n    Attributes:\n        start (int or float): The starting point of the interval.\n        end (int or float): The ending point of the interval.\n        is_start_opened (Optional[bool]): True if the starting point is open.\n            It's False by default.\n        is_end_opened (Optional[bool]): True if the ending point is open.\n            It's False by default.\n    "

    def __init__(self, start, end, is_start_opened=False, is_end_opened=False):
        self._start = start
        self._end = end
        self._is_start_opened = is_start_opened
        self._is_end_opened = is_end_opened

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def is_start_opened(self):
        return self._is_start_opened

    @property
    def is_end_opened(self):
        return self._is_end_opened

    def __str__(self):
        tmp = 'Interval(start=%r,end=%r,is_start_opened=%r,is_end_opened=%r)'
        return tmp % (
         self._start,
         self._end,
         self._is_start_opened,
         self._is_end_opened)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, Interval):
            return False
        return (
         self._start,
         self._end,
         self._is_start_opened,
         self._is_end_opened) == (
         other._start,
         other._end,
         other._is_start_opened,
         other._is_end_opened)