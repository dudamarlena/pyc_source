# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.activitystream/plonesocial/activitystream/tests/test_example.py
# Compiled at: 2013-07-05 10:36:06
import unittest2 as unittest
from Products.CMFCore.utils import getToolByName
from plonesocial.activitystream.testing import PLONESOCIAL_ACTIVITYSTREAM_INTEGRATION_TESTING

class TestExample(unittest.TestCase):
    layer = PLONESOCIAL_ACTIVITYSTREAM_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        pid = 'plonesocial.activitystream'
        installed = [ p['id'] for p in self.qi_tool.listInstalledProducts() ]
        self.assertTrue(pid in installed, 'package appears not to have been installed')