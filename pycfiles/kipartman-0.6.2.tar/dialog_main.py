# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: dialogs/dialog_main.py
# Compiled at: 2018-07-16 12:07:24
import wx, wx.xrc

class DialogMain(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='Kipartman', pos=wx.DefaultPosition, size=wx.Size(1160, 686), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.menu_bar = wx.MenuBar(0)
        self.menu_file = wx.Menu()
        self.menu_file_project = wx.MenuItem(self.menu_file, wx.ID_ANY, 'Open project', wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_file.Append(self.menu_file_project)
        self.menu_file.AppendSeparator()
        self.menu_buy_parts = wx.MenuItem(self.menu_file, wx.ID_ANY, 'Buy parts', 'Open the buy parts window', wx.ITEM_NORMAL)
        self.menu_file.Append(self.menu_buy_parts)
        self.menu_bar.Append(self.menu_file, 'File')
        self.menu_view = wx.Menu()
        self.menu_view_configuration = wx.MenuItem(self.menu_view, wx.ID_ANY, 'Configuration', wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_view.Append(self.menu_view_configuration)
        self.menu_bar.Append(self.menu_view, 'View')
        self.menu_help = wx.Menu()
        self.menu_about = wx.MenuItem(self.menu_help, wx.ID_ANY, 'About', wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_help.Append(self.menu_about)
        self.menu_bar.Append(self.menu_help, 'Help')
        self.SetMenuBar(self.menu_bar)
        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)
        self.notebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer5.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)
        self.info = wx.InfoBar(self)
        self.info.SetShowHideEffects(wx.SHOW_EFFECT_NONE, wx.SHOW_EFFECT_NONE)
        self.info.SetEffectDuration(500)
        bSizer5.Add(self.info, 0, wx.ALL, 5)
        self.SetSizer(bSizer5)
        self.Layout()
        self.status = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)
        self.Centre(wx.BOTH)
        self.Bind(wx.EVT_KILL_FOCUS, self.onKillFocus)
        self.Bind(wx.EVT_MENU, self.onMenuFileProjetSelection, id=self.menu_file_project.GetId())
        self.Bind(wx.EVT_MENU, self.onMenuBuyPartsSelection, id=self.menu_buy_parts.GetId())
        self.Bind(wx.EVT_MENU, self.onMenuViewConfigurationSelection, id=self.menu_view_configuration.GetId())
        self.Bind(wx.EVT_MENU, self.onMenuHelpAboutSelection, id=self.menu_about.GetId())
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onNotebookPageChanged)

    def __del__(self):
        pass

    def onKillFocus(self, event):
        event.Skip()

    def onMenuFileProjetSelection(self, event):
        event.Skip()

    def onMenuBuyPartsSelection(self, event):
        event.Skip()

    def onMenuViewConfigurationSelection(self, event):
        event.Skip()

    def onMenuHelpAboutSelection(self, event):
        event.Skip()

    def onNotebookPageChanged(self, event):
        event.Skip()