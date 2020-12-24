# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_dialogs/epilogue.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 3186 bytes
import wx

class Formula(wx.Dialog):
    __doc__ = '\n   Show an final dialog box before run process. It accept a\n   couple of tuples which represent the formula names with\n   corresponding diction names:\n\n   Example:\n            formula = ("\nEXAMPLES:\n\\nExample 1:\nExample 2:\n etc."\n            diction = ("type 1\ntype 2\ntype 3\n etc."\n    '

    def __init__(self, parent, formula, diction, title):
        wx.Dialog.__init__(self, parent, (-1), style=(wx.DEFAULT_DIALOG_STYLE))
        panel = wx.Panel(self, (wx.ID_ANY), style=(wx.TAB_TRAVERSAL))
        label1 = wx.StaticText(panel, wx.ID_ANY, formula)
        label2 = wx.StaticText(panel, wx.ID_ANY, diction)
        self.button_1 = wx.Button(self, wx.ID_CANCEL, '')
        self.button_2 = wx.Button(self, wx.ID_OK, '')
        self.SetTitle(title)
        label2.SetForegroundColour(wx.Colour(255, 106, 249))
        s1 = wx.BoxSizer(wx.VERTICAL)
        gr_s1 = wx.FlexGridSizer(1, 2, 0, 0)
        gr_s1.Add(label1, 0, wx.ALL, 5)
        gr_s1.Add(label2, 0, wx.ALL, 5)
        btngrid = wx.FlexGridSizer(1, 2, 0, 0)
        btngrid.Add(self.button_1, 0, wx.ALL, 5)
        btngrid.Add(self.button_2, 0, wx.ALL, 5)
        panel.SetSizer(gr_s1)
        s1.Add(panel, 1, wx.ALL | wx.EXPAND, 10)
        s1.Add(btngrid, flag=(wx.ALL | wx.ALIGN_RIGHT | wx.RIGHT), border=10)
        self.SetSizer(s1)
        s1.Fit(self)
        self.Layout()
        self.Bind(wx.EVT_BUTTON, self.on_cancel, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.on_ok, self.button_2)

    def on_cancel(self, event):
        event.Skip()

    def on_ok(self, event):
        event.Skip()