# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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