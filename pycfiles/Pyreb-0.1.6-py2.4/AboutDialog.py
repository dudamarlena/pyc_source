# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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