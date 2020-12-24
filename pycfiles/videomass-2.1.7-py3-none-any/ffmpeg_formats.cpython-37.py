# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_frames/ffmpeg_formats.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 7443 bytes
import wx

class FFmpeg_formats(wx.MiniFrame):
    __doc__ = '\n    It shows a dialog box with a pretty kind of GUI to view\n    the formats available on FFmpeg\n\n    '

    def __init__(self, dict_formats, OS):
        """
        with 'None' not depend from parent:
        wx.Dialog.__init__(self, None, style=wx.DEFAULT_DIALOG_STYLE)

        With parent, -1:
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE)
        if close videomass also close parent window:

        """
        wx.MiniFrame.__init__(self, None)
        self.panel = wx.Panel(self, (wx.ID_ANY), style=(wx.TAB_TRAVERSAL))
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        notebook = wx.Notebook(self.panel, wx.ID_ANY)
        sizer_base.Add(notebook, 1, wx.ALL | wx.EXPAND, 5)
        notebook_pane_1 = wx.Panel(notebook, wx.ID_ANY)
        dmx = wx.ListCtrl(notebook_pane_1, (wx.ID_ANY),
          style=(wx.LC_REPORT | wx.SUNKEN_BORDER))
        sizer_tab1 = wx.BoxSizer(wx.VERTICAL)
        sizer_tab1.Add(dmx, 1, wx.ALL | wx.EXPAND, 5)
        notebook_pane_1.SetSizer(sizer_tab1)
        notebook.AddPage(notebook_pane_1, _('Demuxing only'))
        notebook_pane_2 = wx.Panel(notebook, wx.ID_ANY)
        mx = wx.ListCtrl(notebook_pane_2, (wx.ID_ANY),
          style=(wx.LC_REPORT | wx.SUNKEN_BORDER))
        sizer_tab2 = wx.BoxSizer(wx.VERTICAL)
        sizer_tab2.Add(mx, 1, wx.ALL | wx.EXPAND, 5)
        notebook_pane_2.SetSizer(sizer_tab2)
        notebook.AddPage(notebook_pane_2, _('Muxing only'))
        notebook_pane_3 = wx.Panel(notebook, wx.ID_ANY)
        dmx_mx = wx.ListCtrl(notebook_pane_3, (wx.ID_ANY),
          style=(wx.LC_REPORT | wx.SUNKEN_BORDER))
        sizer_tab3 = wx.BoxSizer(wx.VERTICAL)
        sizer_tab3.Add(dmx_mx, 1, wx.ALL | wx.EXPAND, 5)
        notebook_pane_3.SetSizer(sizer_tab3)
        notebook.AddPage(notebook_pane_3, _('Demuxing/Muxing support'))
        button_close = wx.Button(self.panel, wx.ID_CLOSE, '')
        grid_buttons = wx.GridSizer(1, 1, 0, 0)
        grid_buttons.Add(button_close, 1, wx.ALL, 5)
        sizer_base.Add(grid_buttons, flag=(wx.ALIGN_RIGHT | wx.RIGHT), border=0)
        self.panel.SetSizerAndFit(sizer_base)
        self.Layout()
        self.SetTitle(_('Videomass: FFmpeg file formats'))
        self.SetMinSize((500, 400))
        dmx.InsertColumn(0, (_('format')), width=150)
        dmx.InsertColumn(1, (_('description')), width=450)
        mx.InsertColumn(0, (_('format')), width=150)
        mx.InsertColumn(1, (_('description')), width=450)
        dmx_mx.InsertColumn(0, (_('format')), width=150)
        dmx_mx.InsertColumn(1, (_('description')), width=450)
        if OS == 'Darwin':
            dmx.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
            mx.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
            dmx_mx.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
        else:
            dmx.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))
            mx.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))
            dmx_mx.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))
        dmx.DeleteAllItems()
        mx.DeleteAllItems()
        dmx_mx.DeleteAllItems()
        index = 0
        ds = dict_formats['Demuxing Supported']
        if not ds:
            print('No ffmpeg formats available')
        else:
            dmx.InsertItem(index, '----')
            dmx.SetItemBackgroundColour(index, 'CORAL')
            for a in ds:
                s = ' '.join(a.split()).split(None, 1)
                if len(s) == 1:
                    key, value = s[0], ''
                else:
                    key, value = s[0], s[1]
                index += 1
                dmx.InsertItem(index, key)
                dmx.SetItem(index, 1, value)

        index = 0
        ms = dict_formats['Muxing Supported']
        if not ms:
            print('No ffmpeg formats available')
        else:
            mx.InsertItem(index, '----')
            mx.SetItemBackgroundColour(index, 'CORAL')
            for a in ms:
                s = ' '.join(a.split()).split(None, 1)
                if len(s) == 1:
                    key, value = s[0], ''
                else:
                    key, value = s[0], s[1]
                index += 1
                mx.InsertItem(index, key)
                mx.SetItem(index, 1, value)

        index = 0
        mds = dict_formats['Mux/Demux Supported']
        if not mds:
            print('No ffmpeg formats available')
        else:
            dmx_mx.InsertItem(index, '----')
            dmx_mx.SetItemBackgroundColour(index, 'CORAL')
            for a in mds:
                s = ' '.join(a.split()).split(None, 1)
                if len(s) == 1:
                    key, value = s[0], ''
                else:
                    key, value = s[0], s[1]
                index += 1
                dmx_mx.InsertItem(index, key)
                dmx_mx.SetItem(index, 1, value)

        self.Bind(wx.EVT_BUTTON, self.on_close, button_close)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        self.Destroy()