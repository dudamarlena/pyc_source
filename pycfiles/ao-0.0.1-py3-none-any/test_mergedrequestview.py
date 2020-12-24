# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/anz/dashboard/tests/test_mergedrequestview.py
# Compiled at: 2010-09-26 21:53:53
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from anz.dashboard.tests.base import AnzDashBoardTestCase

class TestMergedRequestView(AnzDashBoardTestCase):
    __module__ = __name__

    def test_viewRetrieve(self):
        view = self.folder.restrictedTraverse('@@mergedRequest', None)
        self.assert_(view is not None)
        return

    def test_getMergedData(self):
        ltool = self.portal.portal_languages
        defaultLanguage = 'zh-cn'
        supportedLanguages = ['en', 'zh-cn']
        ltool.manage_setLanguageSettings(defaultLanguage, supportedLanguages, setUseCombinedLanguageCodes=False)
        ltool.setLanguageBindings()
        view = self.folder.restrictedTraverse('@@mergedRequest', None)
        requests = [
         'widgets@@widgetView/getWidgets', 'i18n@@msgCatalog/catalogMapping?domain=anz.dashboard']
        ret = view.getMergedData(requests=requests, retJson=False)
        self.assertEqual(ret['i18n']['success'], True)
        self.assertEqual(ret['widgets']['success'], True)
        requests = [
         'wrong@@wrongView/dummy', 'i18n@@msgCatalog/catalogMapping?domain=anz.dashboard']
        ret = view.getMergedData(requests=requests, retJson=False)
        self.assertEqual(ret['i18n']['success'], True)
        self.assertEqual(ret['wrong']['success'], False)
        requests = [
         'widgets@@widgetView/wrongMethod', 'i18n@@msgCatalog/catalogMapping?domain=anz.dashboard']
        ret = view.getMergedData(requests=requests, retJson=False)
        self.assertEqual(ret['i18n']['success'], True)
        self.assertEqual(ret['widgets']['success'], False)
        requests = [
         'widgets@@widgetView/getWidgets', 'i18n@@msgCatalog/catalogMapping?domain:list=anz.dashboard']
        ret = view.getMergedData(requests=requests, retJson=False)
        self.assertEqual(ret['i18n']['success'], True)
        self.assertEqual(ret['widgets']['success'], True)
        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMergedRequestView))
    return suite


if __name__ == '__main__':
    framework()