# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ykent/GitLab/pygrisb/pygrisb/pygrisb/io/fio.py
# Compiled at: 2019-02-22 23:25:01
# Size of source mod 2**32: 185 bytes
"""
Help functions for io.
"""
import os

def file_exists(fname):
    """check whether a non-empty file exists.
    """
    return os.path.isfile(fname) and os.path.getsize(fname) > 0