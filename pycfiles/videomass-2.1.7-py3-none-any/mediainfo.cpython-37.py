# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_frames/mediainfo.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 11346 bytes
import wx, os, webbrowser

class Mediainfo(wx.MiniFrame):
    __doc__ = '\n    Display streams information from ffprobe json data.\n    '

    def __init__(self, data, OS):
        """
        NOTE constructor:: with 'None' not depend from videomass.
        With 'parent, -1' if close videomass also close mediainfo window
        """
        self.data = data
        wx.MiniFrame.__init__(self, None)
        self.panel = wx.Panel(self, (wx.ID_ANY), style=(wx.TAB_TRAVERSAL))
        self.file_select = wx.ListCtrl((self.panel), (wx.ID_ANY),
          style=(wx.LC_REPORT | wx.SUNKEN_BORDER))
        notebook = wx.Notebook(self.panel, wx.ID_ANY)
        nb_panel_1 = wx.Panel(notebook, wx.ID_ANY)
        self.format_ctrl = wx.ListCtrl(nb_panel_1, (wx.ID_ANY),
          style=(wx.LC_REPORT | wx.SUNKEN_BORDER))
        nb_panel_2 = wx.Panel(notebook, wx.ID_ANY)
        self.video_ctrl = wx.ListCtrl(nb_panel_2, (wx.ID_ANY),
          style=(wx.LC_REPORT | wx.SUNKEN_BORDER))
        nb_panel_3 = wx.Panel(notebook, wx.ID_ANY)
        self.audio_ctrl = wx.ListCtrl(nb_panel_3, (wx.ID_ANY),
          style=(wx.LC_REPORT | wx.SUNKEN_BORDER))
        nb_panel_4 = wx.Panel(notebook, wx.ID_ANY)
        self.subtitle_ctrl = wx.ListCtrl(nb_panel_4, (wx.ID_ANY),
          style=(wx.LC_REPORT | wx.SUNKEN_BORDER))
        button_close = wx.Button(self.panel, wx.ID_CLOSE, '')
        self.SetTitle('Videomass - Multimedia Streams Information')
        self.SetMinSize((640, 400))
        self.file_select.SetMinSize((640, 200))
        self.file_select.InsertColumn(0, (_('File Selection')), width=500)
        self.format_ctrl.SetMinSize((640, 300))
        self.format_ctrl.InsertColumn(0, (_('References')), width=200)
        self.format_ctrl.InsertColumn(1, (_('Parameters')), width=450)
        self.video_ctrl.InsertColumn(0, (_('References')), width=200)
        self.video_ctrl.InsertColumn(1, (_('Parameters')), width=450)
        self.audio_ctrl.InsertColumn(0, (_('References')), width=200)
        self.audio_ctrl.InsertColumn(1, (_('Parameters')), width=450)
        self.subtitle_ctrl.InsertColumn(0, (_('References')), width=200)
        self.subtitle_ctrl.InsertColumn(1, (_('Parameters')), width=450)
        if OS == 'Darwin':
            self.file_select.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
            self.format_ctrl.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
            self.video_ctrl.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
            self.audio_ctrl.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
            self.subtitle_ctrl.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
        else:
            self.file_select.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))
            self.video_ctrl.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))
            self.format_ctrl.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))
            self.audio_ctrl.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))
            self.subtitle_ctrl.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.file_select, 0, wx.ALL | wx.EXPAND, 5)
        grid_sizer_1 = wx.GridSizer(1, 1, 0, 0)
        grid_buttons = wx.GridSizer(1, 1, 0, 0)
        sizer_tab1 = wx.BoxSizer(wx.VERTICAL)
        sizer_tab1.Add(self.format_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        nb_panel_1.SetSizer(sizer_tab1)
        sizer_tab2 = wx.BoxSizer(wx.VERTICAL)
        sizer_tab2.Add(self.video_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        nb_panel_2.SetSizer(sizer_tab2)
        sizer_tab3 = wx.BoxSizer(wx.VERTICAL)
        sizer_tab3.Add(self.audio_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        nb_panel_3.SetSizer(sizer_tab3)
        sizer_tab4 = wx.BoxSizer(wx.VERTICAL)
        sizer_tab4.Add(self.subtitle_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        nb_panel_4.SetSizer(sizer_tab4)
        notebook.AddPage(nb_panel_1, _('Data Format'))
        notebook.AddPage(nb_panel_2, _('Video Stream'))
        notebook.AddPage(nb_panel_3, _('Audio Streams'))
        notebook.AddPage(nb_panel_4, _('Subtitle Streams'))
        grid_sizer_1.Add(notebook, 1, wx.ALL | wx.EXPAND, 5)
        grid_buttons.Add(button_close, 1, wx.ALL, 5)
        sizer_1.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        sizer_1.Add(grid_buttons, flag=(wx.ALIGN_RIGHT | wx.RIGHT), border=0)
        self.panel.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        flist = [x['format']['filename'] for x in self.data if x['format']['filename']]
        index = 0
        for f in flist:
            self.file_select.InsertItem(index, f)
            index += 1

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select, self.file_select)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_desel, self.file_select)
        self.Bind(wx.EVT_BUTTON, self.on_close, button_close)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_desel(self, event):
        """
        """
        pass

    def on_select(self, event):
        """
        show data during items selection

        """
        self.format_ctrl.DeleteAllItems()
        self.video_ctrl.DeleteAllItems()
        self.audio_ctrl.DeleteAllItems()
        self.subtitle_ctrl.DeleteAllItems()
        index = self.file_select.GetFocusedItem()
        item = self.file_select.GetItemText(index)
        index = 0
        for x in self.data:
            if x.get('format').get('filename') == item:
                select = self.data[self.data.index(x)]
                num_items = self.format_ctrl.GetItemCount()
                self.format_ctrl.InsertItem(num_items, 'DATA FORMAT:')
                self.format_ctrl.SetItemBackgroundColour(index, 'GOLD')
                index += 1
                for k, v in x.get('format').items():
                    self.format_ctrl.InsertItem(index, str(k))
                    self.format_ctrl.SetItem(index, 1, str(v))
                    index += 1

        if select.get('streams'):
            index = 0
            for t in select.get('streams'):
                if t.get('codec_type') == 'video':
                    num_items = self.video_ctrl.GetItemCount()
                    n = 'VIDEO INDEX %d' % t.get('index')
                    self.video_ctrl.InsertItem(num_items, n)
                    self.video_ctrl.SetItemBackgroundColour(index, 'SLATE BLUE')
                    index += 1
                    for k, v in t.items():
                        self.video_ctrl.InsertItem(index, str(k))
                        self.video_ctrl.SetItem(index, 1, str(v))
                        index += 1

            index = 0
            for t in select.get('streams'):
                if t.get('codec_type') == 'audio':
                    num_items = self.audio_ctrl.GetItemCount()
                    n = 'AUDIO INDEX %d' % t.get('index')
                    self.audio_ctrl.InsertItem(num_items, n)
                    self.audio_ctrl.SetItemBackgroundColour(index, 'GREEN')
                    index += 1
                    for k, v in t.items():
                        self.audio_ctrl.InsertItem(index, str(k))
                        self.audio_ctrl.SetItem(index, 1, str(v))
                        index += 1

            index = 0
            for t in select.get('streams'):
                if t.get('codec_type') == 'subtitle':
                    num_items = self.subtitle_ctrl.GetItemCount()
                    n = 'SUBTITLE INDEX %d' % t.get('index')
                    self.subtitle_ctrl.InsertItem(num_items, n)
                    self.subtitle_ctrl.SetItemBackgroundColour(index, 'GOLDENROD')
                    index += 1
                    for k, v in t.items():
                        self.subtitle_ctrl.InsertItem(index, str(k))
                        self.subtitle_ctrl.SetItem(index, 1, str(v))
                        index += 1

    def on_close(self, event):
        self.Destroy()