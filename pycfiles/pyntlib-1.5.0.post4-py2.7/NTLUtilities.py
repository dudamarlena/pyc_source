# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLUtilities.py
# Compiled at: 2018-04-23 08:51:10
import math, sys
__all__ = [
 'jsrange', 'jsstring', 'jsint', 'jsmaxint', 'jsbytes', 'jsstrjsfloor',
 'jsceil', 'jsround',
 'jskeys', 'jsvalues', 'jsitems',
 'jssquare', 'jssign', 'jsappend', 'jsupdate']
ispy3 = sys.version_info[0] > 2
jsrange = range if ispy3 else xrange
jsstring = str if ispy3 else basestring
jsint = int if ispy3 else (int, long)
jsmaxint = sys.maxsize if ispy3 else sys.maxint
jsstr = str if ispy3 else unicode
jsbytes = bytes if ispy3 else str
jsfloor = math.floor if ispy3 else (lambda x: int(math.floor(x)))
jsceil = math.ceil if ispy3 else (lambda x: int(math.ceil(x)))
jsround = round if ispy3 else (lambda x: int(round(x)))
jskeys = lambda x: list(x.keys()) if ispy3 else x.keys()
jsvalues = lambda x: list(x.values()) if ispy3 else x.values()
jsitems = lambda x: list(x.items()) if ispy3 else x.items()

def jssquare(*args):
    from math import sqrt
    for var in args:
        if int(sqrt(var)) ** 2 != var:
            return False

    return True


def jssign(num):
    if num >= 0:
        return 1
    return -1


def jsappend(rst, dst):
    if isinstance(dst, list):
        return list(set(rst + dst))
    else:
        return list(set(rst + [dst]))


def jsupdate(rst, dst):
    for key in dst:
        if key in rst:
            if isinstance(dst[key], dict):
                jsupdate(rst[key], dst[key])
            else:
                rst[key] += dst[key]
        else:
            rst[key] = dst[key]

    return rst