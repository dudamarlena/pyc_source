# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.11.1-i386/egg/z3c/discriminator/tests.py
# Compiled at: 2007-11-26 11:34:12
from zope.testing import doctest
import unittest
OPTIONFLAGS = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
import zope.component.testing, zope.component.tests

def test_suite():
    return unittest.TestSuite((doctest.DocFileSuite('README.txt', optionflags=OPTIONFLAGS, setUp=zope.component.testing.setUp, tearDown=zope.component.testing.tearDown, package='z3c.discriminator'),) + tuple((suite for suite in zope.component.tests.test_suite())))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')