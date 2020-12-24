# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/plotPanel.py
# Compiled at: 2009-05-29 13:49:10
import wx, sys
from SCMPanel import SCMPanel

class PlotPanel(wx.Panel, SCMPanel):
    """ panel for plotting
    """

    def __init__(self, *args, **kwds):
        SCMPanel.__init__(self, *args, **kwds)
        wx.Panel.__init__(self, *args, **kwds)
        self.sizer_4_staticbox = wx.StaticBox(self, -1, 'Neutron')
        self.sizer_3_staticbox = wx.StaticBox(self, -1, 'Macro')
        self.macroModelCheck = wx.CheckBox(self, -1, 'Model Result')
        self.macroExpCheck = wx.CheckBox(self, -1, 'Experiment Data')
        self.neutronModelCheck = wx.CheckBox(self, -1, 'Model Result')
        self.neutronExpCheck = wx.CheckBox(self, -1, 'Experiment Data')
        self.macroModelCheck.SetValue(True)
        self.macroExpCheck.SetValue(True)
        self.neutronModelCheck.SetValue(True)
        self.neutronExpCheck.SetValue(True)
        self.static_line_1 = wx.StaticLine(self, -1)
        self.plotButton = wx.Button(self, -1, 'Plot')
        self.resetButton = wx.Button(self, -1, 'Reset')
        self.gauge = wx.Gauge(self, -1, 50, (110, 95), (210, 20))
        self.__set_properties()
        self.__do_layout()
        self.Bind(wx.EVT_BUTTON, self.onPlot, self.plotButton)
        self.Bind(wx.EVT_BUTTON, self.onReset, self.resetButton)

    def __set_properties(self):
        pass

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.StaticBoxSizer(self.sizer_4_staticbox, wx.VERTICAL)
        sizer_3 = wx.StaticBoxSizer(self.sizer_3_staticbox, wx.VERTICAL)
        sizer_3.Add(self.macroModelCheck, 1, wx.LEFT | wx.ADJUST_MINSIZE, 10)
        sizer_3.Add(self.macroExpCheck, 1, wx.LEFT | wx.ADJUST_MINSIZE, 10)
        sizer_1.Add(sizer_3, 1, wx.EXPAND, 10)
        sizer_4.Add(self.neutronModelCheck, 1, wx.LEFT | wx.ADJUST_MINSIZE | wx.EXPAND, 10)
        sizer_4.Add(self.neutronExpCheck, 1, wx.LEFT | wx.ADJUST_MINSIZE | wx.EXPAND, 10)
        sizer_1.Add(sizer_4, 1, wx.EXPAND, 10)
        sizer_1.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_1.Add(self.static_line_1, 0, wx.BOTTOM | wx.EXPAND, 5)
        sizer_2.Add(self.plotButton, 0, wx.BOTTOM | wx.LEFT | wx.RIGHT | wx.ADJUST_MINSIZE, 5)
        sizer_2.Add(self.resetButton, 0, wx.BOTTOM | wx.LEFT | wx.RIGHT | wx.ADJUST_MINSIZE, 5)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)
        sizer_1.Add(self.gauge, 0, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_1)

    def enableWidgets(self, on=True):
        """Enable or disable the widgets."""
        self.macroDataList.Enable(on)
        self.neutronDataList.Enable(on)
        self.resetButton.Enable(on)
        self.plotButton.Enable(on)

    def onPlot(self, event):
        """Plot some stuff."""
        self.Parent.clearPlots()
        self.Parent.OnPlot(None)
        if self.macroModelCheck.GetValue() == True:
            if self.controller.epscData.flagRun == False:
                msg = 'You should run the model to plot!'
                dlg = wx.MessageDialog(self, msg, 'Warning', wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
                return
            if self.macroExpCheck.GetValue() == True:
                self.macro = 2
            else:
                self.macro = 1
            self.controller.plotEngine.plotMacroTop(self.Parent, self.macro)
        elif self.macroExpCheck.GetValue() == True:
            self.macro = 3
            if self.controller.epscData.expData.checkFlagOn('expData'):
                self.controller.plotEngine.plotMacroTop(self.Parent, self.macro)
            else:
                msg = 'You should input the experimental files to plot!'
                dlg = wx.MessageDialog(self, msg, 'Warning', wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
                return
        else:
            self.macro = 0
        if self.neutronModelCheck.GetValue() == True:
            if self.controller.epscData.flagRun == False:
                msg = 'You should run the model to plot!'
                dlg = wx.MessageDialog(self, msg, 'Warning', wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
                return
            if self.neutronExpCheck.GetValue() == True:
                self.neutron = 2
            else:
                self.neutron = 1
            self.controller.plotEngine.plotNeutronTop(self.Parent, self.neutron)
        elif self.neutronExpCheck.GetValue() == True:
            self.neutron = 3
            if self.controller.epscData.expData.checkFlagOn('expData'):
                if self.controller.epscData.diffractionDataSaved:
                    self.controller.plotEngine.plotNeutronTop(self.Parent, self.neutron)
                else:
                    msg = 'You should input the diffraction data to plot!'
                    dlg = wx.MessageDialog(self, msg, 'Warning', wx.OK)
                    dlg.ShowModal()
                    dlg.Destroy()
                    return
            else:
                msg = 'You should input the experimental files to plot!'
                dlg = wx.MessageDialog(self, msg, 'Warning', wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
                return
        else:
            self.neutron = 0
        return

    def onReset(self, event):
        """Reset everything."""
        self.macroExpCheck.SetValue(False)
        self.macroModelCheck.SetValue(False)
        self.neutronExpCheck.SetValue(False)
        self.neutronModelCheck.SetValue(False)

    def _check(self, event):
        try:
            self._plot(None)
            self.plotButton.Enable()
        except ControlConfigError:
            self.plotButton.Disable()

        return

    def disableButton(self):
        self.plotButton.Enable(False)

    def enableButton(self):
        self.plotButton.Enable(True)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    wx.InitAllImageHandlers()
    frame = wx.Frame(None, -1, 'dynamic test', size=(800, 900))
    panel = PlotPanel(frame)
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()