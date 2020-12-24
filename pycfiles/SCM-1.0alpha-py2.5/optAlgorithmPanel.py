# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/optAlgorithmPanel.py
# Compiled at: 2009-05-29 13:49:10
import wx
from SCMPanel import SCMPanel

class OptAlgorithm(wx.Panel, SCMPanel):
    """
        Panel for choice of optimization algorithm
        ==> leastsq, fmin, bounded-fmin
    """

    def __init__(self, *args, **kwds):
        SCMPanel.__init__(self, *args, **kwds)
        wx.Panel.__init__(self, *args, **kwds)
        self.selectedAlgorithm = 0
        self.radio_box_algorithm = wx.RadioBox(self, -1, 'Algorithm', choices=['leastsq(Levenberg-Marquardt)', 'fmin(Simplex)', 'boxmin(Constrained Simplex)', 'fmin-mystic', 'Differential Evolution'], majorDimension=4, style=wx.RA_SPECIFY_COLS)
        self.button_OK = wx.Button(self, -1, 'OK')
        self.button_Cancel = wx.Button(self, -1, 'Cancel')
        self.Bind(wx.EVT_RADIOBOX, self.OnRadio, self.radio_box_algorithm)
        self.Bind(wx.EVT_BUTTON, self.OnOK, self.button_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.button_Cancel)
        self.__set_properties()
        self.__do_layout()

    def name_algorithm(self):
        return {'leastsq': 0, 'fmin': 1, 'boxmin': 2, 'fmin-mystic': 3, 'de': 4}

    def showData(self):
        self.radio_box_algorithm.SetSelection(self.name_algorithm()[self.controller.epscData.optData.nameAlgorithm])

    def OnRadio(self, event):
        self.selectedAlgorithm = event.GetInt()

    def OnOK(self, event):
        if self.selectedAlgorithm == 0:
            self.controller.epscData.optData.nameAlgorithm = 'leastsq'
            if self.controller.epscData.matParam['Phase1'].typeCrystal == 0:
                self.Parent.optBCC.disableRanges()
            elif self.controller.epscData.matParam['Phase1'].typeCrystal == 1:
                self.Parent.optFCC.disableRanges()
            else:
                self.Parent.optHCP.disableRanges()
        elif self.selectedAlgorithm == 1:
            self.controller.epscData.optData.nameAlgorithm = 'fmin'
            if self.controller.epscData.matParam['Phase1'].typeCrystal == 0:
                self.Parent.optBCC.disableRanges()
            elif self.controller.epscData.matParam['Phase1'].typeCrystal == 1:
                self.Parent.optFCC.disableRanges()
            else:
                self.Parent.optHCP.disableRanges()
        elif self.selectedAlgorithm == 2:
            self.controller.epscData.optData.nameAlgorithm = 'boxmin'
            if self.controller.epscData.matParam['Phase1'].typeCrystal == 0:
                self.Parent.optBCC.enableRanges()
            elif self.controller.epscData.matParam['Phase1'].typeCrystal == 1:
                self.Parent.optFCC.enableRanges()
            else:
                self.Parent.optHCP.enableRanges()
        elif self.selectedAlgorithm == 3:
            self.controller.epscData.optData.nameAlgorithm = 'fmin-mystic'
            if self.controller.epscData.matParam['Phase1'].typeCrystal == 0:
                self.Parent.optBCC.enableRanges()
            elif self.controller.epscData.matParam['Phase1'].typeCrystal == 1:
                self.Parent.optFCC.enableRanges()
            else:
                self.Parent.optHCP.enableRanges()
        elif self.selectedAlgorithm == 4:
            self.controller.epscData.optData.nameAlgorithm = 'de'
            if self.controller.epscData.matParam['Phase1'].typeCrystal == 0:
                self.Parent.optBCC.enableRanges()
            elif self.controller.epscData.matParam['Phase1'].typeCrystal == 1:
                self.Parent.optFCC.enableRanges()
            else:
                self.Parent.optHCP.enableRanges()
        self.controller.epscData.optData.turnOnFlag('optAlgorithm')
        self.treePanel.turnOnOptNode(0)

    def OnCancel(self, event):
        self.radio_box_algorithm.SetSelection(0)
        self.controller.epscData.optData.turnOffFlag('optAlgorithm')
        self.treePanel.turnOffOptNode(0)

    def __set_properties(self):
        self.SetSize((547, 253))
        self.radio_box_algorithm.SetSelection(0)

    def __do_layout(self):
        sizer_top = wx.BoxSizer(wx.VERTICAL)
        sizer_OK = wx.BoxSizer(wx.HORIZONTAL)
        sizer_btn = wx.BoxSizer(wx.HORIZONTAL)
        sizer_top.Add(self.radio_box_algorithm, 0, wx.ALL | wx.EXPAND | wx.ADJUST_MINSIZE, 2)
        sizer_btn.Add((20, 20), 1, wx.ADJUST_MINSIZE, 0)
        sizer_btn.Add((20, 20), 0, wx.ADJUST_MINSIZE, 0)
        sizer_top.Add(sizer_btn, 0, wx.ALL | wx.EXPAND, 2)
        sizer_OK.Add((20, 20), 1, wx.ADJUST_MINSIZE, 0)
        sizer_OK.Add(self.button_OK, 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
        sizer_OK.Add(self.button_Cancel, 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
        sizer_top.Add(sizer_OK, 0, wx.ALL | wx.EXPAND, 2)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_top)


if __name__ == '__main__':
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = (None, -1, '')
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()