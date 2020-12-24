# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nxlib/oop.py
# Compiled at: 2011-03-10 15:49:42
"""
oop.py

Created by newlix on 2011-03-11.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

class Borg(object):
    _shared_state = {}

    def __new__(cls, *a, **k):
        obj = object.__new__(cls, *a, **k)
        obj.__dict__ = cls._shared_state
        return obj