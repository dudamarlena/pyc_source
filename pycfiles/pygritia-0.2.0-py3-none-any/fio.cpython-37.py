# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ykent/GitLab/pygrisb/pygrisb/pygrisb/io/fio.py
# Compiled at: 2019-02-22 23:25:01
# Size of source mod 2**32: 185 bytes
__doc__ = '\nHelp functions for io.\n'
import os

def file_exists(fname):
    """check whether a non-empty file exists.
    """
    return os.path.isfile(fname) and os.path.getsize(fname) > 0