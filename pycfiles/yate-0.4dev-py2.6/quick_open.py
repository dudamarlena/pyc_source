# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yate/quick_open.py
# Compiled at: 2012-01-24 15:40:02
import wx, difflib, ngram

class QuickOpenDialog(wx.Dialog):
    MAX_FILES_TO_SHOW = 20

    def __init__(self, parent, files, G):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, 'Quick Open')
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox)
        self.filename = wx.TextCtrl(panel)
        self.fileList = wx.ListBox(panel)
        self.files = files
        if not G:
            self.G = ngram.NGram(self.files)
        else:
            self.G = G
        self.fileList.SetItems(self.files[:QuickOpenDialog.MAX_FILES_TO_SHOW])
        self.Bind(wx.EVT_TEXT, self.OnChange, self.filename)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelect, self.fileList)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyDown)
        vbox.Add(self.filename, 0, wx.EXPAND)
        vbox.Add(self.fileList, 1, wx.EXPAND)
        self.filename.SetFocus()
        self.fileToOpen = None
        self.CenterOnScreen()
        return

    def OnSelect(self, event):
        self.OpenSelected()

    def OpenSelected(self):
        self.fileToOpen = self.fileList.GetStringSelection()
        self.EndModal(wx.ID_OK)

    def OnChange(self, event):
        value = self.filename.GetValue()
        if len(value) == 0:
            self.fileList.SetItems(self.files[:QuickOpenDialog.MAX_FILES_TO_SHOW])
        else:
            files = self.G.search(value)
            self.fileList.SetItems([ f[0] for f in files[:QuickOpenDialog.MAX_FILES_TO_SHOW] ])
            if len(files) > 0:
                self.fileList.SetSelection(0)

    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_OK)
        elif keycode == wx.WXK_RETURN:
            self.OpenSelected()
        elif keycode == wx.WXK_DOWN and wx.Window.FindFocus() == self.filename:
            self.fileList.SetFocus()
        elif keycode == wx.WXK_UP and wx.Window.FindFocus() == self.fileList and self.fileList.GetSelection() == 0:
            self.filename.SetFocus()
        else:
            event.Skip()