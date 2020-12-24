# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_dialogs/time_selection.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 13433 bytes
import wx, webbrowser

class Time_Duration(wx.Dialog):
    __doc__ = '\n    This class show a simple dialog with a timer selection\n    to set duration.\n    FIXME: replace spinctrl with a timer spin float ctrl if exist\n    '

    def __init__(self, parent, hasSet):
        """
        FFmpeg use this format to specifier a duration range:
        "-ss 00:00:00 -t 00:00:00". The -ss flag is the initial
        start selection time; the -t flag is the duration time amount
        starting from -ss. All this one is specified by hours, minutes
        and seconds values.
        See FFmpeg documents for more details.
        When this dialog is called, the values previously set are returned
        for a complete reading (if there are preconfigured values)
        """
        if hasSet == '':
            self.init_hour = '00'
            self.init_minute = '00'
            self.init_seconds = '00'
            self.cut_hour = '00'
            self.cut_minute = '00'
            self.cut_seconds = '00'
        else:
            self.init_hour = hasSet[4:6]
            self.init_minute = hasSet[7:9]
            self.init_seconds = hasSet[10:12]
            self.cut_hour = hasSet[16:18]
            self.cut_minute = hasSet[19:21]
            self.cut_seconds = hasSet[22:24]
        wx.Dialog.__init__(self, parent, (-1), style=(wx.DEFAULT_DIALOG_STYLE))
        self.start_hour_ctrl = wx.SpinCtrl(self, (wx.ID_ANY), ('%s' % self.init_hour),
          min=0, max=23, style=(wx.TE_PROCESS_ENTER))
        lab1 = wx.StaticText(self, wx.ID_ANY, ':')
        lab1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ''))
        self.start_minute_ctrl = wx.SpinCtrl(self, (wx.ID_ANY), ('%s' % self.init_minute),
          min=0, max=59, style=(wx.TE_PROCESS_ENTER))
        lab2 = wx.StaticText(self, wx.ID_ANY, ':')
        lab2.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ''))
        self.start_second_ctrl = wx.SpinCtrl(self, (wx.ID_ANY), ('%s' % self.init_seconds),
          min=0, max=59, style=(wx.TE_PROCESS_ENTER))
        sizerbox = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _('Seeking (start point) [hh,mm,ss]')), wx.VERTICAL)
        self.stop_hour_ctrl = wx.SpinCtrl(self, (wx.ID_ANY), ('%s' % self.cut_hour),
          min=0, max=23, style=(wx.TE_PROCESS_ENTER))
        lab3 = wx.StaticText(self, wx.ID_ANY, ':')
        lab3.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ''))
        self.stop_minute_ctrl = wx.SpinCtrl(self, (wx.ID_ANY), ('%s' % self.cut_minute),
          min=0, max=59, style=(wx.TE_PROCESS_ENTER))
        lab4 = wx.StaticText(self, wx.ID_ANY, ':')
        lab4.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ''))
        self.stop_second_ctrl = wx.SpinCtrl(self, (wx.ID_ANY), ('%s' % self.cut_seconds),
          min=0, max=59, style=(wx.TE_PROCESS_ENTER))
        sizer_2_staticbox = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _('Cut (end point) [hh,mm,ss]')), wx.VERTICAL)
        btn_help = wx.Button(self, (wx.ID_HELP), '', size=(-1, -1))
        btn_close = wx.Button(self, wx.ID_CANCEL, '')
        btn_ok = wx.Button(self, wx.ID_OK, '')
        btn_reset = wx.Button(self, wx.ID_CLEAR, '')
        self.SetTitle(_('Videomass: duration'))
        self.start_hour_ctrl.SetToolTip(_('Hours time'))
        self.start_minute_ctrl.SetToolTip(_('Minutes Time'))
        self.start_second_ctrl.SetToolTip(_('Seconds time'))
        self.stop_hour_ctrl.SetToolTip(_('Hours amount duration'))
        self.stop_minute_ctrl.SetToolTip(_('Minutes amount duration'))
        self.stop_second_ctrl.SetToolTip(_('Seconds amount duration'))
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_base = wx.FlexGridSizer(3, 1, 0, 0)
        gridFlex1 = wx.FlexGridSizer(1, 5, 0, 0)
        gridFlex2 = wx.FlexGridSizer(1, 5, 0, 0)
        grid_sizer_base.Add(sizerbox, 0, wx.ALL | wx.ALIGN_CENTRE, 5)
        sizerbox.Add(gridFlex1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridFlex1.Add(self.start_hour_ctrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridFlex1.Add(lab1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridFlex1.Add(self.start_minute_ctrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridFlex1.Add(lab2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridFlex1.Add(self.start_second_ctrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_base.Add(sizer_2_staticbox, 0, wx.ALL | wx.ALIGN_CENTRE, 5)
        sizer_2_staticbox.Add(gridFlex2, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridFlex2.Add(self.stop_hour_ctrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridFlex2.Add(lab3, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridFlex2.Add(self.stop_minute_ctrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridFlex2.Add(lab4, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridFlex2.Add(self.stop_second_ctrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridhelp = wx.GridSizer(1, 1, 0, 0)
        gridhelp.Add(btn_help, 1, wx.ALL, 5)
        gridexit = wx.GridSizer(1, 3, 0, 0)
        gridexit.Add(btn_close, 1, wx.ALL, 5)
        gridexit.Add(btn_ok, 1, wx.ALL, 5)
        gridexit.Add(btn_reset, 1, wx.ALL, 5)
        gridBtn = wx.GridSizer(1, 2, 0, 0)
        gridBtn.Add(gridhelp)
        gridBtn.Add(gridexit)
        grid_sizer_base.Add(gridBtn, 1, wx.ALL, 5)
        sizer_base.Add(grid_sizer_base)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        self.Layout()
        self.Bind(wx.EVT_SPINCTRL, self.start_hour, self.start_hour_ctrl)
        self.Bind(wx.EVT_SPINCTRL, self.start_minute, self.start_minute_ctrl)
        self.Bind(wx.EVT_SPINCTRL, self.start_second, self.start_second_ctrl)
        self.Bind(wx.EVT_SPINCTRL, self.stop_hour, self.stop_hour_ctrl)
        self.Bind(wx.EVT_SPINCTRL, self.stop_minute, self.stop_minute_ctrl)
        self.Bind(wx.EVT_SPINCTRL, self.stop_second, self.stop_second_ctrl)
        self.Bind(wx.EVT_BUTTON, self.on_help, btn_help)
        self.Bind(wx.EVT_BUTTON, self.on_close, btn_close)
        self.Bind(wx.EVT_BUTTON, self.on_ok, btn_ok)
        self.Bind(wx.EVT_BUTTON, self.resetValues, btn_reset)

    def start_hour(self, event):
        self.init_hour = '%s' % self.start_hour_ctrl.GetValue()
        if len(self.init_hour) == 1:
            self.init_hour = '0%s' % self.start_hour_ctrl.GetValue()

    def start_minute(self, event):
        self.init_minute = '%s' % self.start_minute_ctrl.GetValue()
        if len(self.init_minute) == 1:
            self.init_minute = '0%s' % self.start_minute_ctrl.GetValue()

    def start_second(self, event):
        self.init_seconds = '%s' % self.start_second_ctrl.GetValue()
        if len(self.init_seconds) == 1:
            self.init_seconds = '0%s' % self.start_second_ctrl.GetValue()

    def stop_hour(self, event):
        self.cut_hour = '%s' % self.stop_hour_ctrl.GetValue()
        if len(self.cut_hour) == 1:
            self.cut_hour = '0%s' % self.stop_hour_ctrl.GetValue()

    def stop_minute(self, event):
        self.cut_minute = '%s' % self.stop_minute_ctrl.GetValue()
        if len(self.cut_minute) == 1:
            self.cut_minute = '0%s' % self.stop_minute_ctrl.GetValue()

    def stop_second(self, event):
        self.cut_seconds = '%s' % self.stop_second_ctrl.GetValue()
        if len(self.cut_seconds) == 1:
            self.cut_seconds = '0%s' % self.stop_second_ctrl.GetValue()

    def resetValues(self, event):
        """
        Reset all values at initial state. Is need to confirm with
        ok Button for apply correctly.
        """
        (
         self.start_hour_ctrl.SetValue(0), self.start_minute_ctrl.SetValue(0))
        (self.start_second_ctrl.SetValue(0), self.stop_hour_ctrl.SetValue(0))
        (self.stop_minute_ctrl.SetValue(0), self.stop_second_ctrl.SetValue(0))
        self.init_hour, self.init_minute, self.init_seconds = ('00', '00', '00')
        self.cut_hour, self.cut_minute, self.cut_seconds = ('00', '00', '00')

    def on_help(self, event):
        """
        """
        page = 'https://jeanslack.github.io/Videomass/Pages/Toolbar/Duration.html'
        webbrowser.open(page)

    def on_close(self, event):
        event.Skip()

    def on_ok(self, event):
        """
        if you enable self.Destroy(), it delete from memory all data
        event and no return correctly. It has the right behavior if
        not used here, because it is called in the main frame.

        Event.Skip(), work correctly here. Sometimes needs to disable
        it for needs to maintain the view of the window (for exemple).
        """
        ss = '%s:%s:%s' % (self.init_hour, self.init_minute, self.init_seconds)
        t = '%s:%s:%s' % (self.cut_hour, self.cut_minute, self.cut_seconds)
        if ss != '00:00:00':
            if t == '00:00:00':
                wx.MessageBox(_("Length of cut missing: Cut (end point) [hh,mm,ss]\n\nYou should calculate the time amount between the Seeking (start point) and the cut point, then insert it in 'Cut (end point)'. Always consider the total duration of the flow in order to avoid entering incorrect values."), 'Duration', wx.ICON_INFORMATION, self)
                return
        self.GetValue()
        event.Skip()

    def GetValue(self):
        """
        This method return values via the interface GetValue()
        """
        cut_range = '-ss %s:%s:%s -t %s:%s:%s' % (self.init_hour,
         self.init_minute,
         self.init_seconds,
         self.cut_hour,
         self.cut_minute,
         self.cut_seconds)
        return cut_range