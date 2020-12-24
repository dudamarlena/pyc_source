# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kikutake/.pyenv/versions/3.4.4/lib/python3.4/site-packages/treeop/mapto.py
# Compiled at: 2016-07-06 08:18:46
# Size of source mod 2**32: 648 bytes
from .error import LevelError

def mapto(func, obj, level):
    if level == 0:
        return func(obj)
    if isinstance(obj, list):
        ret = [
         None] * len(obj)
        for i in range(0, len(obj)):
            ret[i] = mapto(func, obj[i], level - 1)

        return ret
    if isinstance(obj, tuple):
        ret = [
         None] * len(obj)
        for i in range(0, len(obj)):
            ret[i] = mapto(func, obj[i], level - 1)

        return tuple(ret)
    if isinstance(obj, dict):
        ret = {}
        for key in obj.keys():
            ret[key] = mapto(func, obj[key], level - 1)

        return ret
    raise LevelError()