# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/anz/ijabbar/tests/test_setup.py
# Compiled at: 2010-04-15 21:25:08
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from anz.ijabbar.tests.base import AnzIJabbarTestCase

class TestProductInstall(AnzIJabbarTestCase):
    __module__ = __name__

    def test_skinLayersInstalled(self):
        subIds = self.portal.portal_skins.objectIds()
        ids = ['anz_ijabbar']
        for id in ids:
            self.assert_(id in subIds)

    def test_propertiesInstalled(self):
        self.assert_('anz_ijabbar_properties' in self.folder.portal_properties.objectIds())
        properties = self.folder.portal_properties.anz_ijabbar_properties


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductInstall))
    return suite


if __name__ == '__main__':
    framework()