# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: frames/dropdown_frame.py
# Compiled at: 2017-11-14 10:50:54
import wx

class DropdownFrame(wx.PopupTransientWindow):
    """
    Display a popup frame
    """

    def __init__(self, parent, frame, initial=None):
        """
        Create a popup window from frame
        :param parent: owner
        :param frame: type of frame to create
        :param initial: item to select by default
        Frame should contain a SetResult method allowing to set result and cancel callback 
        """
        super(DropdownFrame, self).__init__(parent)
        self.panel = frame(self, initial)
        self.SetSize(self.panel.GetSize())
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND, 5)
        self.SetSizer(sizer)
        self.Layout()

    def Dropdown(self, result_callback):
        pos = self.Parent.GetScreenPosition()
        pos.y = pos.y + self.Parent.GetSize().y
        screenSize = wx.Display(0).GetGeometry().GetSize()
        if pos.y + self.panel.GetSize().y > screenSize.y:
            pos.y = screenSize.y - self.panel.GetSize().y
        if pos.x + self.panel.GetSize().x > screenSize.x:
            pos.x = screenSize.x - self.panel.GetSize().x
        self.panel.SetResult(self.result, self.cancel)
        self.result_callback = result_callback
        self.SetPosition(pos)
        self.Popup()

    def result(self, data):
        self.result_callback(data)
        self.Destroy()

    def cancel(self):
        self.Destroy()