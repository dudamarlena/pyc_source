# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/ploneformgen/readonlystringfield/tests/test_setup.py
# Compiled at: 2009-03-24 10:52:00
import unittest
from Products.CMFCore.utils import getToolByName
from quintagroup.ploneformgen.readonlystringfield.tests.base import ReadOnlyStringFieldTestCase

class TestSetup(ReadOnlyStringFieldTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def test_installerTool(self):
        tool = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(tool.isProductInstalled('PloneFormGen'), 'PloneFormGen product is not installed.')

    def test_factoryTool(self):
        tool = getToolByName(self.portal, 'portal_factory')
        self.failUnless('FormReadonlyStringField' in tool._factory_types.keys(), 'FormReadonlyStringField type is not in portal_factory tool.')

    def test_typesTool(self):
        tool = getToolByName(self.portal, 'portal_types')
        self.failUnless('FormReadonlyStringField' in tool.objectIds(), 'FormReadonlyStringField type is not in portal_types tool.')

    def test_propertiesTool(self):
        tool = getToolByName(self.portal, 'portal_properties')
        navtree = tool.navtree_properties
        self.failUnless('FormReadonlyStringField' in navtree.metaTypesNotToList, 'FormReadonlyStringField is not in metaTypesNotToList property.')
        site = tool.site_properties
        self.failUnless('FormReadonlyStringField' in site.types_not_searched, 'FormReadonlyStringField is not in types_not_searched property.')

    def test_skinsTool(self):
        tool = getToolByName(self.portal, 'portal_skins')
        self.failUnless('readonlystringfield' in tool.objectIds(), 'There is no readonlystringfield folder in portal_skins.')
        for (path_id, path) in tool._getSelections().items():
            layers = [ l.strip() for l in path.split(',') ]
            self.failUnless('readonlystringfield' in layers, 'readonlystringfield layer is not registered for %s.' % path_id)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite