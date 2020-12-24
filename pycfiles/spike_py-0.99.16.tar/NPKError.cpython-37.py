# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/NPKError.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 688 bytes
"""
untitled.py

Created by Marc-André on 2010-07-20.
Copyright (c) 2010 IGBMC. All rights reserved.
"""
from __future__ import print_function

class NPKError(Exception):
    __doc__ = ' implements NPK generic exception\n        adds the named argument data, which can be used to describe the NPKData involved\n    '

    def __init__(self, msg='', data=None):
        self.msg = msg
        self.data = data

    def __str__(self):
        st = self.msg
        if self.data is not None:
            st = '\n%s\n\nData-set involved :\n===================\n%s\n' % (st, self.data.report())
        return st