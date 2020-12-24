# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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