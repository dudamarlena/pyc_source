# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_frames/ffmpeg_codecs.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 9701 bytes
import wx

class FFmpeg_Codecs(wx.MiniFrame):
    __doc__ = '\n    It shows a dialog box with a pretty kind of GUI to view\n    the formats available on FFmpeg\n    '

    def __init__(self, dict_decoders, OS, type_opt):
        """
        with 'None' not depend from parent:
        wx.Dialog.__init__(self, None, style=wx.DEFAULT_DIALOG_STYLE)

        With parent, -1:
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE)
        if close videomass also close parent window:
        """
        if type_opt == '-encoders':
            cod = _('CODING ABILITY')
            colctrl = 'ORANGE'
            title = _('Videomass: FFmpeg encoders')
        else:
            cod = _('DECODING CAPABILITY')
            colctrl = 'SIENNA'
            title = _('Videomass: FFmpeg decoders')
        wx.MiniFrame.__init__(self, None)
        self.panel = wx.Panel(self, (wx.ID_ANY), style=(wx.TAB_TRAVERSAL))
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        notebook = wx.Notebook(self.panel, wx.ID_ANY)
        sizer_base.Add(notebook, 1, wx.ALL | wx.EXPAND, 5)
        nb_panel_1 = wx.Panel(notebook, wx.ID_ANY)
        vid = wx.ListCtrl(nb_panel_1, (wx.ID_ANY), style=(wx.LC_REPORT | wx.SUNKEN_BORDER))
        sizer_tab1 = wx.BoxSizer(wx.VERTICAL)
        sizer_tab1.Add(vid, 1, wx.ALL | wx.EXPAND, 5)
        nb_panel_1.SetSizer(sizer_tab1)
        notebook.AddPage(nb_panel_1, _('Video'))
        nb_panel_2 = wx.Panel(notebook, wx.ID_ANY)
        aud = wx.ListCtrl(nb_panel_2, (wx.ID_ANY), style=(wx.LC_REPORT | wx.SUNKEN_BORDER))
        sizer_tab2 = wx.BoxSizer(wx.VERTICAL)
        sizer_tab2.Add(aud, 1, wx.ALL | wx.EXPAND, 5)
        nb_panel_2.SetSizer(sizer_tab2)
        notebook.AddPage(nb_panel_2, _('Audio'))
        nb_panel_3 = wx.Panel(notebook, wx.ID_ANY)
        sub = wx.ListCtrl(nb_panel_3, (wx.ID_ANY), style=(wx.LC_REPORT | wx.SUNKEN_BORDER))
        sizer_tab3 = wx.BoxSizer(wx.VERTICAL)
        sizer_tab3.Add(sub, 1, wx.ALL | wx.EXPAND, 5)
        nb_panel_3.SetSizer(sizer_tab3)
        notebook.AddPage(nb_panel_3, _('Subtitle'))
        stext = wx.StaticText(self.panel, wx.ID_ANY, '')
        sizer_base.Add(stext, 0, wx.ALL | wx.EXPAND, 5)
        button_close = wx.Button(self.panel, wx.ID_CLOSE, '')
        grid_buttons = wx.GridSizer(1, 1, 0, 0)
        grid_buttons.Add(button_close, 1, wx.ALL, 5)
        sizer_base.Add(grid_buttons, flag=(wx.ALIGN_RIGHT | wx.RIGHT), border=0)
        self.panel.SetSizerAndFit(sizer_base)
        self.Layout()
        self.SetTitle(title)
        self.SetMinSize((700, 500))
        vid.InsertColumn(0, 'codec', width=150)
        vid.InsertColumn(1, 'F', width=40)
        vid.InsertColumn(2, 'S', width=40)
        vid.InsertColumn(3, 'X', width=40)
        vid.InsertColumn(4, 'B', width=40)
        vid.InsertColumn(5, 'D', width=40)
        vid.InsertColumn(6, (_('description')), width=450)
        aud.InsertColumn(0, 'codec', width=150)
        aud.InsertColumn(1, 'F', width=40)
        aud.InsertColumn(2, 'S', width=40)
        aud.InsertColumn(3, 'X', width=40)
        aud.InsertColumn(4, 'B', width=40)
        aud.InsertColumn(5, 'D', width=40)
        aud.InsertColumn(6, (_('description')), width=450)
        sub.InsertColumn(0, 'codec', width=150)
        sub.InsertColumn(1, 'F', width=40)
        sub.InsertColumn(2, 'S', width=40)
        sub.InsertColumn(3, 'X', width=40)
        sub.InsertColumn(4, 'B', width=40)
        sub.InsertColumn(5, 'D', width=40)
        sub.InsertColumn(6, (_('description')), width=450)
        if OS == 'Darwin':
            vid.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
            aud.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
            sub.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
            stext.SetFont(wx.Font(11, wx.SWISS, wx.ITALIC, wx.NORMAL))
        else:
            vid.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))
            aud.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))
            sub.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))
            stext.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL))
        leg = 'F = frame-level multithreading\nS = slice-level multithreading\nX = Codec is experimental\nB = Supports draw_horiz_band\nD = Supports direct rendering method 1'
        stext.SetLabel(leg)
        index = 0
        vcodlist = dict_decoders['Video']
        if not vcodlist:
            print('No ffmpeg codecs available')
        else:
            vid.InsertItem(index, cod)
            vid.SetItemBackgroundColour(index, colctrl)
            for a in vcodlist:
                index += 1
                vid.InsertItem(index, a[6:].split(' ')[1])
                if 'F' in a[1]:
                    vid.SetItem(index, 1, 'YES')
                if 'S' in a[2]:
                    vid.SetItem(index, 2, 'YES')
                if 'X' in a[3]:
                    vid.SetItem(index, 3, 'YES')
                if 'B' in (4, ):
                    vid.SetItem(index, 4, 'YES')
                if 'D' in (5, ):
                    vid.SetItem(index, 5, 'YES')
                d = ' '.join(a.split()).split(None, 2)[2]
                if len(d):
                    vid.SetItem(index, 6, d)
                else:
                    vid.SetItem(index, 6, '')

        index = 0
        acodlist = dict_decoders['Audio']
        if not acodlist:
            print('No ffmpeg codecs available')
        else:
            aud.InsertItem(index, cod)
            aud.SetItemBackgroundColour(index, colctrl)
            for a in acodlist:
                index += 1
                aud.InsertItem(index, a[6:].split(' ')[1])
                if 'F' in a[1]:
                    aud.SetItem(index, 1, 'YES')
                if 'S' in a[2]:
                    aud.SetItem(index, 2, 'YES')
                if 'X' in a[3]:
                    aud.SetItem(index, 3, 'YES')
                if 'B' in (4, ):
                    aud.SetItem(index, 4, 'YES')
                if 'D' in (5, ):
                    aud.SetItem(index, 5, 'YES')
                d = ' '.join(a.split()).split(None, 2)[2]
                if len(d):
                    aud.SetItem(index, 6, d)
                else:
                    aud.SetItem(index, 6, '')

        index = 0
        scodlist = dict_decoders['Subtitle']
        if not scodlist:
            print('No ffmpeg codecs available')
        else:
            sub.InsertItem(index, cod)
            sub.SetItemBackgroundColour(index, colctrl)
            for a in scodlist:
                index += 1
                sub.InsertItem(index, a[6:].split(' ')[1])
                if 'F' in a[1]:
                    sub.SetItem(index, 1, 'YES')
                if 'S' in a[2]:
                    sub.SetItem(index, 2, 'YES')
                if 'X' in a[3]:
                    sub.SetItem(index, 3, 'YES')
                if 'B' in (4, ):
                    sub.SetItem(index, 4, 'YES')
                if 'D' in (5, ):
                    sub.SetItem(index, 5, 'YES')
                d = ' '.join(a.split()).split(None, 2)[2]
                if len(d):
                    sub.SetItem(index, 6, d)
                else:
                    sub.SetItem(index, 6, '')

        self.Bind(wx.EVT_BUTTON, self.on_close, button_close)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        self.Destroy()