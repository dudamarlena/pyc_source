# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/chimera/tests/test_doctest.py
# Compiled at: 2007-02-08 13:55:31
import unittest, doctest
modules = [
 'chimera.chimera',
 'chimera.utils',
 'chimera.colors']

def test_suite():
    g = globals()
    suite = unittest.TestSuite()
    for module in modules:
        try:
            mobj = __import__(module, g, g, module.split('.', 1)[1])
        except IndexError, E:
            mobj = __import__(module, g, g, None)

        suite.addTest(doctest.DocTestSuite(mobj))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(test_suite())