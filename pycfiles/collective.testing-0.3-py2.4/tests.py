# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/collective/testing/tests.py
# Compiled at: 2007-04-17 11:47:01
import doctest
flags = doctest.ELLIPSIS | doctest.REPORT_ONLY_FIRST_FAILURE

def test_suite():
    import collective.testing.debug as debug

    def debug_setup(self):
        debug._test = True

    def debug_teardown(self):
        debug._test = False

    unit_suite = doctest.DocTestSuite(module='collective.testing.debug', globs=dict(pdbator=debug.pdbator, test_func=lambda : 1), setUp=debug_setup, tearDown=debug_teardown, optionflags=flags)
    return unit_suite