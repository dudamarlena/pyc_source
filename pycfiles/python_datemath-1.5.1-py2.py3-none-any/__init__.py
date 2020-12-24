# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nmaccarthy/dev/misc/python-datemath/datemath/__init__.py
# Compiled at: 2019-10-23 20:42:40
from .helpers import parse

def dm(expr, **kwargs):
    """ does our datemath and returns an arrow object """
    return parse(expr, **kwargs)


def datemath(expr, **kwargs):
    """ does our datemath and returns a datetime object """
    return parse(expr, **kwargs).datetime