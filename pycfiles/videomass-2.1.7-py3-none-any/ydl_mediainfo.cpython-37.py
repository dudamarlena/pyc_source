# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_frames/ydl_mediainfo.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 6273 bytes
import wx, os

class YDL_Mediainfo(wx.MiniFrame):
    __doc__ = '\n    Display streams information from youtube-dl data.\n    '

    def __init__(self, data, OS):
        """
        NOTE constructor:: with 'None' not depend from videomass.
        With 'parent, -1' if close videomass also close mediainfo window
        """
        self.data = data
        wx.MiniFrame.__init__(self, None)
        self.panel = wx.Panel(self, (wx.ID_ANY), style=(wx.TAB_TRAVERSAL))
        self.url_select = wx.ListCtrl((self.panel), (wx.ID_ANY),
          style=(wx.LC_REPORT | wx.SUNKEN_BORDER))
        self.textCtrl = wx.TextCtrl((self.panel), (wx.ID_ANY),
          '', style=(wx.TE_MULTILINE | wx.TE_DONTWRAP))
        button_close = wx.Button(self.panel, wx.ID_CLOSE, '')
        self.SetTitle('Videomass - Multimedia Streams Information')
        self.SetMinSize((640, 400))
        self.url_select.SetMinSize((640, 200))
        self.url_select.InsertColumn(0, (_('TITLE')), width=250)
        self.url_select.InsertColumn(1, (_('URL')), width=500)
        self.textCtrl.SetMinSize((640, 300))
        if OS == 'Darwin':
            self.url_select.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
            self.textCtrl.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.BOLD))
        else:
            self.url_select.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))
            self.textCtrl.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.BOLD))
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.url_select, 0, wx.ALL | wx.EXPAND, 5)
        grid_sizer_1 = wx.GridSizer(1, 1, 0, 0)
        sizer_1.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.textCtrl, 0, wx.ALL | wx.EXPAND, 5)
        grid_buttons = wx.GridSizer(1, 1, 0, 0)
        grid_buttons.Add(button_close, 1, wx.ALL, 5)
        sizer_1.Add(grid_buttons, flag=(wx.ALIGN_RIGHT | wx.RIGHT), border=0)
        self.panel.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        index = 0
        for url in self.data:
            self.url_select.InsertItem(index, url['title'])
            self.url_select.SetItem(index, 1, url['url'])
            index += 1

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select, self.url_select)
        self.Bind(wx.EVT_BUTTON, self.on_close, button_close)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_select(self, event):
        """
        show data during items selection

        """
        self.textCtrl.Clear()
        index = self.url_select.GetFocusedItem()
        item = self.url_select.GetItemText(index)
        for info in self.data:
            if info['title'] == item:
                text = 'Categories:      {}\nLicense:         {}\nUpload Date:     {}\nUploader:        {}\nView Count:      {}\nLike Count:      {}\nDislike Count:   {}\nAverage Rating:  {}\nID:              {}\nDuration:        {}\nDescription:     {}\n'.format(info['categories'], info['license'], info['upload_date'], info['uploader'], info['view'], info['like'], info['dislike'], info['average_rating'], info['id'], info['duration'], info['description'])

        self.textCtrl.AppendText(text)

    def on_close(self, event):
        self.Destroy()