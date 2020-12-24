# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\IDE\CDeclar_Task.py
# Compiled at: 2020-01-14 23:39:42
import wx, wx.xrc, wx.stc as stc
from CLogText import LogText

class Panel_Task(wx.Panel):

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
        bzSet = wx.BoxSizer(wx.HORIZONTAL)
        label11 = wx.StaticText(self, wx.ID_ANY, '扫描时间(ms)', wx.DefaultPosition, wx.DefaultSize, 0)
        label11.Wrap(-1)
        bzSet.Add(label11, 0, wx.ALL, 5)
        self.m_text_scantime = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bzSet.Add(self.m_text_scantime, 0, wx.ALL, 5)
        bz.Add(bzSet, 0, wx.EXPAND, 5)
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

        dc = {'scantime': self.m_text_scantime.GetValue(), 
           'list': data}
        return dc

    def renderdata(self, data):
        if data.has_key('scantime') == False:
            self.m_text_scantime.SetValue('0')
            return
        self.m_text_scantime.SetValue(data['scantime'])
        for i in xrange(len(data['list'])):
            index = self.list.InsertItem(self.list.GetItemCount(), data['list'][i][0])
            for j in range(1, len(data['list'][i])):
                self.list.SetItem(index, j, data['list'][i][j])


import sys, wx, wx.lib.mixins.listctrl as listmix

class CustListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.TextEditMixin):

    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.Populate()
        listmix.TextEditMixin.__init__(self)

    def Populate(self):
        self.InsertColumn(0, 'program name')
        self.InsertColumn(1, '')
        self.currentItem = 0