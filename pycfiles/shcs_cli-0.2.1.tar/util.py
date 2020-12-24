# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fraoustin/Workspace/shcs_cli/shcs_cli/util.py
# Compiled at: 2016-09-11 11:02:52
import myterm.table

def first_value(*args):
    for arg in args:
        if arg != None:
            return arg

    return args[(-1)]


Table = myterm.table.Table