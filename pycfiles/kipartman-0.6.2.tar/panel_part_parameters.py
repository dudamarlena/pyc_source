# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: dialogs/panel_part_parameters.py
# Compiled at: 2018-04-29 12:38:28
import wx, wx.xrc, wx.dataview

class PanelPartParameters(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(496, 385), style=wx.TAB_TRAVERSAL)
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        bSizer12 = wx.BoxSizer(wx.VERTICAL)
        self.tree_parameters = wx.dataview.DataViewCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer12.Add(self.tree_parameters, 1, wx.ALL | wx.EXPAND, 5)
        bSizer1.Add(bSizer12, 1, wx.EXPAND, 5)
        self.SetSizer(bSizer1)
        self.Layout()
        self.menu_parameter = wx.Menu()
        self.menu_parameter_add_parameter = wx.MenuItem(self.menu_parameter, wx.ID_ANY, 'Add new parameter', wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_parameter_add_parameter.SetBitmap(wx.Bitmap('resources/add.png', wx.BITMAP_TYPE_ANY))
        self.menu_parameter.Append(self.menu_parameter_add_parameter)
        self.menu_parameter_edit_parameter = wx.MenuItem(self.menu_parameter, wx.ID_ANY, 'Edit parameter', wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_parameter_edit_parameter.SetBitmap(wx.Bitmap('resources/edit.png', wx.BITMAP_TYPE_ANY))
        self.menu_parameter.Append(self.menu_parameter_edit_parameter)
        self.menu_parameter_remove_parameter = wx.MenuItem(self.menu_parameter, wx.ID_ANY, 'Remove parameter', wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_parameter_remove_parameter.SetBitmap(wx.Bitmap('resources/remove.png', wx.BITMAP_TYPE_ANY))
        self.menu_parameter.Append(self.menu_parameter_remove_parameter)
        self.Bind(wx.EVT_RIGHT_DOWN, self.PanelPartParametersOnContextMenu)
        self.Bind(wx.EVT_MENU, self.onMenuParameterAddParameter, id=self.menu_parameter_add_parameter.GetId())
        self.Bind(wx.EVT_MENU, self.onMenuParameterEditParameter, id=self.menu_parameter_edit_parameter.GetId())
        self.Bind(wx.EVT_MENU, self.onMenuParameterRemoveParameter, id=self.menu_parameter_remove_parameter.GetId())

    def __del__(self):
        pass

    def onMenuParameterAddParameter(self, event):
        event.Skip()

    def onMenuParameterEditParameter(self, event):
        event.Skip()

    def onMenuParameterRemoveParameter(self, event):
        event.Skip()

    def PanelPartParametersOnContextMenu(self, event):
        self.PopupMenu(self.menu_parameter, event.GetPosition())