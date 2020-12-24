# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redomino/advancedkeyword/tests/test_doctest.py
# Compiled at: 2013-05-08 04:41:18
import unittest, doctest
from zope.component import testing

def test_suite():
    return unittest.TestSuite([
     doctest.DocTestSuite(module='redomino.advancedkeyword.indexers', setUp=testing.setUp, tearDown=testing.tearDown),
     doctest.DocTestSuite(module='redomino.advancedkeyword.vocabularies', setUp=testing.setUp, tearDown=testing.tearDown)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')