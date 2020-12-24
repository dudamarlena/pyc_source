# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/aio/proto/protoing.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 308 bytes
"""
Device Base Package

"""
from __future__ import absolute_import, division, print_function
from ...aid import getConsole
console = getConsole()

class MixIn(object):
    __doc__ = '\n    Base class to enable consistent MRO for mixin multiple inheritance\n    '

    def __init__(self, *pa, **kwa):
        pass