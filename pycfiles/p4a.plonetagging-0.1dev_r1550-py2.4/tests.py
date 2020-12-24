# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/p4a/plonetagging/tests.py
# Compiled at: 2007-10-12 18:11:48
import unittest
from zope.testing import doctest

def test_suite():
    return unittest.TestSuite((doctest.DocTestSuite('p4a.plonetagging.l10nutils', optionflags=doctest.ELLIPSIS), doctest.DocTestSuite('p4a.plonetagging.utils', optionflags=doctest.ELLIPSIS)))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')