# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/anz/dashboard/tests/test_foldercontentswidgetview.py
# Compiled at: 2010-09-26 21:53:53
import os, sys
from DateTime import DateTime
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from anz.dashboard.tests.base import AnzDashBoardTestCase

class TestFolderContentsWidgetView(AnzDashBoardTestCase):
    __module__ = __name__

    def afterSetUp(self):
        now = DateTime()
        date = now - 2
        self.folder.invokeFactory(type_name='Folder', id='folder1', title='folder 1')
        self.folder1 = self.folder.folder1
        self.folder1.setModificationDate(date)
        self.folder1.setCreationDate(date)
        self.folder1.indexObject()
        self.folder1.invokeFactory(type_name='Document', id='doc1', title='doc 1')
        self.doc1 = self.folder1.doc1
        self.doc1.setModificationDate(date)
        self.doc1.setCreationDate(date)
        self.doc1.indexObject()
        date = now - 1
        self.folder.invokeFactory(type_name='Folder', id='folder2', title='folder 2')
        self.folder2 = self.folder.folder2
        self.folder2.setModificationDate(date)
        self.folder2.setCreationDate(date)
        self.folder2.indexObject()
        self.folder2.invokeFactory(type_name='News Item', id='news1', title='news 1')
        self.news1 = self.folder2.news1
        self.news1.setModificationDate(date)
        self.news1.setCreationDate(date)
        self.news1.indexObject()
        self.folder.invokeFactory(type_name='Anz Dashboard', id='dashboard1', title='dashboard 1')
        self.folder.dashboard1.indexObject()

    def test_viewApplied(self):
        view = self.doc1.restrictedTraverse('@@folderContentsWidget', None)
        self.assert_(view is None)
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse('@@folderContentsWidget', None)
        self.assert_(view is not None)
        return

    def test_getChildNodesData(self):
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse('@@folderContentsWidget', None)
        data = []
        info = {}
        info['id'] = 'folder1'
        info['text'] = unicode('folder 1')
        info['url'] = self.folder.folder1.absolute_url()
        info['path'] = '/plone/Members/test_user_1_/folder1'
        data.append(info)
        info = {}
        info['id'] = 'folder2'
        info['text'] = unicode('folder 2')
        info['url'] = self.folder.folder2.absolute_url()
        info['path'] = '/plone/Members/test_user_1_/folder2'
        data.append(info)
        path = ('/').join(self.folder.getPhysicalPath())
        self.assertEqual(data, view.getChildNodesData(path=path, retJsonFormat=False))
        path = ('/').join(self.folder1.getPhysicalPath())
        self.assertEqual([], view.getChildNodesData(path=path, retJsonFormat=False))
        path = ('/').join(self.folder2.getPhysicalPath())
        self.assertEqual([], view.getChildNodesData(path=path, retJsonFormat=False))
        return

    def test_items(self):
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse('@@folderContentsWidget', None)
        folderPath = ('/').join(self.folder.getPhysicalPath())
        folder1Path = ('/').join(self.folder1.getPhysicalPath())
        folder2Path = ('/').join(self.folder2.getPhysicalPath())
        ret = view.items(paths=[folder1Path], retJson=False)
        self.assertEqual(1, len(ret['items']))
        ret = view.items(paths=[folder1Path, folder2Path], retJson=False)
        self.assertEqual(2, len(ret['items']))
        ret = view.items(paths=[folder1Path], searchSub=True, retJson=False)
        self.assertEqual(2, len(ret['items']))
        ret = view.items(paths=[folder1Path, folder2Path], searchSub=True, retJson=False)
        self.assertEqual(4, len(ret['items']))
        ret = view.items(paths=[folder1Path], portal_types=['Document', 'News Item'], retJson=False)
        self.assertEqual(1, len(ret['items']))
        ret = view.items(paths=[folderPath], searchSub=True, portal_types='Document,News Item', retJson=False)
        self.assertEqual(2, len(ret['items']))
        ret = view.items(paths=[folderPath], searchSub=True, recentDays=0, retJson=False)
        self.assertEqual(6, len(ret['items']))
        ret = view.items(paths=[folderPath], searchSub=True, recentDays=1, retJson=False)
        self.assertEqual(4, len(ret['items']))
        ret = view.items(paths=[folderPath], searchSub=True, recentDays=2, retJson=False)
        self.assertEqual(6, len(ret['items']))
        ret = view.items(paths=[folderPath], searchSub=True, sort_limit=2, retJson=False)
        self.assertEqual(2, len(ret['items']))
        return

    def test_types(self):
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse('@@folderContentsWidget', None)
        ret = view.types(retJson=False)
        self.assertEqual(ret['success'], True)
        self.assert_(len(ret['types']) > 1)
        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFolderContentsWidgetView))
    return suite


if __name__ == '__main__':
    framework()