# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\IDE\CDeclar_Menber.py
# Compiled at: 2020-01-16 00:50:14
import wx, wx.xrc, wx.stc as stc
from CLogText import LogText

class Panel_Declare(wx.Panel):

    def __init__(self, parent, hanndel):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(600, 800), style=wx.TAB_TRAVERSAL)
        self.parent = hanndel
        bz = wx.BoxSizer(wx.VERTICAL)
        self.m_toolBar = wx.ToolBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)
        self.m_tool_save = self.m_toolBar.AddTool(wx.ID_ANY, 'tool', wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)
        self.m_tool_refresh = self.m_toolBar.AddTool(wx.ID_ANY, 'tool', wx.ArtProvider.GetBitmap(wx.ART_GO_TO_PARENT), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)
        self.m_toolBar.AddSeparator()
        self.m_tool_add = self.m_toolBar.AddTool(wx.ID_ANY, 'tool', wx.ArtProvider.GetBitmap(wx.ART_ADD_BOOKMARK), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)
        self.m_tool_delete = self.m_toolBar.AddTool(wx.ID_ANY, 'tool', wx.ArtProvider.GetBitmap(wx.ART_DEL_BOOKMARK), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)
        self.m_toolBar.AddSeparator()
        self.m_tool_up = self.m_toolBar.AddTool(wx.ID_ANY, 'tool', wx.ArtProvider.GetBitmap(wx.ART_GO_UP), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)
        self.m_tool_dn = self.m_toolBar.AddTool(wx.ID_ANY, 'tool', wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)
        self.m_toolBar.Realize()
        bz.Add(self.m_toolBar, 0, wx.EXPAND, 5)
        self.list = CustListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_HRULES | wx.LC_VRULES)
        bz.Add(self.list, 1, wx.ALL | wx.EXPAND, 0)
        self.SetSizer(bz)
        self.Layout()
        self.Bind(wx.EVT_TOOL, self.OnSave, id=self.m_tool_save.GetId())
        self.Bind(wx.EVT_TOOL, self.OnAdd, id=self.m_tool_add.GetId())
        self.Bind(wx.EVT_TOOL, self.OnDelete, id=self.m_tool_delete.GetId())
        self.Bind(wx.EVT_TOOL, self.OnUp, id=self.m_tool_up.GetId())
        self.Bind(wx.EVT_TOOL, self.OnDn, id=self.m_tool_dn.GetId())
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
        return

    def __del__(self):
        pass

    def OnSave(self, event):
        self.parent.SavePage(self.savedata())
        event.Skip()

    def OnAdd(self, event):
        index = self.list.InsertItem(self.list.GetItemCount(), '')
        self.list.SetItemData(index, index)
        event.Skip()

    def OnDelete(self, event):
        print self.currentItem
        self.list.DeleteItem(self.currentItem)
        event.Skip()

    def OnUp(self, event):
        event.Skip()

    def OnDn(self, event):
        event.Skip()

    def OnItemSelected(self, event):
        self.currentItem = event.Index
        print self.currentItem
        event.Skip()

    def savedata(self):
        data = []
        _lenth = self.list.GetItemCount()
        _cols = self.list.GetColumnCount()
        for i in xrange(_lenth):
            lt = []
            for j in xrange(_cols):
                v = self.list.GetItem(i, j).GetText()
                lt.append(v)

            data.append(lt)

        return data

    def renderdata(self, data):
        for i in xrange(len(data)):
            index = self.list.InsertItem(self.list.GetItemCount(), data[i][0])
            for j in range(1, min(self.list.GetColumnCount(), len(data[i]))):
                self.list.SetItem(index, j, data[i][j])


import sys, wx, wx.lib.mixins.listctrl as listmix

class CustListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.TextEditMixin):

    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.Populate()
        listmix.TextEditMixin.__init__(self)

    def Populate(self):
        self.InsertColumn(0, 'name')
        self.InsertColumn(1, 'data type')
        self.InsertColumn(2, 'array lenth', wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(3, 'default value')
        self.InsertColumn(4, 'comment')
        self.currentItem = 0