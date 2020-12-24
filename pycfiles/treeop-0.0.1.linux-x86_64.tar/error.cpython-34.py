# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kikutake/.pyenv/versions/3.4.4/lib/python3.4/site-packages/treeop/error.py
# Compiled at: 2016-07-06 08:27:03
# Size of source mod 2**32: 84 bytes


class TreeOpError(Exception):
    pass


class LevelError(TreeOpError):
    pass