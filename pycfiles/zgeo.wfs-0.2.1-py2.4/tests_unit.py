# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zgeo/wfs/tests/tests_unit.py
# Compiled at: 2008-10-13 09:51:31
import unittest
from zope.component.testing import setUp, tearDown
from zope.configuration.xmlconfig import XMLConfig
from zope.testing import doctest
from zope.testing.doctestunit import DocFileSuite
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc

def configurationSetUp(self):
    setUp()
    import zgeo.geographer, zgeo.wfs, zope.component, zope.annotation, zope.app.publisher.browser, Products.Five, Products.Archetypes, Products.CMFCore, Products.GenericSetup
    XMLConfig('meta.zcml', zope.component)()
    XMLConfig('meta.zcml', zope.app.publisher.browser)()
    XMLConfig('meta.zcml', Products.Five)()
    XMLConfig('meta.zcml', Products.GenericSetup)()
    XMLConfig('meta.zcml', Products.CMFCore)()
    XMLConfig('configure.zcml', zope.annotation)()
    XMLConfig('configure.zcml', Products.Five)()
    XMLConfig('configure.zcml', Products.GenericSetup)()
    XMLConfig('configure.zcml', Products.Archetypes)()
    XMLConfig('configure.zcml', zgeo.geographer)()
    XMLConfig('configure.zcml', zgeo.wfs)()
    ztc.installProduct('PluginIndexes')
    ptc.setupPloneSite(products=[])


def test_suite():
    return unittest.TestSuite((DocFileSuite('tests/unit.txt', package='zgeo.wfs', setUp=configurationSetUp, tearDown=tearDown, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE), DocFileSuite('geocatalog/rtree.txt', package='zgeo.wfs', setUp=configurationSetUp, tearDown=tearDown, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')