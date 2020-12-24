# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/crystalDialog.py
# Compiled at: 2009-05-29 13:49:24
import wx

class CrystalDialog(wx.Dialog):
    """
    Dialog for inputting crystal structure information

    """

    def __init__(self, parent, winSize):
        self.parent = parent
        wx.Dialog.__init__(self, parent, size=winSize)
        self.crystalLabel = wx.StaticText(self, -1, 'Crystal Structure:')
        self.crystalRadio = wx.RadioBox(self, -1, '', wx.DefaultPosition, wx.DefaultSize, self.crystalData())
        self.btn_OK = wx.Button(self, wx.ID_OK)
        self.btn_Cancel = wx.Button(self, wx.ID_CANCEL)
        self.Bind(wx.EVT_RADIOBOX, self.OnCrystal, self.crystalRadio)
        self.__set_properties()
        self.__do_layout()

    def crystalData(self):
        return [
         'BCC', 'FCC', 'HCP']

    def OnCrystal(self, event):
        self.parent.controller.epscData.matParam['Phase1'].typeCrystal = self.crystalRadio.GetSelection()

    def __set_properties(self):
        self.SetTitle('Select Crystal Structure')
        self.parent.controller.epscData.matParam['Phase1'].typeCrystal = 0

    def __do_layout(self):
        sizer_top = wx.BoxSizer(wx.VERTICAL)
        sizer_contents = wx.FlexGridSizer(2, 1, 0, 0)
        sizer_btn = wx.BoxSizer(wx.HORIZONTAL)
        sizer_contents.Add(self.crystalLabel, 2, wx.ALL | wx.ALIGN_CENTER, 5)
        sizer_contents.Add(self.crystalRadio, 2, wx.ALL | wx.ALIGN_CENTER, 5)
        sizer_btn.Add(self.btn_OK, 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
        sizer_btn.Add(self.btn_Cancel, 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
        sizer_top.Add(sizer_contents, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_top.Add(sizer_btn, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_top)
        sizer_top.Fit(self)
        sizer_top.SetSizeHints(self)
        self.Layout()


if __name__ == '__main__':
    app = wx.PySimpleApp(0)
    crystalDialog = CrystalDialog(None, (300, 300))
    app.SetTopWindow(crystalDialog)
    crystalDialog.Show()
    app.MainLoop()