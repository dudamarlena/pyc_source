# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \.\cx_Freeze\samples\wx\wxapp.py
# Compiled at: 2019-08-29 22:24:39
# Size of source mod 2**32: 1305 bytes
import wx

class Frame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, parent=None, title='Hello from cx_Freeze')
        panel = wx.Panel(self)
        closeMeButton = wx.Button(panel, -1, 'Close Me')
        self.Connect(closeMeButton.GetId(), -1, wx.EVT_BUTTON.typeId, self.OnCloseMe)
        self.Connect(self.GetId(), -1, wx.EVT_CLOSE.typeId, self.OnCloseWindow)
        pushMeButton = wx.Button(panel, -1, 'Push Me')
        self.Connect(pushMeButton.GetId(), -1, wx.EVT_BUTTON.typeId, self.OnPushMe)
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