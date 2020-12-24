# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/hklDialog.py
# Compiled at: 2009-05-29 13:49:21
import wx

class HKLDialog(wx.Dialog):
    """
       Dialog for selecting HKL data for optimization
    """

    def __init__(self, parent, winSize):
        wx.Dialog.__init__(self, parent, size=winSize)
        self.epscData = parent.controller.epscData
        if self.epscData.phaseNum != 2022 and self.epscData.phaseNum != 2032:
            self.phase = 'Phase1'
        else:
            self.phase = 'Phase2'
        self.chkbox = []
        listHKL = []
        for i in range(self.epscData.numDiffractionData[self.phase]):
            listHKL.append(str(self.epscData.listDiffractionData[self.phase][i].name) + '_' + self.epscData.listDiffractionData[self.phase][i].angle)

        self.chkHKL = wx.CheckListBox(self, -1, (80, 60), wx.DefaultSize, listHKL)
        for i in range(self.epscData.numDiffractionData[self.phase]):
            if self.epscData.listDiffractionData[self.phase][i].flagOn == True:
                self.chkHKL.Check(i)

        self.btn_OK = wx.Button(self, -1, 'OK')
        self.btn_Cancel = wx.Button(self, -1, 'Cancel')
        self.Bind(wx.EVT_CHECKLISTBOX, self.OnHKL, self.chkHKL)
        self.Bind(wx.EVT_BUTTON, self.OnOK, self.btn_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.btn_Cancel)
        self.__set_properties()
        self.__do_layout()

    def OnHKL(self, event):
        index = event.GetSelection()
        if self.chkHKL.IsChecked(index):
            self.epscData.listDiffractionData[self.phase][index].flagOn = True
        else:
            self.epscData.listDiffractionData[self.phase][index].flagOn = False

    def OnOK(self, event):
        self.Close()

    def OnCancel(self, event):
        self.Close()

    def __set_properties(self):
        self.SetTitle('Select HKLs')

    def __do_layout(self):
        sizer_top = wx.BoxSizer(wx.VERTICAL)
        sizer_btn = wx.BoxSizer(wx.HORIZONTAL)
        sizer_top.Add(self.chkHKL, 2, wx.ALIGN_CENTER | wx.ALL, 5)
        sizer_btn.Add(self.btn_OK, 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
        sizer_btn.Add(self.btn_Cancel, 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
        sizer_top.Add(sizer_btn, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_top)
        sizer_top.Fit(self)
        sizer_top.SetSizeHints(self)
        self.Layout()


if __name__ == '__main__':
    app = wx.PySimpleApp(0)
    hklDialog = HKLDialog(None, 1)
    app.SetTopWindow(hklDialog)
    hklDialog.Show()
    app.MainLoop()