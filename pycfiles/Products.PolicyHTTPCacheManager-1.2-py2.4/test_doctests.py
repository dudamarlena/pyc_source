# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/PolicyHTTPCacheManager/tests/test_doctests.py
# Compiled at: 2008-04-16 07:07:54
"""
$Id: test_doctests.py 62766 2008-04-16 11:07:45Z wichert $
"""
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Testing import ZopeTestCase
from Testing.ZopeTestCase import FunctionalDocFileSuite
from Products.CMFTestCase import CMFTestCase
CMFTestCase.installProduct('PageTemplates')
CMFTestCase.installProduct('StandardCacheManagers')
CMFTestCase.installProduct('PolicyHTTPCacheManager')
CMFTestCase.setupCMFSite()
from zope.testing import doctest
OPTIONFLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

class FunctionalTest(CMFTestCase.FunctionalTestCase):
    __module__ = __name__


def test_suite():
    import unittest
    suite = unittest.TestSuite()
    for fname in ('cache_manager.txt', ):
        suite.addTest(FunctionalDocFileSuite(fname, optionflags=OPTIONFLAGS, package='Products.PolicyHTTPCacheManager.tests', test_class=FunctionalTest))

    return suite


if __name__ == '__main__':
    framework(descriptions=0, verbosity=1)