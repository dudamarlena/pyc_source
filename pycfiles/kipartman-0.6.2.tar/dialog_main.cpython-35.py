# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seb/git/kipartman/kipartman/dialogs/dialog_main.py
# Compiled at: 2017-11-14 10:48:48
# Size of source mod 2**32: 2356 bytes
import wx, wx.xrc

class DialogMain(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='Kipartman', pos=wx.DefaultPosition, size=wx.Size(1160, 686), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.menu_bar = wx.MenuBar(0)
        self.menu_view = wx.Menu()
        self.menu_view_configuration = wx.MenuItem(self.menu_view, wx.ID_ANY, 'Configuration', wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_view.AppendItem(self.menu_view_configuration)
        self.menu_bar.Append(self.menu_view, 'View')
        self.menu_help = wx.Menu()
        self.menu_about = wx.MenuItem(self.menu_help, wx.ID_ANY, 'About', wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_help.AppendItem(self.menu_about)
        self.menu_bar.Append(self.menu_help, 'Help')
        self.SetMenuBar(self.menu_bar)
        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)
        self.notebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer5.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(bSizer5)
        self.Layout()
        self.Centre(wx.BOTH)
        self.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)
        self.Bind(wx.EVT_MENU, self.onMenuViewConfigurationSelection, id=self.menu_view_configuration.GetId())
        self.Bind(wx.EVT_MENU, self.onMenuHelpAboutSelection, id=self.menu_about.GetId())
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onNotebookPageChanged)

    def __del__(self):
        pass

    def onKillFocus(self, event):
        event.Skip()

    def onMenuViewConfigurationSelection(self, event):
        event.Skip()

    def onMenuHelpAboutSelection(self, event):
        event.Skip()

    def onNotebookPageChanged(self, event):
        event.Skip()