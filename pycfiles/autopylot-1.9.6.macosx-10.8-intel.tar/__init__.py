# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/autopylot/lib/python2.7/site-packages/autopylot/__init__.py
# Compiled at: 2013-11-26 22:17:25
from contextlib import contextmanager
from .enum import *
import urlparse

@contextmanager
def ignored(*exceptions):
    """ inspired by http://hg.python.org/cpython/rev/406b47c64480"""
    exceptions = exceptions or Exception
    try:
        yield
    except exceptions:
        pass


def formaturl(url):
    parsed = list(urlparse.urlparse(url))
    parsed[2] = parsed[2].replace('//', '/')
    return urlparse.urlunparse(parsed)