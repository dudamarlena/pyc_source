# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/anz/dashboard/tests/test_msgcatalogview.py
# Compiled at: 2010-09-26 21:53:53
import os, sys
from anz.dashboard.tests.base import AnzDashBoardTestCase

class TestMsgCatalogView(AnzDashBoardTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.folder.invokeFactory(type_name='Document', id='doc1', title='doc 1')
        self.folder.doc1.indexObject()
        self.folder.invokeFactory(type_name='News Item', id='news1', title='news 1')
        self.folder.news1.indexObject()
        self.folder.invokeFactory(type_name='Folder', id='folder1', title='folder 1')
        self.folder.folder1.indexObject()
        ltool = self.portal.portal_languages
        defaultLanguage = 'zh-cn'
        supportedLanguages = ['en', 'zh-cn']
        ltool.manage_setLanguageSettings(defaultLanguage, supportedLanguages, setUseCombinedLanguageCodes=False)
        ltool.setLanguageBindings()

    def test_viewRetrieve(self):
        view = self.folder.restrictedTraverse('@@msgCatalog', None)
        self.assert_(view is not None)
        view = self.folder.doc1.restrictedTraverse('@@msgCatalog', None)
        self.assert_(view is not None)
        view = self.folder.news1.restrictedTraverse('@@msgCatalog', None)
        self.assert_(view is not None)
        view = self.folder.folder1.restrictedTraverse('@@msgCatalog', None)
        self.assert_(view is not None)
        return

    def test_catalogMapping(self):
        view = self.folder.restrictedTraverse('@@msgCatalog', None)
        ret = view.catalogMapping('anz.dashboard', retJson=False)
        self.assert_(ret['success'])
        self.assert_(len(ret['texts'].keys()) > 1)
        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMsgCatalogView))
    return suite