# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\QuillsEnabledRemoteBlogging\tests\test_docfile.py
# Compiled at: 2008-04-09 20:30:20
import unittest
from zope.testing import doctest
from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite
from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import PloneSite
from Products.QuillsEnabledRemoteBlogging import config
from base import QuillsEnabledRemoteBloggingDocTestCase
ZOPE_DEPS = [
 'QuillsEnabled', config.PROJECTNAME]
PLONE_DEPS = ['QuillsEnabled', config.PROJECTNAME]
for x in ZOPE_DEPS + PLONE_DEPS:
    ZopeTestCase.installProduct(x)

PloneTestCase.setupPloneSite(products=PLONE_DEPS)

def test_suite():
    suite = unittest.TestSuite(())
    suite.addTest(ZopeDocFileSuite('metaweblogapi.txt', package='quills.remoteblogging.tests', test_class=QuillsEnabledRemoteBloggingDocTestCase, optionflags=doctest.ELLIPSIS))
    suite.layer = PloneSite
    return suite