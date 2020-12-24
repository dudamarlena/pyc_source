# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/component/add_remove_sub_window.py
# Compiled at: 2013-04-04 15:36:37
from unittest import TestCase
from muntjac.ui.window import Window
from muntjac.application import Application

class AddRemoveSubWindow(TestCase):

    def testAddSubWindow(self):
        app = TestApp()
        app.init()
        subWindow = Window('Sub window')
        mainWindow = app.getMainWindow()
        mainWindow.addWindow(subWindow)
        self.assertEquals(subWindow.getParent(), mainWindow)
        try:
            mainWindow.addWindow(subWindow)
            self.assertTrue(False, 'Window.addWindow did not throw the expected exception')
        except ValueError:
            pass

        try:
            w = Window()
            w.addWindow(subWindow)
            self.assertTrue(False, 'Window.addWindow did not throw the expected exception')
        except ValueError:
            pass

    def testRemoveSubWindow(self):
        app = TestApp()
        app.init()
        subWindow = Window('Sub window')
        mainWindow = app.getMainWindow()
        mainWindow.addWindow(subWindow)
        self.assertEquals(subWindow.getParent(), mainWindow)
        removed = subWindow.removeWindow(subWindow)
        self.assertFalse(removed, 'Window was removed even though it should not have been')
        self.assertEquals(subWindow.getParent(), mainWindow)
        removed = mainWindow.removeWindow(subWindow)
        self.assertTrue(removed, 'Window was not removed correctly')
        self.assertEquals(subWindow.getParent(), None)
        return


class TestApp(Application):

    def init(self):
        w = Window('Main window')
        self.setMainWindow(w)