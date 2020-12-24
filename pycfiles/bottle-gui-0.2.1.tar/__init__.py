# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bystrousak/Dropbox/c0d3z/python/libs/bottle-gui/docs/__init__.py
# Compiled at: 2014-10-21 14:41:30


def allSame(s):
    return not filter(lambda x: x != s[0], s)


def hasDigit(s):
    return any(map(lambda x: x.isdigit(), s))


def getVersion(data):
    data = data.splitlines()
    return filter(lambda (x, y): len(x) == len(y) and allSame(y) and hasDigit(x) and '.' in x, zip(data, data[1:]))[0][0]