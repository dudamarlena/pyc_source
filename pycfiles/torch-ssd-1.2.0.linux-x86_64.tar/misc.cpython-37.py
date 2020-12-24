# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/b3ql/.virtualenvs/SSD/lib/python3.7/site-packages/ssd/utils/misc.py
# Compiled at: 2019-10-28 14:34:58
# Size of source mod 2**32: 213 bytes
import errno, os

def str2bool(s):
    return s.lower() in ('true', '1')


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        try:
            if e.errno != errno.EEXIST:
                raise
        finally:
            e = None
            del e