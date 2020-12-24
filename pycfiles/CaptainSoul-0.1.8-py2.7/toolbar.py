# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cptsoul/mainwindow/toolbar.py
# Compiled at: 2013-09-10 02:43:40
import gtk
from cptsoul.common import CptCommon

class ToolBar(gtk.Toolbar, CptCommon):

    def __init__(self):
        super(ToolBar, self).__init__()
        items = []
        coButton = gtk.ToolButton(gtk.STOCK_CONNECT)
        coButton.set_properties(tooltip_text='Connect', label='Connect')
        self._coButtonClicked = coButton.connect('clicked', self.manager.connectEvent)
        items.append(coButton)
        button = gtk.ToolButton(gtk.STOCK_PREFERENCES)
        button.set_properties(tooltip_text='Settings', label='Settings')
        button.connect('clicked', self.manager.openSettingsWindowEvent)
        items.append(button)
        items.append(gtk.SeparatorToolItem())
        button = gtk.ToolButton(gtk.STOCK_ADD)
        button.set_properties(tooltip_text='Add contact', label='Add contact')
        button.connect('clicked', self.manager.openAddContactWindowEvent)
        items.append(button)
        button = gtk.ToolButton(gtk.STOCK_SAVE)
        button.set_properties(tooltip_text='Downloads', label='Downloads')
        button.connect('clicked', self.openDownloadEvent)
        items.append(button)
        items.append(gtk.SeparatorToolItem())
        button = gtk.ToolButton(gtk.STOCK_QUIT)
        button.set_properties(tooltip_text='Quit', label='Quit')
        button.connect('clicked', self.manager.quitEvent)
        items.append(button)
        self.manager.connect('connecting', self.connectedEvent, coButton)
        self.manager.connect('reconnecting', self.connectedEvent, coButton)
        self.manager.connect('connected', self.connectedEvent, coButton)
        self.manager.connect('disconnected', self.disconnectedEvent, coButton)
        for n, item in enumerate(items):
            self.insert(item, n)

    def connectedEvent(self, widget, button):
        button.set_stock_id(gtk.STOCK_DISCONNECT)
        button.set_properties(tooltip_text='Disconnect', label='Disconnect')
        button.disconnect(self._coButtonClicked)
        self._coButtonClicked = button.connect('clicked', self.manager.disconnectEvent)

    def disconnectedEvent(self, widget, button):
        button.set_stock_id(gtk.STOCK_CONNECT)
        button.set_properties(tooltip_text='Connect', label='Connect')
        button.disconnect(self._coButtonClicked)
        self._coButtonClicked = button.connect('clicked', self.manager.connectEvent)

    def openDownloadEvent(self, widget):
        self.downloadManager.show_all()
        self.downloadManager.present()