# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kikutake/.pyenv/versions/3.4.4/lib/python3.4/site-packages/treeop/applyto.py
# Compiled at: 2016-07-06 08:30:30
# Size of source mod 2**32: 428 bytes
from .error import LevelError

def applyto(func, obj, level):
    if level == 0:
        func(obj)
        return
    if isinstance(obj, list) or isinstance(obj, tuple):
        for i in range(0, len(obj)):
            applyto(func, obj[i], level - 1)

        return
    if isinstance(obj, dict):
        for key in obj.keys():
            applyto(func, obj[key], level - 1)

        return
    raise LevelError()