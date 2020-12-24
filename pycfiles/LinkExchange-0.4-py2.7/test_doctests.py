# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/test_doctests.py
# Compiled at: 2011-04-21 17:44:20
import doctest

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite('linkexchange.config'))
    tests.addTests(doctest.DocTestSuite('linkexchange.db_drivers'))
    tests.addTests(doctest.DocTestSuite('linkexchange.formatters'))
    tests.addTests(doctest.DocTestSuite('linkexchange.platform'))
    tests.addTests(doctest.DocTestSuite('linkexchange.utils'))
    tests.addTests(doctest.DocTestSuite('linkexchange.tests'))
    return tests