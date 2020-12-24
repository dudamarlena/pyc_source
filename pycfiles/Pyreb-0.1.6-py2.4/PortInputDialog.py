# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Pyreb\Dialogs\PortInputDialog.py
# Compiled at: 2006-12-09 08:13:58
import wx, string
from wx.xrc import XRCID, XRCCTRL

class IntValidator(wx.PyValidator):
    __module__ = __name__

    def __init__(self):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return IntValidator()

    def OnChar(self, event):
        key = event.KeyCode()
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
        if chr(key) in string.digits:
            event.Skip()
            return
        wx.Bell()

    def Validate(self, win):
        w = self.GetWindow()
        val = w.GetValue()
        try:
            int(val)
        except:
            return False

        return True

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True


class PyrebPortInputDialog(wx.Dialog):
    __module__ = __name__

    def __init__(self):
        p = wx.PreDialog()
        self.PostCreate(p)
        self.Bind(wx.EVT_BUTTON, self.OnCloseWindow, id=XRCID('ID_OK'))
        self.Bind(wx.EVT_INIT_DIALOG, self.OnInit, id=XRCID('PORTINPUT'))
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnInit(self, event):
        w = XRCCTRL(self, 'ID_PORT')
        w.SetValidator(IntValidator())

    def OnCloseWindow(self, event):
        self.PortCtrl = XRCCTRL(self, 'ID_PORT')
        assert self.PortCtrl, 'Cannot access port control'
        try:
            self.Port = int(self.PortCtrl.GetValue())
        except ValueError:
            txt = 'Invalid value for port: %s' % self.PortCtrl.GetValue()
            wx.MessageDialog(self, txt, 'Error', wx.OK | wx.ICON_ERROR).ShowModal()
            self.PortCtrl.SetValue('17787')
            return

        self.Destroy()