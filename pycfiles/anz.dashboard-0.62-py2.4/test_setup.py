# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/anz/dashboard/tests/test_setup.py
# Compiled at: 2010-09-26 21:53:53
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from anz.dashboard.tests.base import AnzDashBoardTestCase

class TestProductInstall(AnzDashBoardTestCase):
    __module__ = __name__

    def test_skinLayersInstalled(self):
        subIds = self.portal.portal_skins.objectIds()
        ids = ['anz_dashboard', 'anz_dashboard_resources']
        for id in ids:
            self.assert_(id in subIds)

    def test_typesInstalled(self):
        subIds = self.portal.portal_types.objectIds()
        ids = ['Anz Dashboard']
        for id in ids:
            self.assert_(id in subIds)

    def test_modifyToDefaultPage(self):
        properties = self.folder.portal_properties.site_properties
        self.assert_('Anz Dashboard' in properties.getProperty('default_page'))

    def test_ActionCategoryInstalled(self):
        subIds = self.portal.portal_actions.objectIds()
        self.assert_('dashboard_widgets' in subIds)
        dashboard_widgets = self.portal.portal_actions.dashboard_widgets
        self.assertEqual(dashboard_widgets.meta_type, 'CMF Action Category')

    def test_i18nSetup(self):
        ltool = self.portal.portal_languages
        defaultLanguage = 'zh-cn'
        supportedLanguages = ['en', 'zh-cn']
        ltool.manage_setLanguageSettings(defaultLanguage, supportedLanguages, setUseCombinedLanguageCodes=False)
        ltool.setLanguageBindings()
        view = self.folder.restrictedTraverse('@@msgCatalog', None)
        ret = view.catalogMapping('anz.dashboard', retJson=False)
        self.assert_(ret['success'])
        self.assert_(len(ret['texts'].keys()) > 1)
        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductInstall))
    return suite


if __name__ == '__main__':
    framework()