# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\samples\wx\wxapp.py
# Compiled at: 2016-04-18 03:12:47
# Size of source mod 2**32: 1202 bytes
import wx

class Frame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='Hello from cx_Freeze')
        panel = wx.Panel(self)
        closeMeButton = wx.Button(panel, -1, 'Close Me')
        wx.EVT_BUTTON(self, closeMeButton.GetId(), self.OnCloseMe)
        wx.EVT_CLOSE(self, self.OnCloseWindow)
        pushMeButton = wx.Button(panel, -1, 'Push Me')
        wx.EVT_BUTTON(self, pushMeButton.GetId(), self.OnPushMe)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(closeMeButton, flag=wx.ALL, border=20)
        sizer.Add(pushMeButton, flag=wx.ALL, border=20)
        panel.SetSizer(sizer)
        topSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer.Add(panel, flag=wx.ALL | wx.EXPAND)
        topSizer.Fit(self)

    def OnCloseMe(self, event):
        self.Close(True)

    def OnPushMe(self, event):
        wx.MessageBox('I was pushed!', 'Informational message')

    def OnCloseWindow(self, event):
        self.Destroy()


class App(wx.App):

    def OnInit(self):
        frame = Frame()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True


app = App(1)
app.MainLoop()