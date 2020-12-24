# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/web/test.py
# Compiled at: 2011-06-21 16:54:55
"""test utilities
(part of web.py)
"""
import unittest, sys, os, web
TestCase = unittest.TestCase
TestSuite = unittest.TestSuite

def load_modules(names):
    return [ __import__(name, None, None, 'x') for name in names ]


def module_suite(module, classnames=None):
    """Makes a suite from a module."""
    if classnames:
        return unittest.TestLoader().loadTestsFromNames(classnames, module)
    else:
        if hasattr(module, 'suite'):
            return module.suite()
        return unittest.TestLoader().loadTestsFromModule(module)


def doctest_suite(module_names):
    """Makes a test suite from doctests."""
    import doctest
    suite = TestSuite()
    for mod in load_modules(module_names):
        suite.addTest(doctest.DocTestSuite(mod))

    return suite


def suite(module_names):
    """Creates a suite from multiple modules."""
    suite = TestSuite()
    for mod in load_modules(module_names):
        suite.addTest(module_suite(mod))

    return suite


def runTests(suite):
    runner = unittest.TextTestRunner()
    return runner.run(suite)


def main(suite=None):
    if not suite:
        main_module = __import__('__main__')
        args = [ a for a in sys.argv[1:] if not a.startswith('-') ]
        suite = module_suite(main_module, args or None)
    result = runTests(suite)
    sys.exit(not result.wasSuccessful())
    return