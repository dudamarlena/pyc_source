# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/meringue/__init__.py
# Compiled at: 2015-08-22 16:35:01
__VERSION__ = ((0, 3, 4), )
try:
    from verlib import NormalizedVersion
    version = str(NormalizedVersion.from_parts(*__VERSION__))
except ImportError:
    version = ('.').join([ str(j) for i in __VERSION__ for j in i ])