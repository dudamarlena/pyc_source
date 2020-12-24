# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/util/path/ntpath.py
# Compiled at: 2018-04-20 03:19:42
"""Galaxy "safe" path functions forced to work with Windows-style paths regardless of current platform
"""
from __future__ import absolute_import
import ntpath, sys
from . import _build_self
_build_self(sys.modules[__name__], ntpath)