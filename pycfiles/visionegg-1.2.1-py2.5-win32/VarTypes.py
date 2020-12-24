# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\PyroApps\VarTypes.py
# Compiled at: 2009-07-15 18:56:28


def getID(var_type):
    if var_type == 'float':
        return 1
    elif var_type == 'int' or var_type == 'integer':
        return 2
    elif var_type == 'string' or var_type == 'str':
        return 3
    else:
        return -1


def getType(ID):
    if ID == 1:
        return 'float'
    elif ID == 2:
        return 'integer'
    elif ID == 3:
        return 'string'
    else:
        return 'undefined type'