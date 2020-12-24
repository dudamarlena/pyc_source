# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/anz/dashboard/tests/test_rsswidgetview.py
# Compiled at: 2010-09-26 21:53:53
import os, sys
from time import sleep
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from anz.dashboard.tests.base import AnzDashBoardTestCase

class TestRssWidgetView(AnzDashBoardTestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.folder.invokeFactory(type_name='Document', id='doc1', title='doc 1')
        self.folder.doc1.indexObject()
        self.folder.invokeFactory(type_name='Anz Dashboard', id='dashboard1', title='dashboard 1')
        self.folder.dashboard1.indexObject()

    def test_viewApplied(self):
        view = self.folder.doc1.restrictedTraverse('@@rssWidget', None)
        self.assert_(view is None)
        view = self.folder.dashboard1.restrictedTraverse('@@rssWidget', None)
        self.assert_(view is not None)
        return

    def test_entries(self):
        view = self.folder.dashboard1.restrictedTraverse('@@rssWidget', None)
        ret = view.entries('http://newsrss.bbc.co.uk/rss/newsonline_world_edition/front_page/rss.xml', cachetime=1, retJson=False)
        self.assert_(ret['success'] == True)
        ret = view.entries('http://newsrss.bbc.co.uk/rss/newsonline_world_edition/front_page/rss.xml', cachetime=1, retJson=False)
        self.assert_(ret['success'] == True)
        sleep(3)
        ret = view.entries('http://newsrss.bbc.co.uk/rss/newsonline_world_edition/front_page/rss.xml', cachetime=1, retJson=False)
        self.assert_(ret['success'] == True)
        ret = view.entries('http://wrong url', retJson=False)
        self.assert_(ret['success'] == False)
        return


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRssWidgetView))
    return suite


if __name__ == '__main__':
    framework()