# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bystrousak/Dropbox/c0d3z/python/libs/bottle-gui/docs/__init__.py
# Compiled at: 2014-10-21 14:41:30


def allSame(s):
    return not filter(lambda x: x != s[0], s)


def hasDigit(s):
    return any(map(lambda x: x.isdigit(), s))


def getVersion(data):
    data = data.splitlines()
    return filter(lambda (x, y): len(x) == len(y) and allSame(y) and hasDigit(x) and '.' in x, zip(data, data[1:]))[0][0]