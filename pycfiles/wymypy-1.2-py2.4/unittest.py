# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wymypy/libs/unittest.py
# Compiled at: 2007-01-15 12:44:20


class UnitTest:
    __module__ = __name__
    __tests = []

    @classmethod
    def register(cls, method):
        cls.__tests.append(method)
        return method

    @classmethod
    def run(cls):
        print 'Run UnitTest'
        for method in cls.__tests:
            print ':: UnitTest : %s( )' % method.__name__
            method()

    @staticmethod
    def exception(strfct):
        try:
            return eval(strfct)
        except Exception, m:
            return m.__class__