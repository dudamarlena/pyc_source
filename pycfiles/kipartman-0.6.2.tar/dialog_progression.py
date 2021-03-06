# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: dialogs/dialog_progression.py
# Compiled at: 2017-11-14 10:49:13
import wx, wx.xrc

class DialogProgression(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.Size(395, 164), style=wx.DEFAULT_DIALOG_STYLE)
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        bSizer14 = wx.BoxSizer(wx.VERTICAL)
        self.static_progression = wx.StaticText(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.static_progression.Wrap(-1)
        bSizer14.Add(self.static_progression, 0, wx.ALL | wx.EXPAND, 5)
        self.gauge_progression = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.gauge_progression.SetValue(0)
        bSizer14.Add(self.gauge_progression, 0, wx.ALL | wx.EXPAND, 5)
        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1Cancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbSizer1.AddButton(self.m_sdbSizer1Cancel)
        m_sdbSizer1.Realize()
        bSizer14.Add(m_sdbSizer1, 1, wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetSizer(bSizer14)
        self.Layout()
        self.Centre(wx.BOTH)
        self.m_sdbSizer1Cancel.Bind(wx.EVT_BUTTON, self.onCancelButtonClick)

    def __del__(self):
        pass

    def onCancelButtonClick(self, event):
        event.Skip()