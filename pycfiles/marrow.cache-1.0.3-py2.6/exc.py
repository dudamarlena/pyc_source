# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/marrow/cache/exc.py
# Compiled at: 2014-12-11 02:18:40
from __future__ import unicode_literals

class CacheMiss(Exception):
    """A matching value could not be found using these criteria."""
    pass