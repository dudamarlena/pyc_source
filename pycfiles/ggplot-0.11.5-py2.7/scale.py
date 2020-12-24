# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/scales/scale.py
# Compiled at: 2016-07-11 10:52:39
from __future__ import absolute_import, division, print_function, unicode_literals

class scale(object):
    """
    Base class for scales.
    """
    VALID_SCALES = []

    def __init__(self, *args, **kwargs):
        for s in self.VALID_SCALES:
            setattr(self, s, None)

        if args:
            self.name = args[0]
        for k, v in kwargs.items():
            if k in self.VALID_SCALES:
                setattr(self, k, v)

        return