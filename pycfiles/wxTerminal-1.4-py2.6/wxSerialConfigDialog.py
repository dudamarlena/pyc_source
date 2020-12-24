# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wxTerminal/wxSerialConfigDialog.py
# Compiled at: 2013-01-16 07:43:02
import wx, serial, sys, glob
SHOW_BAUDRATE = 1
SHOW_FORMAT = 2
SHOW_FLOW = 4
SHOW_TIMEOUT = 8
SHOW_ALL = SHOW_BAUDRATE | SHOW_FORMAT | SHOW_FLOW | SHOW_TIMEOUT

def _enumerate_serial_win():
    import _winreg as winreg, itertools
    path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    except WindowsError:
        raise IterationError

    for i in itertools.count():
        try:
            val = winreg.EnumValue(key, i)
            yield (str(val[1]), str(val[0]))
        except EnvironmentError:
            break


def EnumerateSerial():
    devs = []
    if 'linux' in sys.platform:
        devs.extend(glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*'))
    elif 'win' in sys.platform:
        devs.extend(_enumerate_serial_win())
    else:
        raise NotImplementedError, 'Only win and linux are supported'
    return devs


class SerialConfigDialog(wx.Dialog):
    """Serial Port confiuration dialog, to be used with pyserial 2.0+
       When instantiating a class of this dialog, then the "serial" keyword
       argument is mandatory. It is a reference to a serial.Serial instance.
       the optional "show" keyword argument can be used to show/hide different
       settings. The default is SHOW_ALL which coresponds to 
       SHOW_BAUDRATE|SHOW_FORMAT|SHOW_FLOW|SHOW_TIMEOUT. All constants can be
       found in ths module (not the class)."""

    def __init__(self, *args, **kwds):
        self.serial = kwds['serial']
        del kwds['serial']
        self.show = SHOW_ALL
        if kwds.has_key('show'):
            self.show = kwds['show']
            del kwds['show']
        kwds['style'] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.label_2 = wx.StaticText(self, -1, 'Port')
        self.combo_box_port = wx.ComboBox(self, -1, choices=['dummy1', 'dummy2', 'dummy3', 'dummy4', 'dummy5'], style=wx.CB_DROPDOWN)
        if self.show & SHOW_BAUDRATE:
            self.label_1 = wx.StaticText(self, -1, 'Baudrate')
            self.choice_baudrate = wx.Choice(self, -1, choices=['choice 1'])
        if self.show & SHOW_FORMAT:
            self.label_3 = wx.StaticText(self, -1, 'Data Bits')
            self.choice_databits = wx.Choice(self, -1, choices=['choice 1'])
            self.label_4 = wx.StaticText(self, -1, 'Stop Bits')
            self.choice_stopbits = wx.Choice(self, -1, choices=['choice 1'])
            self.label_5 = wx.StaticText(self, -1, 'Parity')
            self.choice_parity = wx.Choice(self, -1, choices=['choice 1'])
        if self.show & SHOW_TIMEOUT:
            self.checkbox_timeout = wx.CheckBox(self, -1, 'Use Timeout')
            self.text_ctrl_timeout = wx.TextCtrl(self, -1, '')
            self.label_6 = wx.StaticText(self, -1, 'seconds')
        if self.show & SHOW_FLOW:
            self.checkbox_rtscts = wx.CheckBox(self, -1, 'RTS/CTS')
            self.checkbox_xonxoff = wx.CheckBox(self, -1, 'Xon/Xoff')
        self.button_ok = wx.Button(self, -1, 'OK')
        self.button_cancel = wx.Button(self, -1, 'Cancel')
        self.__set_properties()
        self.__do_layout()
        index = 0
        self.combo_box_port.Clear()
        for (n, portname) in enumerate(EnumerateSerial()):
            self.combo_box_port.Append(portname)
            if self.serial.portstr == portname:
                index = n

        if self.serial.portstr is not None:
            self.combo_box_port.SetValue(str(self.serial.portstr))
        else:
            self.combo_box_port.SetSelection(index)
        if self.show & SHOW_BAUDRATE:
            self.choice_baudrate.Clear()
            for (n, baudrate) in enumerate(self.serial.BAUDRATES):
                self.choice_baudrate.Append(str(baudrate))
                if self.serial.baudrate == baudrate:
                    index = n

            self.choice_baudrate.SetSelection(index)
        if self.show & SHOW_FORMAT:
            self.choice_databits.Clear()
            for (n, bytesize) in enumerate(self.serial.BYTESIZES):
                self.choice_databits.Append(str(bytesize))
                if self.serial.bytesize == bytesize:
                    index = n

            self.choice_databits.SetSelection(index)
            self.choice_stopbits.Clear()
            for (n, stopbits) in enumerate(self.serial.STOPBITS):
                self.choice_stopbits.Append(str(stopbits))
                if self.serial.stopbits == stopbits:
                    index = n

            self.choice_stopbits.SetSelection(index)
            self.choice_parity.Clear()
            for (n, parity) in enumerate(self.serial.PARITIES):
                self.choice_parity.Append(str(serial.PARITY_NAMES[parity]))
                if self.serial.parity == parity:
                    index = n

            self.choice_parity.SetSelection(index)
        if self.show & SHOW_TIMEOUT:
            if self.serial.timeout is None:
                self.checkbox_timeout.SetValue(False)
                self.text_ctrl_timeout.Enable(False)
            else:
                self.checkbox_timeout.SetValue(True)
                self.text_ctrl_timeout.Enable(True)
                self.text_ctrl_timeout.SetValue(str(self.serial.timeout))
        if self.show & SHOW_FLOW:
            self.checkbox_rtscts.SetValue(self.serial.rtscts)
            self.checkbox_xonxoff.SetValue(self.serial.xonxoff)
        self.__attach_events()
        return

    def __set_properties(self):
        self.SetTitle('Serial Port Configuration')
        if self.show & SHOW_TIMEOUT:
            self.text_ctrl_timeout.Enable(0)
        self.button_ok.SetDefault()

    def __do_layout(self):
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_basics = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Basics'), wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(self.label_2, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_5.Add(self.combo_box_port, 1, 0, 0)
        sizer_basics.Add(sizer_5, 0, wx.RIGHT | wx.EXPAND, 0)
        if self.show & SHOW_BAUDRATE:
            sizer_baudrate = wx.BoxSizer(wx.HORIZONTAL)
            sizer_baudrate.Add(self.label_1, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_baudrate.Add(self.choice_baudrate, 1, wx.ALIGN_RIGHT, 0)
            sizer_basics.Add(sizer_baudrate, 0, wx.EXPAND, 0)
        sizer_2.Add(sizer_basics, 0, wx.EXPAND, 0)
        if self.show & SHOW_FORMAT:
            sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_format = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Data Format'), wx.VERTICAL)
            sizer_6.Add(self.label_3, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_6.Add(self.choice_databits, 1, wx.ALIGN_RIGHT, 0)
            sizer_format.Add(sizer_6, 0, wx.EXPAND, 0)
            sizer_7.Add(self.label_4, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_7.Add(self.choice_stopbits, 1, wx.ALIGN_RIGHT, 0)
            sizer_format.Add(sizer_7, 0, wx.EXPAND, 0)
            sizer_8.Add(self.label_5, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_8.Add(self.choice_parity, 1, wx.ALIGN_RIGHT, 0)
            sizer_format.Add(sizer_8, 0, wx.EXPAND, 0)
            sizer_2.Add(sizer_format, 0, wx.EXPAND, 0)
        if self.show & SHOW_TIMEOUT:
            sizer_timeout = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Timeout'), wx.HORIZONTAL)
            sizer_timeout.Add(self.checkbox_timeout, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_timeout.Add(self.text_ctrl_timeout, 0, 0, 0)
            sizer_timeout.Add(self.label_6, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_2.Add(sizer_timeout, 0, 0, 0)
        if self.show & SHOW_FLOW:
            sizer_flow = wx.StaticBoxSizer(wx.StaticBox(self, -1, 'Flow Control'), wx.HORIZONTAL)
            sizer_flow.Add(self.checkbox_rtscts, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_flow.Add(self.checkbox_xonxoff, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_flow.Add((10, 10), 1, wx.EXPAND, 0)
            sizer_2.Add(sizer_flow, 0, wx.EXPAND, 0)
        sizer_3.Add(self.button_ok, 0, 0, 0)
        sizer_3.Add(self.button_cancel, 0, 0, 0)
        sizer_2.Add(sizer_3, 0, wx.ALL | wx.ALIGN_RIGHT, 4)
        self.SetAutoLayout(1)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        sizer_2.SetSizeHints(self)
        self.Layout()

    def __attach_events(self):
        wx.EVT_BUTTON(self, self.button_ok.GetId(), self.OnOK)
        wx.EVT_BUTTON(self, self.button_cancel.GetId(), self.OnCancel)
        if self.show & SHOW_TIMEOUT:
            wx.EVT_CHECKBOX(self, self.checkbox_timeout.GetId(), self.OnTimeout)

    def OnOK(self, events):
        success = True
        self.serial.port = str(self.combo_box_port.GetValue())
        if self.show & SHOW_BAUDRATE:
            self.serial.baudrate = self.serial.BAUDRATES[self.choice_baudrate.GetSelection()]
        if self.show & SHOW_FORMAT:
            self.serial.bytesize = self.serial.BYTESIZES[self.choice_databits.GetSelection()]
            self.serial.stopbits = self.serial.STOPBITS[self.choice_stopbits.GetSelection()]
            self.serial.parity = self.serial.PARITIES[self.choice_parity.GetSelection()]
        if self.show & SHOW_FLOW:
            self.serial.rtscts = self.checkbox_rtscts.GetValue()
            self.serial.xonxoff = self.checkbox_xonxoff.GetValue()
        if self.show & SHOW_TIMEOUT:
            if self.checkbox_timeout.GetValue():
                try:
                    self.serial.timeout = float(self.text_ctrl_timeout.GetValue())
                except ValueError:
                    dlg = wx.MessageDialog(self, 'Timeout must be a numeric value', 'Value Error', wx.OK | wx.ICON_ERROR)
                    dlg.ShowModal()
                    dlg.Destroy()
                    success = False

            else:
                self.serial.timeout = None
        if success:
            self.EndModal(wx.ID_OK)
        return

    def OnCancel(self, events):
        self.EndModal(wx.ID_CANCEL)

    def OnTimeout(self, events):
        if self.checkbox_timeout.GetValue():
            self.text_ctrl_timeout.Enable(True)
        else:
            self.text_ctrl_timeout.Enable(False)


class MyApp(wx.App):
    """Test code"""

    def OnInit(self):
        wxInitAllImageHandlers()
        ser = serial.Serial()
        print ser
        for flags in (SHOW_BAUDRATE, SHOW_FLOW, SHOW_FORMAT, SHOW_TIMEOUT, SHOW_ALL):
            dialog_serial_cfg = SerialConfigDialog(None, -1, '', serial=ser, show=flags)
            self.SetTopWindow(dialog_serial_cfg)
            result = dialog_serial_cfg.ShowModal()
            print ser
            if result != wx.ID_OK:
                break

        while 1:
            dialog_serial_cfg = SerialConfigDialog(None, -1, '', serial=ser)
            self.SetTopWindow(dialog_serial_cfg)
            result = dialog_serial_cfg.ShowModal()
            print ser
            if result != wx.ID_OK:
                break

        return 0


if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()