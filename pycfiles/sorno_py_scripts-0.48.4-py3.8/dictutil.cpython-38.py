# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sorno/dictutil.py
# Compiled at: 2020-03-16 00:44:32
# Size of source mod 2**32: 452 bytes
"""dictutil provides additional classes or functions for python dicts
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from collections import defaultdict

class DefaultDictWithEnhancedFactory(defaultdict):
    __doc__ = 'A dict with a default factory that takes the missing key'

    def __missing__(self, key):
        return self.default_factory(key)