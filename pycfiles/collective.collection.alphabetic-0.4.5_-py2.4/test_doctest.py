# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/collection/alphabetic/tests/test_doctest.py
# Compiled at: 2009-06-10 12:36:06
import unittest, doctest
from zope.testing import doctestunit
from zope.component import testing, eventtesting
from Testing import ZopeTestCase as ztc
from collective.collection.alphabetic.tests import base

class TestSetup(base.CollectionAlphabeticFunctionalTestCase):
    __module__ = __name__

    def afterSetUp(self):
        """Code that is needed is the afterSetUp of both test cases.
        """
        ztc.utils.setupCoreSessions(self.app)


def test_suite():
    return unittest.TestSuite([doctestunit.DocFileSuite('tests/unittest.txt', package='collective.collection.alphabetic', setUp=testing.setUp, tearDown=testing.tearDown, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.FunctionalDocFileSuite('tests/functional.txt', package='collective.collection.alphabetic', test_class=TestSetup, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')