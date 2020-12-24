# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\QuillsRemoteBlogging\tests\test_docfile.py
# Compiled at: 2008-06-04 06:25:04
import unittest
from zope.testing import doctest
from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite
from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import PloneSite
from Products.QuillsRemoteBlogging import config
from base import QuillsRemoteBloggingDocTestCase
ZOPE_DEPS = [
 'Quills', config.PROJECTNAME]
PLONE_DEPS = ['Quills', config.PROJECTNAME]
for x in ZOPE_DEPS + PLONE_DEPS:
    ZopeTestCase.installProduct(x)

PloneTestCase.setupPloneSite(products=PLONE_DEPS)

def test_suite():
    suite = unittest.TestSuite(())
    suite.addTest(ZopeDocFileSuite('metaweblogapi.txt', package='quills.remoteblogging.tests', test_class=QuillsRemoteBloggingDocTestCase, optionflags=doctest.ELLIPSIS))
    suite.layer = PloneSite
    return suite