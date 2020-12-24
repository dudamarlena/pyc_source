# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_dialogs/video_filters.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 61101 bytes
import wx, webbrowser

class VideoRotate(wx.Dialog):
    __doc__ = '\n    Show a dialog to movie frame orientation.\n    TODO: make rotate button with images\n    '

    def __init__(self, parent, orientation, msg):
        """
        Make sure you use the clear button when you finish the task.
        """
        wx.Dialog.__init__(self, parent, (-1), style=(wx.DEFAULT_DIALOG_STYLE))
        self.button_up = wx.Button(self, wx.ID_ANY, _('Flip over'))
        self.button_left = wx.Button(self, wx.ID_ANY, _('Rotate Left'))
        self.button_right = wx.Button(self, wx.ID_ANY, _('Rotate Right'))
        self.button_down = wx.Button(self, wx.ID_ANY, _('Flip below'))
        self.text_rotate = wx.TextCtrl(self, (wx.ID_ANY), '', style=(wx.TE_PROCESS_ENTER | wx.TE_READONLY))
        sizerLabel = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _('Orientation points')), wx.VERTICAL)
        btn_close = wx.Button(self, wx.ID_CANCEL, '')
        self.btn_ok = wx.Button(self, wx.ID_OK, '')
        btn_reset = wx.Button(self, wx.ID_CLEAR, '')
        self.SetTitle(_('Videomass: Set video/image rotation'))
        self.button_up.SetToolTip(_('Reverses visual movie from bottom to top'))
        self.button_left.SetToolTip(_('Rotate view movie to left'))
        self.button_right.SetToolTip(_('Rotate view movie to Right'))
        self.button_down.SetToolTip(_('Reverses visual movie from top to bottom'))
        self.text_rotate.SetMinSize((200, 30))
        self.text_rotate.SetToolTip(_('Display show settings'))
        sizerBase = wx.BoxSizer(wx.VERTICAL)
        gridBase = wx.FlexGridSizer(2, 0, 0, 0)
        sizerBase.Add(gridBase, 0, wx.ALL, 0)
        gridBtnExit = wx.FlexGridSizer(1, 3, 0, 0)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        grid_sizerLabel = wx.GridSizer(1, 1, 0, 0)
        grid_sizerBase = wx.GridSizer(1, 2, 0, 0)
        sizer_3.Add(self.button_up, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        grid_sizerBase.Add(self.button_left, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizerBase.Add(self.button_right, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_3.Add(grid_sizerBase, 1, wx.EXPAND, 0)
        sizer_3.Add(self.button_down, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizerLabel.Add(self.text_rotate, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_3.Add(grid_sizerLabel, 1, wx.EXPAND, 0)
        sizerLabel.Add(sizer_3, 1, wx.EXPAND, 0)
        gridBase.Add(sizerLabel, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridBase.Add(gridBtnExit, 1, wx.ALL, 5)
        gridBtnExit.Add(btn_close, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridBtnExit.Add(self.btn_ok, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridBtnExit.Add(btn_reset, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(sizerBase)
        sizerBase.Fit(self)
        self.Layout()
        self.Bind(wx.EVT_BUTTON, self.on_up, self.button_up)
        self.Bind(wx.EVT_BUTTON, self.on_left, self.button_left)
        self.Bind(wx.EVT_BUTTON, self.on_right, self.button_right)
        self.Bind(wx.EVT_BUTTON, self.on_down, self.button_down)
        self.Bind(wx.EVT_BUTTON, self.on_close, btn_close)
        self.Bind(wx.EVT_BUTTON, self.on_ok, self.btn_ok)
        self.Bind(wx.EVT_BUTTON, self.on_reset, btn_reset)
        if orientation == '':
            self.orientation = ''
        else:
            self.orientation = orientation
            self.text_rotate.SetValue(msg)

    def on_up(self, event):
        self.orientation = 'transpose=2,transpose=2'
        self.text_rotate.SetValue(_('180° from bottom to top'))

    def on_left(self, event):
        opt = 'transpose=2'
        self.orientation = opt
        self.text_rotate.SetValue(_('Rotate 90° Left'))

    def on_right(self, event):
        self.orientation = 'transpose=1'
        self.text_rotate.SetValue(_('Rotate 90° Right'))

    def on_down(self, event):
        self.orientation = 'transpose=2,transpose=2'
        self.text_rotate.SetValue(_('180° from top to bottom'))

    def on_reset(self, event):
        self.orientation = ''
        self.text_rotate.SetValue('')

    def on_close(self, event):
        event.Skip()

    def on_ok(self, event):
        """
        if you enable self.Destroy(), it delete from memory all
        data event and no return correctly. It has the right behavior
        if not used here, because it is called in the main frame.

        Event.Skip(), work correctly here. Sometimes needs to disable
        it for needs to maintain the view of the window.
        """
        self.GetValue()
        event.Skip()

    def GetValue(self):
        """
        This method return values via the interface GetValue()
        """
        msg = self.text_rotate.GetValue()
        return (self.orientation, msg)


class VideoCrop(wx.Dialog):
    __doc__ = '\n    Show a dialog with buttons for movie image orientation.\n    TODO: make rotate button with images\n    '

    def __init__(self, parent, fcrop):
        """
        Make sure you use the clear button when you finish the task.
        """
        self.w = ''
        self.h = ''
        self.y = ''
        self.x = ''
        wx.Dialog.__init__(self, parent, (-1), style=(wx.DEFAULT_DIALOG_STYLE))
        self.label_width = wx.StaticText(self, wx.ID_ANY, _('Width'))
        self.crop_width = wx.SpinCtrl(self, (wx.ID_ANY), '-1', min=(-1),
          max=10000,
          size=(-1, -1),
          style=(wx.TE_PROCESS_ENTER))
        self.label_height = wx.StaticText(self, wx.ID_ANY, _('Height'))
        self.crop_height = wx.SpinCtrl(self, (wx.ID_ANY), '-1', min=(-1),
          max=10000,
          size=(-1, -1),
          style=(wx.TE_PROCESS_ENTER))
        self.label_X = wx.StaticText(self, wx.ID_ANY, 'X')
        self.crop_X = wx.SpinCtrl(self, (wx.ID_ANY), '-1', min=(-1),
          max=10000,
          size=(-1, -1),
          style=(wx.TE_PROCESS_ENTER))
        self.label_Y = wx.StaticText(self, wx.ID_ANY, 'Y')
        self.crop_Y = wx.SpinCtrl(self, (wx.ID_ANY), '-1', min=(-1),
          max=10000,
          size=(-1, -1),
          style=(wx.TE_PROCESS_ENTER))
        sizerLabel = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _('Crop Dimensions')), wx.VERTICAL)
        btn_help = wx.Button(self, wx.ID_HELP, '')
        btn_close = wx.Button(self, wx.ID_CANCEL, '')
        self.btn_ok = wx.Button(self, wx.ID_OK, '')
        btn_reset = wx.Button(self, wx.ID_CLEAR, '')
        sizerBase = wx.BoxSizer(wx.VERTICAL)
        gridBase = wx.FlexGridSizer(2, 1, 0, 0)
        sizerBase.Add(gridBase, 0, wx.ALL, 0)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        grid_sizerBase = wx.FlexGridSizer(1, 5, 0, 0)
        sizer_3.Add(self.label_height, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        sizer_3.Add(self.crop_height, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        grid_sizerBase.Add(self.label_Y, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizerBase.Add(self.crop_Y, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizerBase.Add((50, 50), 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizerBase.Add(self.crop_width, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizerBase.Add(self.label_width, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_3.Add(grid_sizerBase, 1, wx.EXPAND, 0)
        sizer_3.Add(self.crop_X, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_3.Add(self.label_X, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizerLabel.Add(sizer_3, 1, wx.EXPAND, 0)
        gridBase.Add(sizerLabel, 1, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 10)
        gridBtn = wx.GridSizer(1, 2, 0, 0)
        gridBase.Add(gridBtn)
        gridhelp = wx.GridSizer(1, 1, 0, 0)
        gridBtn.Add(gridhelp, 0, wx.ALL, 5)
        gridexit = wx.GridSizer(1, 3, 0, 0)
        gridBtn.Add(gridexit, 0, wx.ALL, 5)
        gridhelp.Add(btn_help, 1, wx.ALL, 5)
        gridexit.Add(btn_close, 1, wx.ALL, 5)
        gridexit.Add(self.btn_ok, 1, wx.ALL, 5)
        gridexit.Add(btn_reset, 1, wx.ALL, 5)
        self.SetSizer(sizerBase)
        sizerBase.Fit(self)
        self.Layout()
        self.SetTitle(_('Videomass: video/image crop'))
        height = _('The height of the output video.\nSet to -1 for disabling.')
        width = _('The width of the output video.\nSet to -1 for disabling.')
        x = _('The horizontal position of the left edge.')
        y = _('The vertical position of the top edge of the left corner.')
        self.crop_width.SetToolTip(_('Width:\n%s') % width)
        self.crop_Y.SetToolTip('Y:\n%s' % y)
        self.crop_X.SetToolTip('X:\n%s' % x)
        self.crop_height.SetToolTip(_('Height:\n%s') % height)
        self.Bind(wx.EVT_BUTTON, self.on_close, btn_close)
        self.Bind(wx.EVT_BUTTON, self.on_ok, self.btn_ok)
        self.Bind(wx.EVT_BUTTON, self.on_reset, btn_reset)
        self.Bind(wx.EVT_BUTTON, self.on_help, btn_help)
        if fcrop:
            s = fcrop.split(':')
            item1 = s[0][5:]
            s[0] = item1
            for i in s:
                if i.startswith('w'):
                    self.w = i[2:]
                    self.crop_width.SetValue(int(self.w))
                if i.startswith('h'):
                    self.h = i[2:]
                    self.crop_height.SetValue(int(self.h))
                if i.startswith('x'):
                    self.x = i[2:]
                    self.crop_X.SetValue(int(self.x))
                if i.startswith('y'):
                    self.y = i[2:]
                    self.crop_Y.SetValue(int(self.y))

    def on_help(self, event):
        """
        """
        page = 'https://jeanslack.github.io/Videomass/Pages/Main_Toolbar/VideoConv_Panel/Filters/FilterCrop.html'
        webbrowser.open(page)

    def on_reset(self, event):
        self.h, self.y, self.x, self.w = ('', '', '', '')
        (self.crop_width.SetValue(-1), self.crop_X.SetValue(-1))
        (self.crop_height.SetValue(-1), self.crop_Y.SetValue(-1))

    def on_close(self, event):
        event.Skip()

    def on_ok(self, event):
        """
        if you enable self.Destroy(), it delete from memory all data
        event and no return correctly. It has the right behavior if not
        used here, because it is called in the main frame.

        Event.Skip(), work correctly here. Sometimes needs to disable it for
        needs to maintain the view of the window (for exemple).
        """
        self.GetValue()
        event.Skip()

    def GetValue(self):
        """
        This method return values via the interface GetValue()

        """
        if self.crop_width.GetValue() == -1:
            self.w = ''
        else:
            self.w = 'w=%s:' % self.crop_width.GetValue()
        if self.crop_height.GetValue() == -1:
            self.h = ''
        else:
            self.h = 'h=%s:' % self.crop_height.GetValue()
        if self.crop_X.GetValue() == -1:
            self.x = ''
        else:
            self.x = 'x=%s:' % self.crop_X.GetValue()
        if self.crop_Y.GetValue() == -1:
            self.y = ''
        else:
            self.y = 'y=%s:' % self.crop_Y.GetValue()
        s = '%s%s%s%s' % (self.w, self.h, self.x, self.y)
        if s:
            lst = len(s)
            val = '%s' % s[:lst - 1]
        else:
            val = ''
        return val


class VideoResolution(wx.Dialog):
    __doc__ = '\n    This class show parameters for set custom video resizing.\n    Include a video size, video scaling with setdar and\n    setsar options.\n    '

    def __init__(self, parent, scale, dar, sar):
        """
        See FFmpeg documents for more details..
        When this dialog is called, the values previously set are returned
        for a complete reading (if there are preconfigured values)
        """
        self.width = '0'
        self.height = '0'
        self.darNum = '0'
        self.darDen = '0'
        self.sarNum = '0'
        self.sarDen = '0'
        wx.Dialog.__init__(self, parent, (-1), style=(wx.DEFAULT_DIALOG_STYLE))
        v_scalingbox = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _('Scale (resize)')), wx.VERTICAL)
        label_width = wx.StaticText(self, wx.ID_ANY, _('Width'))
        self.spin_scale_width = wx.SpinCtrl(self, (wx.ID_ANY), '0', min=(-2), max=9000,
          style=(wx.TE_PROCESS_ENTER))
        label_x1 = wx.StaticText(self, wx.ID_ANY, 'X')
        label_x1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ''))
        self.spin_scale_height = wx.SpinCtrl(self, (wx.ID_ANY), '0', min=(-2),
          max=9000,
          style=(wx.TE_PROCESS_ENTER))
        label_height = wx.StaticText(self, wx.ID_ANY, _('Height'))
        v_setdar = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _('Setdar (display aspect ratio):')), wx.VERTICAL)
        label_num = wx.StaticText(self, wx.ID_ANY, _('Numerator'))
        self.spin_setdarNum = wx.SpinCtrl(self, (wx.ID_ANY), '0', min=0, max=99,
          style=(wx.TE_PROCESS_ENTER),
          size=(-1, -1))
        label_sepdar = wx.StaticText(self, wx.ID_ANY, '/')
        label_sepdar.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ''))
        self.spin_setdarDen = wx.SpinCtrl(self, (wx.ID_ANY), '0', min=0, max=99,
          style=(wx.TE_PROCESS_ENTER),
          size=(-1, -1))
        label_den = wx.StaticText(self, wx.ID_ANY, _('Denominator'))
        v_setsar = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _('SetSar (sample aspect ratio):')), wx.VERTICAL)
        label_num1 = wx.StaticText(self, wx.ID_ANY, _('Numerator'))
        self.spin_setsarNum = wx.SpinCtrl(self, (wx.ID_ANY), '0', min=0, max=10000,
          style=(wx.TE_PROCESS_ENTER),
          size=(-1, -1))
        label_sepsar = wx.StaticText(self, wx.ID_ANY, '/')
        label_sepsar.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ''))
        self.spin_setsarDen = wx.SpinCtrl(self, (wx.ID_ANY), '0', min=0, max=10000,
          style=(wx.TE_PROCESS_ENTER),
          size=(-1, -1))
        label_den1 = wx.StaticText(self, wx.ID_ANY, _('Denominator'))
        btn_help = wx.Button(self, wx.ID_HELP, '')
        btn_close = wx.Button(self, wx.ID_CANCEL, '')
        self.btn_ok = wx.Button(self, wx.ID_OK, '')
        btn_reset = wx.Button(self, wx.ID_CLEAR, '')
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_base = wx.FlexGridSizer(4, 1, 0, 0)
        grid_sizer_base.Add(v_scalingbox, 1, wx.ALL | wx.EXPAND, 15)
        grid_sizer_base.Add(v_setdar, 1, wx.ALL | wx.EXPAND, 15)
        grid_sizer_base.Add(v_setsar, 1, wx.ALL | wx.EXPAND, 15)
        Flex_scale = wx.FlexGridSizer(1, 5, 0, 0)
        v_scalingbox.Add(Flex_scale, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        Flex_scale.Add(label_width, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_scale.Add(self.spin_scale_width, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_scale.Add(label_x1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_scale.Add(self.spin_scale_height, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_scale.Add(label_height, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_dar = wx.FlexGridSizer(1, 5, 0, 0)
        v_setdar.Add(Flex_dar, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        Flex_dar.Add(label_num, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_dar.Add(self.spin_setdarNum, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_dar.Add(label_sepdar, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_dar.Add(self.spin_setdarDen, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_dar.Add(label_den, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_sar = wx.FlexGridSizer(1, 5, 0, 0)
        v_setsar.Add(Flex_sar, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        Flex_sar.Add(label_num1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_sar.Add(self.spin_setsarNum, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_sar.Add(label_sepsar, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_sar.Add(self.spin_setsarDen, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_sar.Add(label_den1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridBtn = wx.GridSizer(1, 2, 0, 0)
        gridexit = wx.GridSizer(1, 3, 0, 0)
        gridexit.Add(btn_close, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridexit.Add(self.btn_ok, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridexit.Add(btn_reset, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridhelp = wx.GridSizer(1, 1, 0, 0)
        gridhelp.Add(btn_help, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridBtn.Add(gridhelp, 1, wx.ALL, 10)
        gridBtn.Add(gridexit, 1, wx.ALL, 10)
        grid_sizer_base.Add(gridBtn)
        sizer_base.Add(grid_sizer_base, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        self.Layout()
        self.SetTitle(_('Videomass: resize (change resolution)'))
        scale_str = _('Scale (resize) the input video or image.')
        self.spin_scale_width.SetToolTip(_('WIDTH:\n%s') % scale_str)
        self.spin_scale_height.SetToolTip(_('HEIGHT:\n%s') % scale_str)
        setdar_str = _('Sets the Display Aspect Ratio.\nSet to 0 to disabling.')
        self.spin_setdarNum.SetToolTip(_('-NUMERATOR-\n%s') % setdar_str)
        self.spin_setdarDen.SetToolTip(_('-DENOMINATOR-\n%s') % setdar_str)
        setsar_str = _('The setsar filter sets the Sample (aka Pixel) Aspect Ratio.\nSet to 0 to disabling.')
        self.spin_setsarNum.SetToolTip(_('-NUMERATOR-\n%s') % setsar_str)
        self.spin_setsarDen.SetToolTip(_('-DENOMINATOR-\n%s') % setsar_str)
        self.Bind(wx.EVT_BUTTON, self.on_close, btn_close)
        self.Bind(wx.EVT_BUTTON, self.on_ok, self.btn_ok)
        self.Bind(wx.EVT_BUTTON, self.on_reset, btn_reset)
        self.Bind(wx.EVT_BUTTON, self.on_help, btn_help)
        if scale:
            self.width = scale.split(':')[0][8:]
            self.height = scale.split(':')[1][2:]
            self.spin_scale_width.SetValue(int(self.width))
            self.spin_scale_height.SetValue(int(self.height))
        if dar:
            self.darNum = dar.split('/')[0][7:]
            self.darDen = dar.split('/')[1]
            self.spin_setdarNum.SetValue(int(self.darNum))
            self.spin_setdarDen.SetValue(int(self.darDen))
        if sar:
            self.sarNum = sar.split('/')[0][7:]
            self.sarDen = sar.split('/')[1]
            self.spin_setsarNum.SetValue(int(self.sarNum))
            self.spin_setsarDen.SetValue(int(self.sarDen))

    def on_help(self, event):
        """
        """
        page = 'https://jeanslack.github.io/Videomass/Pages/Main_Toolbar/VideoConv_Panel/Filters/FilterScaling.html'
        webbrowser.open(page)

    def on_reset(self, event):
        self.width, self.height = ('0', '0')
        self.darNum, self.darDen = ('0', '0')
        self.sarNum, self.sarDen = ('0', '0')
        (self.spin_scale_width.SetValue(0), self.spin_scale_height.SetValue(0))
        (self.spin_setdarNum.SetValue(0), self.spin_setdarDen.SetValue(0))
        (self.spin_setsarNum.SetValue(0), self.spin_setsarDen.SetValue(0))

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
        self.GetValue()
        event.Skip()

    def GetValue(self):
        """
        This method return values via the interface GetValue()
        """
        diction = {}
        self.width = '%s' % self.spin_scale_width.GetValue()
        self.height = '%s' % self.spin_scale_height.GetValue()
        self.darNum = '%s' % self.spin_setdarNum.GetValue()
        self.darDen = '%s' % self.spin_setdarDen.GetValue()
        self.sarNum = '%s' % self.spin_setsarNum.GetValue()
        self.sarDen = '%s' % self.spin_setsarDen.GetValue()
        if self.width == '0' or self.height == '0':
            size = ''
        else:
            size = 'scale=w=%s:h=%s' % (self.width, self.height)
            diction['scale'] = size
        if self.darNum == '0' or self.darDen == '0':
            setdar = ''
        else:
            setdar = 'setdar=%s/%s' % (self.darNum, self.darDen)
            diction['setdar'] = setdar
        if self.sarNum == '0' or self.sarDen == '0':
            setsar = ''
        else:
            setsar = 'setsar=%s/%s' % (self.sarNum, self.sarDen)
            diction['setsar'] = setsar
        return diction


class Lacing(wx.Dialog):
    __doc__ = '\n    Show a dialog for image deinterlace/interlace functions\n    with advanced option for each filter.\n    '

    def __init__(self, parent, deinterlace, interlace):
        """
        Make sure you use the clear button when you finish the task.
        """
        self.cmd_opt = {}
        if deinterlace:
            self.cmd_opt['deinterlace'] = deinterlace
        else:
            if interlace:
                self.cmd_opt['interlace'] = interlace
            else:
                wx.Dialog.__init__(self, parent, (-1), style=(wx.DEFAULT_DIALOG_STYLE))
                self.enable_opt = wx.ToggleButton(self, wx.ID_ANY, _('Advanced Options'))
                zone1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _('Deinterlace')), wx.VERTICAL)
                zone2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _('Interlace')), wx.VERTICAL)
                self.ckbx_deintW3fdif = wx.CheckBox(self, wx.ID_ANY, _("Deinterlaces (Using the 'w3fdif' filter)"))
                self.rdbx_w3fdif = wx.RadioBox(self, (wx.ID_ANY), 'Filter', choices=[
                 'simple', 'complex'],
                  majorDimension=0,
                  style=(wx.RA_SPECIFY_ROWS))
                self.rdbx_w3fdif_d = wx.RadioBox(self, (wx.ID_ANY), 'Deint', choices=[
                 'all', 'interlaced'],
                  majorDimension=0,
                  style=(wx.RA_SPECIFY_ROWS))
                self.ckbx_deintYadif = wx.CheckBox(self, wx.ID_ANY, _("Deinterlaces (Using the 'yadif' filter)"))
                yadif = [
                 '0, send_frame', '1, send_field',
                 '2, send_frame_nospatial', '3, send_field_nospatial']
                self.rdbx_Yadif_mode = wx.RadioBox(self, (wx.ID_ANY), 'Mode', choices=yadif,
                  majorDimension=0,
                  style=(wx.RA_SPECIFY_ROWS))
                self.rdbx_Yadif_parity = wx.RadioBox(self, (wx.ID_ANY), 'Parity', choices=[
                 '0, tff',
                 '1, bff',
                 '-1, auto'],
                  majorDimension=0,
                  style=(wx.RA_SPECIFY_ROWS))
                self.rdbx_Yadif_deint = wx.RadioBox(self, (wx.ID_ANY), 'Deint', choices=[
                 '0, all',
                 '1, interlaced'],
                  majorDimension=0,
                  style=(wx.RA_SPECIFY_ROWS))
                self.ckbx_interlace = wx.CheckBox(self, wx.ID_ANY, _("Interlaces (Using the 'interlace' filter)"))
                self.rdbx_inter_scan = wx.RadioBox(self, (wx.ID_ANY), 'Scanning mode', choices=[
                 'scan=tff',
                 'scan=bff'],
                  majorDimension=0,
                  style=(wx.RA_SPECIFY_ROWS))
                self.rdbx_inter_lowpass = wx.RadioBox(self, (wx.ID_ANY), 'Set vertical low-pass filter',
                  choices=[
                 'lowpass=0',
                 'lowpass=1'],
                  majorDimension=0,
                  style=(wx.RA_SPECIFY_ROWS))
                btn_help = wx.Button(self, wx.ID_HELP, '')
                btn_close = wx.Button(self, wx.ID_CANCEL, '')
                self.btn_ok = wx.Button(self, wx.ID_OK, '')
                btn_reset = wx.Button(self, wx.ID_CLEAR, '')
                self.SetTitle(_('Videomass: deinterlace/interlace'))
                self.rdbx_w3fdif.Hide()
                self.rdbx_w3fdif_d.Hide()
                self.rdbx_Yadif_mode.Hide()
                self.rdbx_Yadif_parity.Hide()
                self.rdbx_Yadif_deint.Hide()
                self.rdbx_inter_scan.Hide()
                self.rdbx_inter_lowpass.Hide()
                self.ckbx_deintW3fdif.SetValue(False)
                self.ckbx_deintYadif.SetValue(False)
                self.ckbx_interlace.SetValue(False)
                self.rdbx_w3fdif.SetSelection(1)
                self.rdbx_w3fdif_d.SetSelection(0)
                self.rdbx_Yadif_mode.SetSelection(1)
                self.rdbx_Yadif_parity.SetSelection(2)
                self.rdbx_Yadif_deint.SetSelection(0)
                self.rdbx_inter_scan.SetSelection(0)
                self.rdbx_inter_lowpass.SetSelection(1)
                (self.rdbx_w3fdif.Disable(), self.rdbx_w3fdif_d.Disable())
                (self.rdbx_Yadif_mode.Disable(),)
                (self.rdbx_Yadif_parity.Disable(), self.rdbx_Yadif_deint.Disable())
                (self.rdbx_inter_scan.Disable(), self.rdbx_inter_lowpass.Disable())
                self.sizer_base = wx.BoxSizer(wx.VERTICAL)
                self.sizer_base.Add(self.enable_opt, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 10)
                grid_sizer_base = wx.FlexGridSizer(4, 1, 0, 0)
                grid_sizer_base.Add(zone1, 1, wx.ALL | wx.EXPAND, 5)
                deint_grid = wx.FlexGridSizer(2, 4, 0, 0)
                zone1.Add(deint_grid)
                deint_grid.Add(self.ckbx_deintW3fdif, 0, wx.ALL, 15)
                deint_grid.Add(self.rdbx_w3fdif, 0, wx.ALL, 15)
                deint_grid.Add(self.rdbx_w3fdif_d, 0, wx.ALL, 15)
                deint_grid.Add((20, 20), 0, wx.ALL, 15)
                deint_grid.Add(self.ckbx_deintYadif, 0, wx.ALL, 15)
                deint_grid.Add(self.rdbx_Yadif_mode, 0, wx.ALL, 15)
                deint_grid.Add(self.rdbx_Yadif_parity, 0, wx.ALL, 15)
                deint_grid.Add(self.rdbx_Yadif_deint, 0, wx.ALL, 15)
                grid_sizer_base.Add(zone2, 1, wx.ALL | wx.EXPAND, 5)
                inter_grid = wx.FlexGridSizer(1, 3, 0, 0)
                zone2.Add(inter_grid)
                inter_grid.Add(self.ckbx_interlace, 0, wx.ALL, 15)
                inter_grid.Add(self.rdbx_inter_scan, 0, wx.ALL, 15)
                inter_grid.Add(self.rdbx_inter_lowpass, 0, wx.ALL, 15)
                gridBtn = wx.GridSizer(1, 2, 0, 0)
                grid_sizer_base.Add(gridBtn, 1, wx.ALL | wx.ALIGN_CENTRE, 0)
                gridhelp = wx.GridSizer(1, 1, 0, 0)
                gridexit = wx.GridSizer(1, 3, 0, 0)
                gridBtn.Add(gridhelp)
                gridBtn.Add(gridexit)
                gridhelp.Add(btn_help, 1, wx.ALL, 5)
                gridexit.Add(btn_close, 1, wx.ALL, 5)
                gridexit.Add(self.btn_ok, 1, wx.ALL, 5)
                gridexit.Add(btn_reset, 1, wx.ALL, 5)
                self.sizer_base.Add(grid_sizer_base, 1, wx.ALL, 5)
                self.SetSizer(self.sizer_base)
                self.sizer_base.Fit(self)
                self.Layout()
                self.ckbx_deintW3fdif.SetToolTip(_('Deinterlace the input video with `w3fdif` filter'))
                self.rdbx_w3fdif.SetToolTip(_('Set the interlacing filter coefficients.'))
                self.rdbx_w3fdif_d.SetToolTip(_('Specify which frames to deinterlace.'))
                toolt = _('Deinterlace the input video with `yadif` filter. For FFmpeg is the best and fastest choice ')
                self.ckbx_deintYadif.SetToolTip(toolt)
                self.rdbx_Yadif_mode.SetToolTip(_('mode\nThe interlacing mode to adopt.'))
                toolt = _('parity\nThe picture field parity assumed for the input interlaced video.')
                self.rdbx_Yadif_parity.SetToolTip(toolt)
                self.rdbx_Yadif_deint.SetToolTip(_('Specify which frames to deinterlace.'))
                self.ckbx_interlace.SetToolTip(_('Simple interlacing filter from progressive contents.'))
                toolt = _('scan:\ndetermines whether the interlaced frame is taken from the even (tff - default) or odd (bff) lines of the progressive frame.')
                self.rdbx_inter_scan.SetToolTip(toolt)
                toolt = _('lowpas:\nEnable (default) or disable the vertical lowpass filter to avoid twitter interlacing and reduce moire patterns.\nDefault is no setting.')
                self.rdbx_inter_lowpass.SetToolTip(toolt)
                self.Bind(wx.EVT_CHECKBOX, self.on_DeintW3fdif, self.ckbx_deintW3fdif)
                self.Bind(wx.EVT_RADIOBOX, self.on_W3fdif_filter, self.rdbx_w3fdif)
                self.Bind(wx.EVT_RADIOBOX, self.on_W3fdif_deint, self.rdbx_w3fdif_d)
                self.Bind(wx.EVT_CHECKBOX, self.on_DeintYadif, self.ckbx_deintYadif)
                self.Bind(wx.EVT_RADIOBOX, self.on_modeYadif, self.rdbx_Yadif_mode)
                self.Bind(wx.EVT_RADIOBOX, self.on_parityYadif, self.rdbx_Yadif_parity)
                self.Bind(wx.EVT_RADIOBOX, self.on_deintYadif, self.rdbx_Yadif_deint)
                self.Bind(wx.EVT_CHECKBOX, self.on_Interlace, self.ckbx_interlace)
                self.Bind(wx.EVT_RADIOBOX, self.on_intScan, self.rdbx_inter_scan)
                self.Bind(wx.EVT_RADIOBOX, self.on_intLowpass, self.rdbx_inter_lowpass)
                self.Bind(wx.EVT_TOGGLEBUTTON, self.Advanced_Opt, self.enable_opt)
                self.Bind(wx.EVT_BUTTON, self.on_close, btn_close)
                self.Bind(wx.EVT_BUTTON, self.on_ok, self.btn_ok)
                self.Bind(wx.EVT_BUTTON, self.on_reset, btn_reset)
                self.Bind(wx.EVT_BUTTON, self.on_help, btn_help)
                self.settings()

    def settings--- This code section failed: ---

 L. 857         0  LOAD_STR                 'deinterlace'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                cmd_opt
                6  COMPARE_OP               in
             8_10  POP_JUMP_IF_FALSE   384  'to 384'

 L. 858        12  LOAD_FAST                'self'
               14  LOAD_ATTR                cmd_opt
               16  LOAD_STR                 'deinterlace'
               18  BINARY_SUBSCR    
               20  LOAD_METHOD              startswith
               22  LOAD_STR                 'yadif'
               24  CALL_METHOD_1         1  '1 positional argument'
               26  POP_JUMP_IF_FALSE   186  'to 186'

 L. 859        28  LOAD_FAST                'self'
               30  LOAD_ATTR                ckbx_deintYadif
               32  LOAD_METHOD              SetValue
               34  LOAD_CONST               True
               36  CALL_METHOD_1         1  '1 positional argument'
               38  POP_TOP          

 L. 860        40  LOAD_FAST                'self'
               42  LOAD_ATTR                ckbx_deintW3fdif
               44  LOAD_METHOD              Disable
               46  CALL_METHOD_0         0  '0 positional arguments'
               48  POP_TOP          

 L. 861        50  LOAD_FAST                'self'
               52  LOAD_ATTR                ckbx_interlace
               54  LOAD_METHOD              Disable
               56  CALL_METHOD_0         0  '0 positional arguments'
               58  POP_TOP          

 L. 862        60  LOAD_FAST                'self'
               62  LOAD_ATTR                rdbx_Yadif_mode
               64  LOAD_METHOD              Enable
               66  CALL_METHOD_0         0  '0 positional arguments'
               68  POP_TOP          

 L. 863        70  LOAD_FAST                'self'
               72  LOAD_ATTR                rdbx_Yadif_parity
               74  LOAD_METHOD              Enable
               76  CALL_METHOD_0         0  '0 positional arguments'
               78  POP_TOP          

 L. 864        80  LOAD_FAST                'self'
               82  LOAD_ATTR                rdbx_Yadif_deint
               84  LOAD_METHOD              Enable
               86  CALL_METHOD_0         0  '0 positional arguments'
               88  POP_TOP          

 L. 865        90  LOAD_FAST                'self'
               92  LOAD_ATTR                cmd_opt
               94  LOAD_STR                 'deinterlace'
               96  BINARY_SUBSCR    
               98  LOAD_METHOD              split
              100  LOAD_STR                 '='
              102  CALL_METHOD_1         1  '1 positional argument'
              104  LOAD_CONST               1
              106  BINARY_SUBSCR    
              108  LOAD_METHOD              split
              110  LOAD_STR                 ':'
              112  CALL_METHOD_1         1  '1 positional argument'
              114  STORE_FAST               'indx'

 L. 866       116  LOAD_FAST                'indx'
              118  LOAD_CONST               1
              120  BINARY_SUBSCR    
              122  LOAD_STR                 '-1'
              124  COMPARE_OP               ==
              126  POP_JUMP_IF_FALSE   132  'to 132'

 L. 867       128  LOAD_CONST               2
              130  STORE_FAST               'parity'
            132_0  COME_FROM           126  '126'

 L. 868       132  LOAD_FAST                'self'
              134  LOAD_ATTR                rdbx_Yadif_mode
              136  LOAD_METHOD              SetSelection
              138  LOAD_GLOBAL              int
              140  LOAD_FAST                'indx'
              142  LOAD_CONST               0
              144  BINARY_SUBSCR    
              146  CALL_FUNCTION_1       1  '1 positional argument'
              148  CALL_METHOD_1         1  '1 positional argument'
              150  POP_TOP          

 L. 869       152  LOAD_FAST                'self'
              154  LOAD_ATTR                rdbx_Yadif_parity
              156  LOAD_METHOD              SetSelection
              158  LOAD_FAST                'parity'
              160  CALL_METHOD_1         1  '1 positional argument'
              162  POP_TOP          

 L. 870       164  LOAD_FAST                'self'
              166  LOAD_ATTR                rdbx_Yadif_deint
              168  LOAD_METHOD              SetSelection
              170  LOAD_GLOBAL              int
              172  LOAD_FAST                'indx'
              174  LOAD_CONST               2
              176  BINARY_SUBSCR    
              178  CALL_FUNCTION_1       1  '1 positional argument'
              180  CALL_METHOD_1         1  '1 positional argument'
              182  POP_TOP          
              184  JUMP_FORWARD        382  'to 382'
            186_0  COME_FROM            26  '26'

 L. 872       186  LOAD_FAST                'self'
              188  LOAD_ATTR                cmd_opt
              190  LOAD_STR                 'deinterlace'
              192  BINARY_SUBSCR    
              194  LOAD_METHOD              startswith
              196  LOAD_STR                 'w3fdif'
              198  CALL_METHOD_1         1  '1 positional argument'
          200_202  POP_JUMP_IF_FALSE   592  'to 592'

 L. 873       204  LOAD_FAST                'self'
              206  LOAD_ATTR                ckbx_deintW3fdif
              208  LOAD_METHOD              SetValue
              210  LOAD_CONST               True
              212  CALL_METHOD_1         1  '1 positional argument'
              214  POP_TOP          

 L. 874       216  LOAD_FAST                'self'
              218  LOAD_ATTR                ckbx_deintYadif
              220  LOAD_METHOD              Disable
              222  CALL_METHOD_0         0  '0 positional arguments'
              224  POP_TOP          

 L. 875       226  LOAD_FAST                'self'
              228  LOAD_ATTR                ckbx_interlace
              230  LOAD_METHOD              Disable
              232  CALL_METHOD_0         0  '0 positional arguments'
              234  POP_TOP          

 L. 876       236  LOAD_FAST                'self'
              238  LOAD_ATTR                rdbx_w3fdif
              240  LOAD_METHOD              Enable
              242  CALL_METHOD_0         0  '0 positional arguments'
              244  POP_TOP          

 L. 877       246  LOAD_FAST                'self'
              248  LOAD_ATTR                rdbx_w3fdif_d
              250  LOAD_METHOD              Enable
              252  CALL_METHOD_0         0  '0 positional arguments'
              254  POP_TOP          

 L. 878       256  LOAD_FAST                'self'
              258  LOAD_ATTR                cmd_opt
              260  LOAD_STR                 'deinterlace'
              262  BINARY_SUBSCR    
              264  LOAD_METHOD              split
              266  LOAD_STR                 '='
              268  CALL_METHOD_1         1  '1 positional argument'
              270  LOAD_CONST               1
              272  BINARY_SUBSCR    
              274  LOAD_METHOD              split
              276  LOAD_STR                 ':'
              278  CALL_METHOD_1         1  '1 positional argument'
              280  STORE_FAST               'indx'

 L. 879       282  LOAD_FAST                'indx'
              284  LOAD_CONST               0
              286  BINARY_SUBSCR    
              288  LOAD_STR                 'complex'
              290  COMPARE_OP               ==
          292_294  POP_JUMP_IF_FALSE   302  'to 302'

 L. 880       296  LOAD_CONST               1
              298  STORE_FAST               'filt'
              300  JUMP_FORWARD        320  'to 320'
            302_0  COME_FROM           292  '292'

 L. 881       302  LOAD_FAST                'indx'
              304  LOAD_CONST               0
              306  BINARY_SUBSCR    
              308  LOAD_STR                 'simple'
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_FALSE   320  'to 320'

 L. 882       316  LOAD_CONST               0
              318  STORE_FAST               'filt'
            320_0  COME_FROM           312  '312'
            320_1  COME_FROM           300  '300'

 L. 883       320  LOAD_FAST                'self'
              322  LOAD_ATTR                rdbx_w3fdif
              324  LOAD_METHOD              SetSelection
              326  LOAD_FAST                'filt'
              328  CALL_METHOD_1         1  '1 positional argument'
              330  POP_TOP          

 L. 884       332  LOAD_FAST                'indx'
              334  LOAD_CONST               1
              336  BINARY_SUBSCR    
              338  LOAD_STR                 'all'
              340  COMPARE_OP               ==
          342_344  POP_JUMP_IF_FALSE   352  'to 352'

 L. 885       346  LOAD_CONST               0
              348  STORE_FAST               'deint'
              350  JUMP_FORWARD        370  'to 370'
            352_0  COME_FROM           342  '342'

 L. 886       352  LOAD_FAST                'indx'
              354  LOAD_CONST               1
              356  BINARY_SUBSCR    
              358  LOAD_STR                 'interlaced'
              360  COMPARE_OP               ==
          362_364  POP_JUMP_IF_FALSE   370  'to 370'

 L. 887       366  LOAD_CONST               1
              368  STORE_FAST               'deint'
            370_0  COME_FROM           362  '362'
            370_1  COME_FROM           350  '350'

 L. 888       370  LOAD_FAST                'self'
              372  LOAD_ATTR                rdbx_w3fdif_d
              374  LOAD_METHOD              SetSelection
              376  LOAD_FAST                'deint'
              378  CALL_METHOD_1         1  '1 positional argument'
              380  POP_TOP          
            382_0  COME_FROM           184  '184'
              382  JUMP_FORWARD        592  'to 592'
            384_0  COME_FROM             8  '8'

 L. 890       384  LOAD_STR                 'interlace'
              386  LOAD_FAST                'self'
              388  LOAD_ATTR                cmd_opt
              390  COMPARE_OP               in
          392_394  POP_JUMP_IF_FALSE   592  'to 592'

 L. 891       396  LOAD_FAST                'self'
              398  LOAD_ATTR                ckbx_interlace
              400  LOAD_METHOD              SetValue
              402  LOAD_CONST               True
              404  CALL_METHOD_1         1  '1 positional argument'
              406  POP_TOP          

 L. 892       408  LOAD_FAST                'self'
              410  LOAD_ATTR                ckbx_deintW3fdif
              412  LOAD_METHOD              Disable
              414  CALL_METHOD_0         0  '0 positional arguments'
              416  LOAD_FAST                'self'
              418  LOAD_ATTR                ckbx_deintYadif
              420  LOAD_METHOD              Disable
              422  CALL_METHOD_0         0  '0 positional arguments'
              424  BUILD_TUPLE_2         2 
              426  POP_TOP          

 L. 893       428  LOAD_FAST                'self'
              430  LOAD_ATTR                rdbx_inter_scan
              432  LOAD_METHOD              Enable
              434  CALL_METHOD_0         0  '0 positional arguments'
              436  LOAD_FAST                'self'
              438  LOAD_ATTR                rdbx_inter_lowpass
              440  LOAD_METHOD              Enable
              442  CALL_METHOD_0         0  '0 positional arguments'
              444  BUILD_TUPLE_2         2 
              446  POP_TOP          

 L. 895       448  LOAD_FAST                'self'
              450  LOAD_ATTR                cmd_opt
              452  LOAD_STR                 'interlace'
              454  BINARY_SUBSCR    
              456  LOAD_METHOD              split
              458  LOAD_STR                 '='
              460  CALL_METHOD_1         1  '1 positional argument'
              462  LOAD_CONST               2
              464  BINARY_SUBSCR    
              466  LOAD_METHOD              split
              468  LOAD_STR                 ':'
              470  CALL_METHOD_1         1  '1 positional argument'
              472  STORE_FAST               'scan'

 L. 896       474  LOAD_STR                 'tff'
              476  LOAD_FAST                'scan'
              478  LOAD_CONST               0
              480  BINARY_SUBSCR    
              482  COMPARE_OP               in
          484_486  POP_JUMP_IF_FALSE   494  'to 494'

 L. 897       488  LOAD_CONST               0
              490  STORE_FAST               'scan'
              492  JUMP_FORWARD        512  'to 512'
            494_0  COME_FROM           484  '484'

 L. 898       494  LOAD_STR                 'bff'
              496  LOAD_FAST                'scan'
              498  LOAD_CONST               0
              500  BINARY_SUBSCR    
              502  COMPARE_OP               in
          504_506  POP_JUMP_IF_FALSE   512  'to 512'

 L. 899       508  LOAD_CONST               1
              510  STORE_FAST               'scan'
            512_0  COME_FROM           504  '504'
            512_1  COME_FROM           492  '492'

 L. 900       512  LOAD_FAST                'self'
              514  LOAD_ATTR                rdbx_inter_scan
              516  LOAD_METHOD              SetSelection
              518  LOAD_FAST                'scan'
              520  CALL_METHOD_1         1  '1 positional argument'
              522  POP_TOP          

 L. 902       524  LOAD_FAST                'self'
              526  LOAD_ATTR                cmd_opt
              528  LOAD_STR                 'interlace'
              530  BINARY_SUBSCR    
              532  LOAD_METHOD              split
              534  LOAD_STR                 ':'
              536  CALL_METHOD_1         1  '1 positional argument'
              538  STORE_FAST               'lowpass'

 L. 903       540  LOAD_STR                 'lowpass=0'
              542  LOAD_FAST                'lowpass'
              544  LOAD_CONST               1
              546  BINARY_SUBSCR    
              548  COMPARE_OP               in
          550_552  POP_JUMP_IF_FALSE   560  'to 560'

 L. 904       554  LOAD_CONST               0
              556  STORE_FAST               'lowpass'
              558  JUMP_FORWARD        578  'to 578'
            560_0  COME_FROM           550  '550'

 L. 905       560  LOAD_STR                 'lowpass=1'
              562  LOAD_FAST                'lowpass'
              564  LOAD_CONST               1
              566  BINARY_SUBSCR    
              568  COMPARE_OP               in
          570_572  POP_JUMP_IF_FALSE   578  'to 578'

 L. 906       574  LOAD_CONST               1
              576  STORE_FAST               'lowpass'
            578_0  COME_FROM           570  '570'
            578_1  COME_FROM           558  '558'

 L. 907       578  LOAD_FAST                'self'
              580  LOAD_ATTR                rdbx_inter_lowpass
              582  LOAD_METHOD              SetSelection
              584  LOAD_FAST                'lowpass'
              586  CALL_METHOD_1         1  '1 positional argument'
              588  POP_TOP          
              590  JUMP_FORWARD        592  'to 592'
            592_0  COME_FROM           590  '590'
            592_1  COME_FROM           392  '392'
            592_2  COME_FROM           382  '382'
            592_3  COME_FROM           200  '200'

Parse error at or near `COME_FROM' instruction at offset 592_2

    def on_DeintW3fdif(self, event):
        """
        """
        if self.ckbx_deintW3fdif.IsChecked():
            (
             self.rdbx_w3fdif.Enable(), self.rdbx_w3fdif_d.Enable())
            (self.ckbx_deintYadif.Disable(), self.ckbx_interlace.Disable())
            self.cmd_opt['deinterlace'] = 'w3fdif=complex:all'
        else:
            if not self.ckbx_deintW3fdif.IsChecked():
                (
                 self.rdbx_w3fdif.Disable(), self.rdbx_w3fdif_d.Disable())
                (self.ckbx_deintYadif.Enable(), self.ckbx_interlace.Enable())
                self.cmd_opt.clear()

    def on_W3fdif_filter(self, event):
        """
        """
        self.cmd_opt['deinterlace'] = 'w3fdif=%s:%s' % (
         self.rdbx_w3fdif.GetStringSelection(),
         self.rdbx_w3fdif_d.GetStringSelection())

    def on_W3fdif_deint(self, event):
        """
        """
        self.cmd_opt['deinterlace'] = 'w3fdif=%s:%s' % (
         self.rdbx_w3fdif.GetStringSelection(),
         self.rdbx_w3fdif_d.GetStringSelection())

    def on_DeintYadif(self, event):
        """
        """
        if self.ckbx_deintYadif.IsChecked():
            (
             self.ckbx_deintW3fdif.Disable(), self.rdbx_Yadif_mode.Enable())
            (self.rdbx_Yadif_parity.Enable(), self.rdbx_Yadif_deint.Enable())
            (self.ckbx_interlace.Disable(),)
            self.cmd_opt['deinterlace'] = 'yadif=1:-1:0'
        else:
            if not self.ckbx_deintYadif.IsChecked():
                (
                 self.ckbx_deintW3fdif.Enable(), self.rdbx_Yadif_mode.Disable())
                (self.rdbx_Yadif_parity.Disable(), self.rdbx_Yadif_deint.Disable())
                (self.ckbx_interlace.Enable(),)
                self.cmd_opt.clear()

    def on_modeYadif(self, event):
        """
        """
        parity = self.rdbx_Yadif_parity.GetStringSelection().split(',')
        self.cmd_opt['deinterlace'] = 'yadif=%s:%s:%s' % (
         self.rdbx_Yadif_mode.GetStringSelection()[0],
         parity[0],
         self.rdbx_Yadif_deint.GetStringSelection()[0])

    def on_parityYadif(self, event):
        """
        """
        parity = self.rdbx_Yadif_parity.GetStringSelection().split(',')
        self.cmd_opt['deinterlace'] = 'yadif=%s:%s:%s' % (
         self.rdbx_Yadif_mode.GetStringSelection()[0],
         parity[0],
         self.rdbx_Yadif_deint.GetStringSelection()[0])

    def on_deintYadif(self, event):
        """
        """
        parity = self.rdbx_Yadif_parity.GetStringSelection().split(',')
        self.cmd_opt['deinterlace'] = 'yadif=%s:%s:%s' % (
         self.rdbx_Yadif_mode.GetStringSelection()[0],
         parity[0],
         self.rdbx_Yadif_deint.GetStringSelection()[0])

    def on_Interlace(self, event):
        """
        """
        if self.ckbx_interlace.IsChecked():
            (
             self.ckbx_deintW3fdif.Disable(), self.ckbx_deintYadif.Disable())
            (self.rdbx_inter_scan.Enable(), self.rdbx_inter_lowpass.Enable())
            self.cmd_opt['interlace'] = 'interlace=scan=tff:lowpass=1'
        else:
            if not self.ckbx_interlace.IsChecked():
                (
                 self.ckbx_deintW3fdif.Enable(), self.ckbx_deintYadif.Enable())
                (self.rdbx_inter_scan.Disable(), self.rdbx_inter_lowpass.Disable())
                self.cmd_opt.clear()

    def on_intScan(self, event):
        """
        """
        self.cmd_opt['interlace'] = 'interlace=%s:%s' % (
         self.rdbx_inter_scan.GetStringSelection(),
         self.rdbx_inter_lowpass.GetStringSelection())

    def on_intLowpass(self, event):
        """
        """
        self.cmd_opt['interlace'] = 'interlace=%s:%s' % (
         self.rdbx_inter_scan.GetStringSelection(),
         self.rdbx_inter_lowpass.GetStringSelection())

    def Advanced_Opt(self, event):
        """
        Show or Hide advanved option for all filters
        """
        if self.enable_opt.GetValue():
            self.rdbx_w3fdif.Show()
            self.rdbx_w3fdif_d.Show()
            self.rdbx_Yadif_mode.Show()
            self.rdbx_Yadif_parity.Show()
            self.rdbx_Yadif_deint.Show()
            self.rdbx_inter_scan.Show()
            self.rdbx_inter_lowpass.Show()
        else:
            self.rdbx_w3fdif.Hide()
            self.rdbx_w3fdif_d.Hide()
            self.rdbx_Yadif_mode.Hide()
            self.rdbx_Yadif_parity.Hide()
            self.rdbx_Yadif_deint.Hide()
            self.rdbx_inter_scan.Hide()
            self.rdbx_inter_lowpass.Hide()
        self.SetSizer(self.sizer_base)
        self.sizer_base.Fit(self)
        self.Layout()

    def on_reset(self, event):
        """
        Reset all option and values
        """
        self.cmd_opt.clear()
        self.ckbx_deintW3fdif.SetValue(False)
        self.ckbx_deintYadif.SetValue(False)
        self.ckbx_interlace.SetValue(False)
        self.ckbx_deintW3fdif.Enable()
        self.ckbx_deintYadif.Enable()
        self.ckbx_interlace.Enable()
        self.rdbx_w3fdif.SetSelection(1)
        self.rdbx_w3fdif_d.SetSelection(0)
        self.rdbx_Yadif_mode.SetSelection(1)
        self.rdbx_Yadif_parity.SetSelection(2)
        self.rdbx_Yadif_deint.SetSelection(0)
        self.rdbx_inter_scan.SetSelection(0)
        self.rdbx_inter_lowpass.SetSelection(1)
        (self.rdbx_w3fdif.Disable(), self.rdbx_w3fdif_d.Disable())
        (self.rdbx_Yadif_mode.Disable(), self.rdbx_Yadif_parity.Disable())
        (self.rdbx_Yadif_deint.Disable(), self.rdbx_inter_scan.Disable())
        self.rdbx_inter_lowpass.Disable()

    def on_help(self, event):
        """
        """
        page = 'https://jeanslack.github.io/Videomass/Pages/Main_Toolbar/VideoConv_Panel/Filters/Deint_Inter.html'
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
        self.GetValue()
        event.Skip()

    def GetValue(self):
        """
        This method return values via the interface GetValue()
        """
        return self.cmd_opt


class Denoisers(wx.Dialog):
    __doc__ = '\n    Show a dialog for set denoiser filter\n    '

    def __init__(self, parent, denoiser):
        """
        Make sure you use the clear button when you finish the task.
        Enable filters denoiser useful in some case, example when apply
        a deinterlace filter
        <https://askubuntu.com/questions/866186/how-to-get-good-quality-when-
        converting-digital-video>
        """
        if denoiser:
            self.denoiser = denoiser
        else:
            self.denoiser = ''
        wx.Dialog.__init__(self, parent, (-1), style=(wx.DEFAULT_DIALOG_STYLE))
        zone = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _('Apply Denoisers Filters')), wx.VERTICAL)
        self.ckbx_nlmeans = wx.CheckBox(self, wx.ID_ANY, _('Enable nlmeans denoiser'))
        nlmeans = [
         'Default',
         'Old VHS tapes - good starting point restoration',
         'Heavy - really noisy inputs',
         'Light - good quality inputs']
        self.rdb_nlmeans = wx.RadioBox(self, (wx.ID_ANY), (_('nlmeans options')), choices=nlmeans,
          majorDimension=0,
          style=(wx.RA_SPECIFY_ROWS))
        self.ckbx_hqdn3d = wx.CheckBox(self, wx.ID_ANY, _('Enable hqdn3d denoiser'))
        hqdn3d = [
         'Default', 'Conservative [4.0:4.0:3.0:3.0]',
         'Old VHS tapes restoration [9.0:5.0:3.0:3.0]']
        self.rdb_hqdn3d = wx.RadioBox(self, (wx.ID_ANY), (_('hqdn3d options')), choices=hqdn3d,
          majorDimension=0,
          style=(wx.RA_SPECIFY_ROWS))
        btn_help = wx.Button(self, wx.ID_HELP, '')
        btn_close = wx.Button(self, wx.ID_CANCEL, '')
        self.btn_ok = wx.Button(self, wx.ID_OK, '')
        btn_reset = wx.Button(self, wx.ID_CLEAR, '')
        self.sizer_base = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_base = wx.FlexGridSizer(2, 1, 0, 0)
        grid_sizer_base.Add(zone, 1, wx.ALL | wx.EXPAND, 5)
        grid_den = wx.FlexGridSizer(2, 2, 0, 0)
        zone.Add(grid_den)
        grid_den.Add(self.ckbx_nlmeans, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 15)
        grid_den.Add(self.rdb_nlmeans, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 15)
        grid_den.Add(self.ckbx_hqdn3d, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 15)
        grid_den.Add(self.rdb_hqdn3d, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 15)
        gridhelp = wx.GridSizer(1, 1, 0, 0)
        gridexit = wx.GridSizer(1, 3, 0, 0)
        gridBtn = wx.GridSizer(1, 2, 0, 0)
        gridBtn.Add(gridhelp)
        gridBtn.Add(gridexit)
        grid_sizer_base.Add(gridBtn)
        gridhelp.Add(btn_help, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridexit.Add(btn_close, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridexit.Add(self.btn_ok, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gridexit.Add(btn_reset, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.sizer_base.Add(grid_sizer_base, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(self.sizer_base)
        self.sizer_base.Fit(self)
        self.Layout()
        self.SetTitle(_('Videomass: denoisers filters'))
        tool = _('nlmeans:\n(Denoise frames using Non-Local Means algorithm is capable of restoring video sequences with even strong noise. It is ideal for enhancing the quality of old VHS tapes.')
        self.ckbx_nlmeans.SetToolTip(tool)
        tool = _('hqdn3d:\nThis is a high precision/quality 3d denoise filter. It aims to reduce image noise, producing smooth images and making still images really still. It should enhance compressibility.')
        self.ckbx_hqdn3d.SetToolTip(tool)
        self.Bind(wx.EVT_CHECKBOX, self.on_nlmeans, self.ckbx_nlmeans)
        self.Bind(wx.EVT_CHECKBOX, self.on_hqdn3d, self.ckbx_hqdn3d)
        self.Bind(wx.EVT_RADIOBOX, self.on_nlmeans_opt, self.rdb_nlmeans)
        self.Bind(wx.EVT_RADIOBOX, self.on_hqdn3d_opt, self.rdb_hqdn3d)
        self.Bind(wx.EVT_BUTTON, self.on_help, btn_help)
        self.Bind(wx.EVT_BUTTON, self.on_close, btn_close)
        self.Bind(wx.EVT_BUTTON, self.on_ok, self.btn_ok)
        self.Bind(wx.EVT_BUTTON, self.on_reset, btn_reset)
        self.settings()

    def settings(self):
        """
        Set default or set in according with previusly activated option
        """
        if self.denoiser:
            if self.denoiser.startswith('nlmeans'):
                spl = self.denoiser.split('=')
                if len(spl) == 1:
                    self.rdb_nlmeans.SetSelection(0)
                else:
                    if spl[1] == '8:3:2':
                        self.rdb_nlmeans.SetSelection(1)
                    if spl[1] == '10:5:3':
                        self.rdb_nlmeans.SetSelection(2)
                    if spl[1] == '6:3:1':
                        self.rdb_nlmeans.SetSelection(3)
                self.ckbx_nlmeans.SetValue(True)
                self.ckbx_hqdn3d.SetValue(False)
                self.ckbx_nlmeans.Enable()
                self.ckbx_hqdn3d.Disable()
                self.rdb_nlmeans.Enable()
                self.rdb_hqdn3d.Disable()
            else:
                if self.denoiser.startswith('hqdn3d'):
                    spl = self.denoiser.split('=')
                    print(spl)
                    if len(spl) == 1:
                        self.rdb_hqdn3d.SetSelection(0)
                    else:
                        if spl[1] == '4.0:4.0:3.0:3.0':
                            self.rdb_hqdn3d.SetSelection(1)
                        if spl[1] == '9.0:5.0:3.0:3.0':
                            self.rdb_hqdn3d.SetSelection(2)
                        self.ckbx_nlmeans.SetValue(False)
                        self.ckbx_hqdn3d.SetValue(True)
                        self.ckbx_nlmeans.Disable()
                        self.ckbx_hqdn3d.Enable()
                        self.rdb_nlmeans.Disable()
                        self.rdb_hqdn3d.Enable()
        else:
            self.ckbx_nlmeans.SetValue(False)
            self.ckbx_hqdn3d.SetValue(False)
            self.ckbx_nlmeans.Enable()
            self.ckbx_hqdn3d.Enable()
            self.rdb_nlmeans.SetSelection(0)
            self.rdb_nlmeans.Disable()
            self.rdb_hqdn3d.Disable()

    def on_nlmeans(self, event):
        """
        """
        if self.ckbx_nlmeans.IsChecked():
            self.rdb_nlmeans.Enable()
            self.rdb_hqdn3d.Disable()
            self.ckbx_hqdn3d.Disable()
            self.denoiser = 'nlmeans'
        else:
            if not self.ckbx_nlmeans.IsChecked():
                self.rdb_nlmeans.Disable()
                self.ckbx_hqdn3d.Enable()
                self.denoiser = ''

    def on_nlmeans_opt(self, event):
        """
        """
        opt = self.rdb_nlmeans.GetStringSelection()
        if opt == 'Default':
            self.denoiser = 'nlmeans'
        else:
            if opt == 'Old VHS tapes - good starting point restoration':
                self.denoiser = 'nlmeans=8:3:2'
            else:
                if opt == 'Heavy - really noisy inputs':
                    self.denoiser = 'nlmeans=10:5:3'
                else:
                    if opt == 'Light - good quality inputs':
                        self.denoiser = 'nlmeans=6:3:1'

    def on_hqdn3d(self, event):
        """
        """
        if self.ckbx_hqdn3d.IsChecked():
            self.ckbx_nlmeans.Disable()
            self.rdb_hqdn3d.Enable()
            self.denoiser = 'hqdn3d'
        else:
            if not self.ckbx_hqdn3d.IsChecked():
                self.ckbx_nlmeans.Enable()
                self.rdb_hqdn3d.Disable()
                self.denoiser = ''

    def on_hqdn3d_opt(self, event):
        """
        """
        opt = self.rdb_hqdn3d.GetStringSelection()
        if opt == 'Default':
            self.denoiser = 'hqdn3d'
        else:
            if opt == 'Conservative [4.0:4.0:3.0:3.0]':
                self.denoiser = 'hqdn3d=4.0:4.0:3.0:3.0'
            else:
                if opt == 'Old VHS tapes restoration [9.0:5.0:3.0:3.0]':
                    self.denoiser = 'hqdn3d=9.0:5.0:3.0:3.0'

    def on_help(self, event):
        """
        """
        page = 'https://jeanslack.github.io/Videomass/Pages/Main_Toolbar/VideoConv_Panel/Filters/Denoisers.html'
        webbrowser.open(page)

    def on_reset(self, event):
        """
        Reset all option and values
        """
        self.denoiser = ''
        self.ckbx_nlmeans.SetValue(False)
        self.ckbx_hqdn3d.SetValue(False)
        self.ckbx_nlmeans.Enable()
        self.ckbx_hqdn3d.Enable()
        self.rdb_nlmeans.SetSelection(0)
        self.rdb_nlmeans.Disable()
        self.rdb_hqdn3d.SetSelection(0)
        self.rdb_hqdn3d.Disable()

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
        self.GetValue()
        event.Skip()

    def GetValue(self):
        """
        This method return values via the interface GetValue()
        """
        return self.denoiser