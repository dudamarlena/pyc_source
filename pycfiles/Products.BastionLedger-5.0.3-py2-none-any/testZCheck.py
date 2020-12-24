# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionBanking/tests/testZCheck.py
# Compiled at: 2015-07-18 19:38:10
from Products.BastionBase.tests.ZPTTestCase import SkinsTestCase

class TestSkins(SkinsTestCase):
    skinname = 'bastionbanking'
    productname = 'BastionBanking'


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSkins))
    return suite