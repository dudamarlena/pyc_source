# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_frames/shownormlist.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 7603 bytes
import wx

class NormalizationList(wx.MiniFrame):
    __doc__ = '\n    Show FFmpeg volumedetect command data and report offset and gain\n    results need for normalization process.\n\n    '

    def __init__(self, title, data, OS):
        """
        detailslist is a list of items list.

        """
        wx.MiniFrame.__init__(self, None)
        self.panel = wx.Panel(self, (wx.ID_ANY), style=(wx.TAB_TRAVERSAL))
        normlist = wx.ListCtrl((self.panel), (wx.ID_ANY),
          style=(wx.LC_REPORT | wx.SUNKEN_BORDER))
        self.SetTitle(_(title))
        self.SetMinSize((850, 400))
        normlist.InsertColumn(0, (_('File name')), width=300)
        normlist.InsertColumn(1, (_('Max volume dBFS')), width=150)
        normlist.InsertColumn(2, (_('Mean volume dBFS')), width=150)
        normlist.InsertColumn(3, (_('Offset dBFS')), width=100)
        normlist.InsertColumn(4, (_('Result dBFS')), width=120)
        self.button_close = wx.Button(self.panel, wx.ID_CLOSE, '')
        descript = wx.StaticText(self.panel, wx.ID_ANY, _('Post-normalization references:'))
        red = wx.StaticText(self.panel, wx.ID_ANY, '\t')
        red.SetBackgroundColour(wx.Colour(233, 80, 77))
        txtred = wx.StaticText(self.panel, wx.ID_ANY, _('=  Clipped peaks'))
        grey = wx.StaticText(self.panel, wx.ID_ANY, '\t')
        grey.SetBackgroundColour(wx.Colour(100, 100, 100))
        txtgrey = wx.StaticText(self.panel, wx.ID_ANY, _('=  No changes'))
        yell = wx.StaticText(self.panel, wx.ID_ANY, '\t')
        yell.SetBackgroundColour(wx.Colour(198, 180, 38))
        txtyell = wx.StaticText(self.panel, wx.ID_ANY, _('=  Below max peak'))
        sizer = wx.BoxSizer(wx.VERTICAL)
        gridbtn = wx.GridSizer(1, 1, 0, 0)
        sizer.Add(normlist, 1, wx.EXPAND | wx.ALL, 5)
        grid_list = wx.FlexGridSizer(1, 7, 0, 0)
        grid_list.Add(descript, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        grid_list.Add(red, 1, wx.ALL, 5)
        grid_list.Add(txtred, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        grid_list.Add(grey, 1, wx.ALL, 5)
        grid_list.Add(txtgrey, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        grid_list.Add(yell, 1, wx.ALL, 5)
        grid_list.Add(txtyell, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        sizer.Add(grid_list, 0, wx.ALL, 5)
        sizer.Add(gridbtn, flag=(wx.ALIGN_RIGHT | wx.RIGHT), border=5)
        gridbtn.Add(self.button_close, 1, wx.ALL, 5)
        self.panel.SetSizerAndFit(sizer)
        if OS == 'Darwin':
            normlist.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
            descript.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD))
            txtred.SetFont(wx.Font(11, wx.SWISS, wx.ITALIC, wx.NORMAL))
            txtgrey.SetFont(wx.Font(11, wx.SWISS, wx.ITALIC, wx.NORMAL))
            txtyell.SetFont(wx.Font(11, wx.SWISS, wx.ITALIC, wx.NORMAL))
        else:
            normlist.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))
            descript.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD))
            txtred.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL))
            txtgrey.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL))
            txtyell.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL))
        self.Bind(wx.EVT_BUTTON, self.on_close, self.button_close)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        index = 0
        if title == _('RMS-based volume statistics'):
            for i in data:
                normlist.InsertItem(index, i[0])
                normlist.SetItem(index, 1, i[1])
                normlist.SetItem(index, 2, i[2])
                if float(i[3]) == 0.0:
                    normlist.SetItemBackgroundColour(index, '#646464')
                    normlist.SetItem(index, 3, i[3])
                else:
                    normlist.SetItem(index, 3, i[3])
                if float(i[4]) > 0.0:
                    normlist.SetItemBackgroundColour(index, '#e9504d')
                    normlist.SetItem(index, 4, i[4])
                else:
                    normlist.SetItem(index, 4, i[4])
                if float(i[4]) < float(i[1]):
                    normlist.SetItemBackgroundColour(index, '#C6B426')
                    normlist.SetItem(index, 4, i[4])
                else:
                    normlist.SetItem(index, 4, i[4])

        else:
            if title == _('PEAK-based volume statistics'):
                for i in data:
                    normlist.InsertItem(index, i[0])
                    normlist.SetItem(index, 1, i[1])
                    normlist.SetItem(index, 2, i[2])
                    normlist.SetItem(index, 3, i[3])
                    if float(i[4]) == float(i[1]):
                        normlist.SetItemBackgroundColour(index, '#646464')
                        normlist.SetItem(index, 4, i[4])
                    else:
                        normlist.SetItem(index, 4, i[4])
                    if float(i[4]) < float(i[1]):
                        normlist.SetItemBackgroundColour(index, '#C6B426')
                        normlist.SetItem(index, 4, i[4])
                    else:
                        normlist.SetItem(index, 4, i[4])

    def on_close(self, event):
        """
        destroy dialog by button and the X
        """
        self.Destroy()