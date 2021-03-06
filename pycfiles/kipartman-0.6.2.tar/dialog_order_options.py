# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: dialogs/dialog_order_options.py
# Compiled at: 2017-11-14 10:48:57
import wx, wx.xrc, wx.dataview

class DialogOrderOptions(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title='Order options', pos=wx.DefaultPosition, size=wx.Size(508, 540), style=wx.DEFAULT_DIALOG_STYLE)
        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        bSizer10 = wx.BoxSizer(wx.VERTICAL)
        self.checkbox_clean = wx.CheckBox(self, wx.ID_ANY, 'Clean current order list', wx.DefaultPosition, wx.DefaultSize, 0)
        self.checkbox_clean.SetValue(True)
        bSizer10.Add(self.checkbox_clean, 0, wx.ALL, 5)
        radiobox_distributorsChoices = [
         'Select best distributor', 'Select best prices']
        self.radiobox_distributors = wx.RadioBox(self, wx.ID_ANY, 'Distributors', wx.DefaultPosition, wx.DefaultSize, radiobox_distributorsChoices, 1, wx.RA_SPECIFY_COLS)
        self.radiobox_distributors.SetSelection(1)
        self.radiobox_distributors.Enable(False)
        self.radiobox_distributors.Hide()
        bSizer10.Add(self.radiobox_distributors, 0, wx.ALL, 5)
        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, 'Allowed distributors:', wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        bSizer10.Add(self.m_staticText5, 0, wx.ALL, 5)
        wSizer1 = wx.WrapSizer(wx.HORIZONTAL)
        self.check_select_all = wx.CheckBox(self, wx.ID_ANY, 'Select all', wx.DefaultPosition, wx.DefaultSize, 0)
        self.check_select_all.SetValue(True)
        wSizer1.Add(self.check_select_all, 0, wx.ALL, 5)
        self.check_select_none = wx.CheckBox(self, wx.ID_ANY, 'Select none', wx.DefaultPosition, wx.DefaultSize, 0)
        wSizer1.Add(self.check_select_none, 0, wx.ALL, 5)
        bSizer10.Add(wSizer1, 0, wx.EXPAND, 5)
        self.tree_distributors = wx.dataview.DataViewCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer10.Add(self.tree_distributors, 1, wx.ALL | wx.EXPAND, 5)
        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1OK = wx.Button(self, wx.ID_OK)
        m_sdbSizer1.AddButton(self.m_sdbSizer1OK)
        self.m_sdbSizer1Cancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbSizer1.AddButton(self.m_sdbSizer1Cancel)
        m_sdbSizer1.Realize()
        bSizer10.Add(m_sdbSizer1, 0, wx.EXPAND, 5)
        self.SetSizer(bSizer10)
        self.Layout()
        self.Centre(wx.BOTH)
        self.check_select_all.Bind(wx.EVT_CHECKBOX, self.onCheckSelectAll)
        self.check_select_none.Bind(wx.EVT_CHECKBOX, self.onCheckSelectNone)
        self.m_sdbSizer1Cancel.Bind(wx.EVT_BUTTON, self.OnCancelButtonClick)
        self.m_sdbSizer1OK.Bind(wx.EVT_BUTTON, self.OnOKButtonClick)

    def __del__(self):
        pass

    def onCheckSelectAll(self, event):
        event.Skip()

    def onCheckSelectNone(self, event):
        event.Skip()

    def OnCancelButtonClick(self, event):
        event.Skip()

    def OnOKButtonClick(self, event):
        event.Skip()