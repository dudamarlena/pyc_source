# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iccommunity/mediawiki/tests/test_utilities.py
# Compiled at: 2008-10-06 10:31:13
"""Test the catalog indexes added by OntoCatalog.
"""
import unittest
from zope.component import getUtility
from iccommunity.mediawiki.tests.base import MediawikiTestCase
from iccommunity.mediawiki.interfaces import IicCommunityManagementMediawikiRolesMapper

class TestMediawikiUtilities(MediawikiTestCase):
    """Testing utilities"""
    __module__ = __name__

    def test_get_parsed_rolemap(self):
        """Testing the get_parsed_rolemap method"""
        self.loginAsPortalOwner()
        settings = getUtility(IicCommunityManagementMediawikiRolesMapper, name='iccommunity.configuration', context=self.portal)
        settings.rolemap = [
         'Role;Role', 'Another role;    A mediawiki role ']
        expected = [('Role', 'Role'), ('Another role', 'A mediawiki role')]
        self.assertEquals(settings.get_parsed_rolemap(), expected)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMediawikiUtilities))
    return suite