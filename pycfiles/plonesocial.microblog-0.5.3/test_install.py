# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.microblog/plonesocial/microblog/tests/test_install.py
# Compiled at: 2013-04-12 05:54:49
import unittest2 as unittest
from Products.CMFCore.utils import getToolByName
from plonesocial.microblog.testing import PLONESOCIAL_MICROBLOG_INTEGRATION_TESTING

class TestInstall(unittest.TestCase):
    layer = PLONESOCIAL_MICROBLOG_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        pid = 'plonesocial.microblog'
        installed = [ p['id'] for p in self.qi_tool.listInstalledProducts() ]
        self.assertTrue(pid in installed, 'package appears not to have been installed')