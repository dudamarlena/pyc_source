# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/collection/alphabetic/tests/test_setup.py
# Compiled at: 2009-06-10 13:50:14
import unittest
from Products.CMFCore.utils import getToolByName
from base import CollectionAlphabeticTestCase

class TestSetup(CollectionAlphabeticTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.types = getToolByName(self.portal, 'portal_types')
        self.propertiestool = getToolByName(self.portal, 'portal_properties')

    def test_character_tokens(self):
        self.assertEquals('boolean', self.propertiestool.collection_alphabetic_properties.getPropertyType('use_alphabet'))
        self.assertEquals('tokens', self.propertiestool.collection_alphabetic_properties.getPropertyType('character_tokens'))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite