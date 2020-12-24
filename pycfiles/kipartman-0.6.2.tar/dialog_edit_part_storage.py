# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: dialogs/dialog_edit_part_storage.py
# Compiled at: 2017-11-14 03:50:44
import wx, wx.xrc

class DialogEditPartStorage(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.Size(365, 184), style=wx.DEFAULT_DIALOG_STYLE)
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        bSizer4 = wx.BoxSizer(wx.VERTICAL)
        fgSizer2 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer2.AddGrowableCol(1)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, 'Storage', wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        fgSizer2.Add(self.m_staticText1, 1, wx.RIGHT | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
        self.button_storage = wx.Button(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BU_LEFT)
        fgSizer2.Add(self.button_storage, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, 'Quantity', wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        fgSizer2.Add(self.m_staticText2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.spin_quantity = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 99999999, 0)
        fgSizer2.Add(self.spin_quantity, 0, wx.ALL, 5)
        bSizer4.Add(fgSizer2, 1, wx.EXPAND, 5)
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_validate = wx.Button(self, wx.ID_OK, 'Add', wx.DefaultPosition, wx.DefaultSize, 0)
        self.button_validate.SetDefault()
        bSizer2.Add(self.button_validate, 0, wx.ALL, 5)
        self.button_cancel = wx.Button(self, wx.ID_CANCEL, 'Cancel', wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.button_cancel, 0, wx.ALL, 5)
        bSizer1.Add(bSizer2, 0, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 5)
        bSizer4.Add(bSizer1, 0, wx.EXPAND | wx.ALIGN_RIGHT, 5)
        self.SetSizer(bSizer4)
        self.Layout()
        self.Centre(wx.BOTH)
        self.button_storage.Bind(wx.EVT_BUTTON, self.onButtonPartStorageClick)
        self.button_validate.Bind(wx.EVT_BUTTON, self.onValidateClick)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancelClick)

    def __del__(self):
        pass

    def onButtonPartStorageClick(self, event):
        event.Skip()

    def onValidateClick(self, event):
        event.Skip()

    def onCancelClick(self, event):
        event.Skip()