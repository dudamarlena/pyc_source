# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: dialogs/panel_part_attachements.py
# Compiled at: 2017-11-14 10:49:59
import wx, wx.xrc, wx.dataview

class PanelPartAttachements(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(496, 385), style=wx.TAB_TRAVERSAL)
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        bSizer12 = wx.BoxSizer(wx.VERTICAL)
        bSizer11 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer10 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_add_attachement = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap('resources/add.png', wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW)
        bSizer10.Add(self.button_add_attachement, 0, wx.ALL, 5)
        self.button_edit_attachement = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap('resources/edit.png', wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW)
        bSizer10.Add(self.button_edit_attachement, 0, wx.ALL, 5)
        self.button_remove_attachement = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap('resources/remove.png', wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW)
        bSizer10.Add(self.button_remove_attachement, 0, wx.ALL, 5)
        bSizer11.Add(bSizer10, 1, wx.EXPAND, 5)
        bSizer12.Add(bSizer11, 0, wx.EXPAND, 5)
        self.tree_attachements = wx.dataview.DataViewCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer12.Add(self.tree_attachements, 1, wx.ALL | wx.EXPAND, 5)
        bSizer1.Add(bSizer12, 1, wx.EXPAND, 5)
        self.SetSizer(bSizer1)
        self.Layout()
        self.context_menu = wx.Menu()
        self.context_menu_open = wx.MenuItem(self.context_menu, wx.ID_ANY, 'Open', wx.EmptyString, wx.ITEM_NORMAL)
        self.context_menu.AppendItem(self.context_menu_open)
        self.button_add_attachement.Bind(wx.EVT_BUTTON, self.onButtonAddAttachementClick)
        self.button_edit_attachement.Bind(wx.EVT_BUTTON, self.onButtonEditAttachementClick)
        self.button_remove_attachement.Bind(wx.EVT_BUTTON, self.onButtonRemoveAttachementClick)
        self.Bind(wx.EVT_MENU, self.onContextMenuOpenSelection, id=self.context_menu_open.GetId())

    def __del__(self):
        pass

    def onButtonAddAttachementClick(self, event):
        event.Skip()

    def onButtonEditAttachementClick(self, event):
        event.Skip()

    def onButtonRemoveAttachementClick(self, event):
        event.Skip()

    def onContextMenuOpenSelection(self, event):
        event.Skip()