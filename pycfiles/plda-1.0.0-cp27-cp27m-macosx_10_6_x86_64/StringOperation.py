# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\lib\StringOperation.py
# Compiled at: 2018-09-18 04:40:01


def PickupFor2Key(str, key1, key2):
    fx = str.find(key1)
    if fx >= 0:
        fy = str.find(key2, fx)
    else:
        return (
         str, -1)
    if fy < fx:
        return str
    if fx < 0 or fy < 0:
        return (str, -1)
    val = str[fx + len(key1):fy]
    return (
     val, 1)


def RemoveFor2Key(str, key1, key2):
    fx = str.find(key1)
    if fx >= 0:
        fy = str.find(key2, fx)
    else:
        return (
         str, -1)
    if fy < fx:
        return (str, -1)
    if fx < 0 or fy < 0:
        return (str, -1)
    fs = str[:fx - 1]
    fe = str[fy + len(key2):]
    val = fs + fe
    return (
     val, 1)


def find_lastpos(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position