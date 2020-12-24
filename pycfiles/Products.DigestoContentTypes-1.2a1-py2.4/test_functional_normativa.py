# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Products/DigestoContentTypes/tests/test_functional_normativa.py
# Compiled at: 2009-04-26 22:17:24
import unittest, doctest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.DigestoContentTypes.tests.base import DigestoContentTypesFunctionalTestCase

def test_suite():
    return unittest.TestSuite([ztc.ZopeDocFileSuite('tests/fulltextsearch.txt', package='Products.DigestoContentTypes', test_class=DigestoContentTypesFunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('tests/sendmail.txt', package='Products.DigestoContentTypes', test_class=DigestoContentTypesFunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('tests/duplicatedid.txt', package='Products.DigestoContentTypes', test_class=DigestoContentTypesFunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('tests/requiredsource.txt', package='Products.DigestoContentTypes', test_class=DigestoContentTypesFunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('tests/extensionattachments.txt', package='Products.DigestoContentTypes', test_class=DigestoContentTypesFunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('tests/renameattachements.txt', package='Products.DigestoContentTypes', test_class=DigestoContentTypesFunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')