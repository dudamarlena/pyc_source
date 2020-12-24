# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/optHCPDataPanel.py
# Compiled at: 2009-05-29 13:49:24
import wx
from hklDialog import HKLDialog
from SCMPanel import SCMPanel

class OptHCPDataPanel(wx.ScrolledWindow, SCMPanel):
    """
    Optimization data input panel for HCP structure
    Selection of macro and hkl.
    Low and high values for bounded optimization
    """

    def __init__(self, *args, **kwds):
        SCMPanel.__init__(self, *args, **kwds)
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self.controller = self.Parent.Parent.controller
        self.sizer_Model_staticbox = wx.StaticBox(self, -1, 'Model Parameters Setting')
        self.sizer_Experiment_staticbox = wx.StaticBox(self, -1, 'Experiment Data Setting')
        self.chkbox_macro = wx.CheckBox(self, -1, 'Macro (Extensometer)')
        self.chkbox_hkl = wx.CheckBox(self, -1, 'HKL (Neutron)')
        self.button_HKL = wx.Button(self, -1, 'Select HKLs')
        self.static_line_1 = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)
        self.sizer_slip_staticbox = []
        self.sizer_slip_staticbox.append(wx.StaticBox(self, -1, 'BASAL'))
        self.sizer_slip_staticbox.append(wx.StaticBox(self, -1, 'PRSM1ORD'))
        self.sizer_slip_staticbox.append(wx.StaticBox(self, -1, 'PRSM2ORD'))
        self.sizer_slip_staticbox.append(wx.StaticBox(self, -1, 'PYR1ORDA'))
        self.sizer_slip_staticbox.append(wx.StaticBox(self, -1, 'PYR1C+A'))
        self.sizer_slip_staticbox.append(wx.StaticBox(self, -1, 'PYR2ORDR'))
        self.sizer_slip_staticbox.append(wx.StaticBox(self, -1, 'PYR_COMP_TWIN'))
        self.sizer_slip_staticbox.append(wx.StaticBox(self, -1, 'PYR_TENS_TWIN'))
        self.chbox_voce = [[], [], [], [], [], [], [], []]
        self.label_name_voce = []
        self.label_initial_voce = []
        self.label_low_voce = []
        self.label_high_voce = []
        self.text_initial_voce = [[], [], [], [], [], [], [], []]
        self.text_low_voce = [[], [], [], [], [], [], [], []]
        self.text_high_voce = [[], [], [], [], [], [], [], []]
        self.nameVoce = ['Tau Zero', 'Tau One', 'Theta Zero', 'Theta One']
        for i in range(8):
            self.label_name_voce.append(wx.StaticText(self, -1, 'Name '))
            self.label_initial_voce.append(wx.StaticText(self, -1, 'Initial '))
            self.label_low_voce.append(wx.StaticText(self, -1, 'Low '))
            self.label_high_voce.append(wx.StaticText(self, -1, 'High '))
            for j in range(4):
                self.chbox_voce[i].append(wx.CheckBox(self, -1, self.nameVoce[j]))
                self.text_initial_voce[i].append(wx.TextCtrl(self, -1, size=(50, -1)))
                self.text_low_voce[i].append(wx.TextCtrl(self, -1, size=(50, -1)))
                self.text_high_voce[i].append(wx.TextCtrl(self, -1, size=(50, -1)))
                self.text_initial_voce[i][j].Enable(False)

        self.button_OK = wx.Button(self, -1, 'OK')
        self.button_Cancel = wx.Button(self, -1, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.OnOK, self.button_OK)
        self.Bind(wx.EVT_BUTTON, self.OnHKL, self.button_HKL)
        self.Bind(wx.EVT_CHECKBOX, self.OnChkHKL, self.chkbox_hkl)
        self.__set_properties()
        self.__do_layout()

    def disableRanges(self):
        for i in range(8):
            for j in range(4):
                self.text_low_voce[i][j].Enable(False)
                self.text_high_voce[i][j].Enable(False)

    def enableRanges(self):
        for i in range(8):
            for j in range(4):
                self.text_low_voce[i][j].Enable(True)
                self.text_high_voce[i][j].Enable(True)

    def showData(self):
        if self.controller.epscData.optData.getData('expData') == 'macro':
            self.chkbox_macro.SetValue(True)
        elif self.controller.epscData.optData.getData('expData') == 'hkl':
            self.chkbox_hkl.SetValue(True)
        elif self.controller.epscData.optData.getData('expData') == 'both':
            self.chkbox_macro.SetValue(True)
            self.chkbox_hkl.SetValue(True)
        for i in range(8):
            for j in range(4):
                self.chbox_voce[i][j].SetValue(self.controller.epscData.optData.voceFlag[i][j])
                self.text_low_voce[i][j].SetValue(str(self.controller.epscData.optData.lowVoce[i][j]))
                self.text_high_voce[i][j].SetValue(str(self.controller.epscData.optData.highVoce[i][j]))

        self.showVoce()

    def showVoce(self):
        for i in range(8):
            if i + 1 in self.controller.epscData.matParam['Phase1'].selectedSystems:
                for j in range(4):
                    self.chbox_voce[i][j].Enable(True)
                    self.text_initial_voce[i][j].SetValue(str(self.controller.epscData.matParam['Phase1'].voce[i][j]))

            else:
                for j in range(4):
                    self.chbox_voce[i][j].Enable(False)

        self.Update()

    def OnHKL(self, event):
        if self.controller.epscData.diffractionDataSaved:
            dialog = HKLDialog(parent=self, winSize=(300, 300))
        else:
            msg = 'You should input diffraction data first!'
            dialog = wx.MessageDialog(self, msg, 'Warning', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        event.Skip()

    def OnChkHKL(self, event):
        if event.IsChecked():
            self.button_HKL.Enable(True)
        else:
            self.button_HKL.Enable(False)

    def refreshOptimizedVoce(self, p):
        count = 0
        for i in range(8):
            if i + 1 in self.controller.epscData.matParam['Phase1'].selectedSystems:
                for j in range(4):
                    if self.controller.epscData.optData.voceFlag[i][j] == 1:
                        self.text_initial_voceHCP[i][j].SetValue(str(p[count]))
                        count += 1

        self.Update()

    def OnOK(self, event):
        if self.chkbox_macro.GetValue() == True:
            self.controller.epscData.optData.setData('expData', 'macro')
            if self.chkbox_hkl.GetValue() == True:
                self.controller.epscData.optData.setData('expData', 'both')
        else:
            self.controller.epscData.optData.setData('expData', 'hkl')
        for i in range(8):
            for j in range(4):
                self.controller.epscData.optData.voceFlag[i][j] = self.chbox_voce[i][j].GetValue()
                self.controller.epscData.optData.lowVoce[i][j] = self.text_low_voce[i][j].GetValue()
                self.controller.epscData.optData.highVoce[i][j] = self.text_high_voce[i][j].GetValue()

        self.treePanel.turnOnOptNode(1)
        self.controller.epscData.optData.turnOnFlag('range')
        self.controller.epscData.optData.turnOnFlag('optData')

    def __set_properties(self):
        self.SetSize((664, 398))
        self.SetScrollbars(20, 20, 50, 50)
        self.chkbox_macro.SetValue(1)

    def __do_layout(self):
        sizer_top = wx.BoxSizer(wx.VERTICAL)
        sizer_OK = wx.BoxSizer(wx.HORIZONTAL)
        sizer_btn = wx.BoxSizer(wx.HORIZONTAL)
        sizer_Model = wx.StaticBoxSizer(self.sizer_Model_staticbox, wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(2, 2, 0, 0)
        sizer_ph2_power = wx.BoxSizer(wx.VERTICAL)
        sizer_ph1_power = wx.BoxSizer(wx.VERTICAL)
        sizer_Experiment = wx.StaticBoxSizer(self.sizer_Experiment_staticbox, wx.VERTICAL)
        sizer_Experiment.Add(self.chkbox_macro, 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
        sizer_Experiment.Add(self.chkbox_hkl, 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
        sizer_Experiment.Add(self.button_HKL, 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
        sizer_top.Add(sizer_Experiment, 0, wx.ALL | wx.EXPAND, 2)
        for i in range(8):
            sizer_ph1 = wx.StaticBoxSizer(self.sizer_slip_staticbox[i], wx.HORIZONTAL)
            sizer_ph1_voce = wx.FlexGridSizer(5, 4, 0, 0)
            sizer_ph1_voce.Add(self.label_name_voce[i], 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
            sizer_ph1_voce.Add(self.label_initial_voce[i], 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
            sizer_ph1_voce.Add(self.label_low_voce[i], 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
            sizer_ph1_voce.Add(self.label_high_voce[i], 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
            for j in range(4):
                sizer_ph1_voce.Add(self.chbox_voce[i][j], 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
                sizer_ph1_voce.Add(self.text_initial_voce[i][j], 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
                sizer_ph1_voce.Add(self.text_high_voce[i][j], 0, wx.ALL | wx.ADJUST_MINSIZE, 5)
                sizer_ph1_voce.Add(self.text_low_voce[i][j], 0, wx.ALL | wx.ADJUST_MINSIZE, 5)

            sizer_ph1.Add(sizer_ph1_voce, 1, wx.EXPAND, 0)
            grid_sizer_1.Add(sizer_ph1, 1, wx.EXPAND, 0)

        sizer_Model.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        sizer_top.Add(sizer_Model, 0, wx.ALL | wx.EXPAND, 2)
        sizer_btn.Add((20, 20), 1, wx.ADJUST_MINSIZE, 0)
        sizer_btn.Add((20, 20), 1, wx.ADJUST_MINSIZE, 0)
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
    frame = wx.Frame(None, -1, 'dynamic test', size=(800, 600))
    frame_1 = OptHCPDataPanel(frame)
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()