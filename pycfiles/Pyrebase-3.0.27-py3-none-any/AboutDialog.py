# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Pyreb\Dialogs\AboutDialog.py
# Compiled at: 2006-03-07 02:58:16
import wx
from wx.xrc import XRCCTRL

class PyrebAboutDialog(wx.Dialog):
    __module__ = __name__

    def __init__(self):
        p = wx.PreDialog()
        self.PostCreate(p)
        self.Bind(wx.EVT_BUTTON, self.OnCloseWindow)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, event):
        self.Destroy()