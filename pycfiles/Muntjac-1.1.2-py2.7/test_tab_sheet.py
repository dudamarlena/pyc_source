# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/component/test_tab_sheet.py
# Compiled at: 2013-04-04 15:36:37
from unittest import TestCase
from muntjac.ui.label import Label
from muntjac.ui.tab_sheet import TabSheet

class TestTabSheet(TestCase):

    def testAddExistingComponent(self):
        c = Label('abc')
        tabSheet = TabSheet()
        tabSheet.addComponent(c)
        tabSheet.addComponent(c)
        itr = tabSheet.getComponentIterator()
        self.assertEquals(c, itr.next())
        self.assertRaises(StopIteration, itr.next)
        self.assertNotEquals(tabSheet.getTab(c), None)
        return

    def testGetComponentFromTab(self):
        c = Label('abc')
        tabSheet = TabSheet()
        tab = tabSheet.addTab(c)
        self.assertEquals(c, tab.getComponent())

    def testAddTabWithComponentOnly(self):
        tabSheet = TabSheet()
        tab1 = tabSheet.addTab(Label('aaa'))
        tab2 = tabSheet.addTab(Label('bbb'))
        tab3 = tabSheet.addTab(Label('ccc'))
        self.assertEquals(0, tabSheet.getTabPosition(tab1))
        self.assertEquals(1, tabSheet.getTabPosition(tab2))
        self.assertEquals(2, tabSheet.getTabPosition(tab3))
        tabSheet.addTab(tab1.getComponent())
        self.assertEquals(0, tabSheet.getTabPosition(tab1))
        self.assertEquals(1, tabSheet.getTabPosition(tab2))
        self.assertEquals(2, tabSheet.getTabPosition(tab3))

    def testAddTabWithComponentAndIndex(self):
        tabSheet = TabSheet()
        tab1 = tabSheet.addTab(Label('aaa'))
        tab2 = tabSheet.addTab(Label('bbb'))
        tab3 = tabSheet.addTab(Label('ccc'))
        tab4 = tabSheet.addTab(Label('ddd'), 1)
        tab5 = tabSheet.addTab(Label('eee'), 3)
        self.assertEquals(0, tabSheet.getTabPosition(tab1))
        self.assertEquals(1, tabSheet.getTabPosition(tab4))
        self.assertEquals(2, tabSheet.getTabPosition(tab2))
        self.assertEquals(3, tabSheet.getTabPosition(tab5))
        self.assertEquals(4, tabSheet.getTabPosition(tab3))
        tabSheet.addTab(tab1.getComponent(), 3)
        self.assertEquals(0, tabSheet.getTabPosition(tab1))
        self.assertEquals(1, tabSheet.getTabPosition(tab4))
        self.assertEquals(2, tabSheet.getTabPosition(tab2))
        self.assertEquals(3, tabSheet.getTabPosition(tab5))
        self.assertEquals(4, tabSheet.getTabPosition(tab3))

    def testAddTabWithAllParameters(self):
        tabSheet = TabSheet()
        tab1 = tabSheet.addTab(Label('aaa'))
        tab2 = tabSheet.addTab(Label('bbb'))
        tab3 = tabSheet.addTab(Label('ccc'))
        tab4 = tabSheet.addTab(Label('ddd'), 'ddd', None, 1)
        tab5 = tabSheet.addTab(Label('eee'), 'eee', None, 3)
        self.assertEquals(0, tabSheet.getTabPosition(tab1))
        self.assertEquals(1, tabSheet.getTabPosition(tab4))
        self.assertEquals(2, tabSheet.getTabPosition(tab2))
        self.assertEquals(3, tabSheet.getTabPosition(tab5))
        self.assertEquals(4, tabSheet.getTabPosition(tab3))
        tabSheet.addTab(tab1.getComponent(), 'xxx', None, 3)
        self.assertEquals(0, tabSheet.getTabPosition(tab1))
        self.assertEquals(1, tabSheet.getTabPosition(tab4))
        self.assertEquals(2, tabSheet.getTabPosition(tab2))
        self.assertEquals(3, tabSheet.getTabPosition(tab5))
        self.assertEquals(4, tabSheet.getTabPosition(tab3))
        return

    def testGetTabByPosition(self):
        tabSheet = TabSheet()
        tab1 = tabSheet.addTab(Label('aaa'))
        tab2 = tabSheet.addTab(Label('bbb'))
        tab3 = tabSheet.addTab(Label('ccc'))
        self.assertEquals(tab1, tabSheet.getTab(0))
        self.assertEquals(tab2, tabSheet.getTab(1))
        self.assertEquals(tab3, tabSheet.getTab(2))