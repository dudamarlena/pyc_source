# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/tabsheets/TabSheetClosingExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Label, TabSheet
from muntjac.ui import tab_sheet

class TabSheetClosingExample(VerticalLayout, tab_sheet.ISelectedTabChangeListener, tab_sheet.ICloseHandler):

    def __init__(self):
        super(TabSheetClosingExample, self).__init__()
        l1 = VerticalLayout()
        l1.setMargin(True)
        l1.addComponent(Label('There are no previously saved actions.'))
        l2 = VerticalLayout()
        l2.setMargin(True)
        l2.addComponent(Label('There are no saved notes.'))
        l3 = VerticalLayout()
        l3.setMargin(True)
        l3.addComponent(Label('There are currently no issues.'))
        l4 = VerticalLayout()
        l4.setMargin(True)
        l4.addComponent(Label('There are no comments.'))
        l5 = VerticalLayout()
        l5.setMargin(True)
        l5.addComponent(Label('There is no new feedback.'))
        self._t = TabSheet()
        self._t.setHeight('200px')
        self._t.setWidth('400px')
        saved = self._t.addTab(l1, 'Saved actions', None)
        saved.setClosable(True)
        notes = self._t.addTab(l2, 'Notes', None)
        notes.setClosable(True)
        issues = self._t.addTab(l3, 'Issues', None)
        issues.setClosable(True)
        comments = self._t.addTab(l4, 'Comments', None)
        comments.setClosable(True)
        feedback = self._t.addTab(l5, 'Feedback', None)
        feedback.setClosable(True)
        self._t.addListener(self, tab_sheet.ISelectedTabChangeListener)
        self._t.setCloseHandler(self)
        self.addComponent(self._t)
        return

    def selectedTabChange(self, event):
        tabsheet = event.getTabSheet()
        tab = tabsheet.getTab(tabsheet.getSelectedTab())
        if tab is not None:
            self.getWindow().showNotification('Selected tab: ' + tab.getCaption())
        return

    def onTabClose(self, tabsheet, tabContent):
        self.getWindow().showNotification('Closed tab: ' + tabsheet.getTab(tabContent).getCaption())
        tabsheet.removeComponent(tabContent)