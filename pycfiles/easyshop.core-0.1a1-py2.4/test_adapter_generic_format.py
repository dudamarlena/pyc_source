# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/tests/test_adapter_generic_format.py
# Compiled at: 2008-08-07 12:42:20
from DateTime import DateTime
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from base import EasyShopTestCase
from easyshop.core.tests import utils
from easyshop.core.interfaces import IFormats
from easyshop.core.interfaces import IImageManagement

class TestFormatterInfos(EasyShopTestCase):
    """
    """
    __module__ = __name__

    def afterSetUp(self):
        """
        """
        super(TestFormatterInfos, self).afterSetUp()
        self.fi_1 = IFormats(self.shop)
        self.fi_2 = IFormats(self.shop.categories.category_1)

    def testGetFormats(self):
        """
        """
        fi_1 = self.fi_1.getFormats()
        fi_2 = self.fi_2.getFormats()
        self.assertEqual(fi_1['lines_per_page'], 1)
        self.assertEqual(fi_1['products_per_line'], 2)
        self.assertEqual(fi_1['image_size'], 'mini')
        self.assertEqual(fi_1['text'], 'short_text')
        self.assertEqual(fi_1['product_height'], 0)
        self.assertEqual(fi_2['lines_per_page'], 1)
        self.assertEqual(fi_2['products_per_line'], 2)
        self.assertEqual(fi_2['image_size'], 'mini')
        self.assertEqual(fi_2['text'], 'short_text')
        self.assertEqual(fi_2['product_height'], 0)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFormatterInfos))
    return suite