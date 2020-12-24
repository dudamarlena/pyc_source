# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/test/examples/docstrings.py
# Compiled at: 2007-09-05 02:50:36
"""module doc continued module doc"""

class MyClass(object):
    """class doc"""
    __module__ = __name__

    def foo(self):
        """method doc"""
        return 'foo'


def bar():
    """function doc"""
    return 'bar'


class MyClass1(object):
    """class doc 1"""
    __module__ = __name__

    def foo(self):
        """method doc continued method doc"""
        return 'foo'


def bar1():
    x = 1
    return 'bar1'


def bar2():
    """multi-line 
    function doc"""
    return 'bar2'


if True:
    x = 1