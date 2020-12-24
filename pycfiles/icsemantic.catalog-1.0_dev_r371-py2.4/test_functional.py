# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/catalog/tests/test_functional.py
# Compiled at: 2008-10-06 10:31:12
"""Functional tests for OntoCatalog.
"""
import unittest, doctest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase.layer import PloneSite
from icsemantic.catalog.config import *
import base

def test_suite():
    return unittest.TestSuite([ztc.ZopeDocFileSuite('tests/synonymous_criterion.txt', package=PACKAGENAME, test_class=base.ICSemanticCatalogFunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('tests/translated_criterion.txt', package=PACKAGENAME, test_class=base.ICSemanticCatalogFunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('tests/related_criterion.txt', package=PACKAGENAME, test_class=base.ICSemanticCatalogFunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), ztc.ZopeDocFileSuite('tests/advanced_search.txt', package=PACKAGENAME, test_class=base.ICSemanticCatalogFunctionalTestCase, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')