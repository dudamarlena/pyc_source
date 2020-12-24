# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/test/examples/pythoncode.py
# Compiled at: 2008-06-17 03:34:41


class A(object):
    __module__ = __name__

    def foo(self):
        """foo"""
        return 'foo'


class B(A):
    __module__ = __name__

    class C(object):
        __module__ = __name__


def bar():
    """bar"""
    return 'bar'


results = {'lc': 22, 'nclasses': 3, 'ndefs': 2, 'ncomments': 4, 'nstrs': 11, 'nkws': 8, 'ndkws': 4}