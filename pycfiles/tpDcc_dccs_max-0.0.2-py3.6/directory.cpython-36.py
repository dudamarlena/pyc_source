# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/max/core/directory.py
# Compiled at: 2020-04-11 22:25:56
# Size of source mod 2**32: 564 bytes
"""
Module that contains functions and classes related with directories and files in 3ds Max
"""
from __future__ import print_function, division, absolute_import
import MaxPlus

def get_file(caption='Select File', filters='*', start_directory=''):
    try:
        result = MaxPlus.Core.EvalMAXScript('getOpenFileName             caption:"{}"             filename:"{}"             types:"{}";'.format(caption, start_directory, filters)).Get()
        return result
    except Exception:
        return