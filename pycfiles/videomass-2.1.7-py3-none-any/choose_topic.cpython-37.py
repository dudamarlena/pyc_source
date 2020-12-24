# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_panels/choose_topic.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 9421 bytes
import wx
import wx.lib.agw.hyperlink as hpl
from videomass3.vdms_io import IO_tools
from videomass3.vdms_sys.msg_info import current_release
import os, shutil
get = wx.GetApp()
OS = get.OS
PYLIB_YDL = get.pylibYdl
EXEC_YDL = get.execYdl
msgready = _('Successful! \n\nyoutube-dl is ready\n\nImportant: youtube-dl is very often updated, remember to check for updates weekly.\nYou can use the dedicated functions in the menu bar of Videomass: Tools/youtube-dl" .\n\nDo you want to close Videomass now and restart it manually?')
if OS == 'Windows':
    msg = _('{}\n\nTo download video from YouTube.com and other video sites, Videomass needs an updated\nversion of youtube-dl.exe from https://github.com/ytdl-org/youtube-dl/releases\n\n- Requires: Microsoft Visual C++ 2010 Redistributable Package (x86)\n   for major information visit http://ytdl-org.github.io/youtube-dl/download.html\n\nDo you want to download youtube-dl now?').format(PYLIB_YDL)
else:
    if OS == 'Darwin':
        msg = _('{}\n\nTo download video from YouTube.com and other video sites, Videomass needs an updated version of youtube-dl from https://github.com/ytdl-org/youtube-dl/releases\n\nDo you want to download youtube-dl now?').format(PYLIB_YDL)
    else:
        msg = _('{}\n\nTo download video from YouTube.com and other video sites, Videomass needs an updated version of youtube-dl.\nVideomass recommends pip to install youtube-dl and keep it updated by the user.\n\nHowever, an updated copy of youtube-dl can be downloaded locally.\n\n...Do you wish to continue?').format(PYLIB_YDL)
        msgerr = _('{}\n\nyoutube-dl: no library or executable found .').format(PYLIB_YDL)
prst_mng = _('  Presets Manager - Create, edit and use quickly your favorite\n  FFmpeg presets and profiles with full formats support and codecs. ')
video_lab = _('  A set of useful tools for audio and video manipulations;\n  convert or save your profiles and reuse them with Presets Manager. ')
youtube_lab = _('  Easily download videos and audio in different formats\n  and quality from YouTube, Facebook and more sites. ')

class Choose_Topic(wx.Panel):
    __doc__ = '\n    Helps to choose the appropriate contextual panel\n    '

    def __init__(self, parent, OS, videoconv_icn, youtube_icn, prstmng_icn):
        self.parent = parent
        self.oS = OS
        version = current_release()
        wx.Panel.__init__(self, parent, -1)
        welcome = wx.StaticText(self, wx.ID_ANY, _('Welcome to Videomass'))
        version = wx.StaticText(self, wx.ID_ANY, _('Version {}').format(version[2]))
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        grid_buttons = wx.FlexGridSizer(5, 0, 20, 20)
        grid_base = wx.GridSizer(1, 1, 0, 0)
        self.presets_mng = wx.Button(self, (wx.ID_ANY), prst_mng, size=(-1, -1),
          style=(wx.BU_LEFT | wx.NO_BORDER))
        self.presets_mng.SetBitmap(wx.Bitmap(prstmng_icn), wx.LEFT)
        self.video = wx.Button(self, (wx.ID_ANY), video_lab, size=(-1, -1),
          style=(wx.BU_LEFT | wx.BORDER_NONE))
        self.video.SetBitmap(wx.Bitmap(videoconv_icn), wx.LEFT)
        self.youtube = wx.Button(self, (wx.ID_ANY), youtube_lab, size=(-1, -1),
          style=(wx.BU_LEFT | wx.BORDER_NONE))
        self.youtube.SetBitmap(wx.Bitmap(youtube_icn), wx.LEFT)
        grid_buttons.AddMany([
         (welcome, 0,
          wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 0),
         (
          version, 0,
          wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 20),
         (
          self.presets_mng, 0, wx.EXPAND, 5),
         (
          self.video, 0, wx.EXPAND, 5),
         (
          self.youtube, 0, wx.EXPAND, 5)])
        grid_base.Add(grid_buttons, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        sizer_base.Add(grid_base, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        sizer_hpl = wx.BoxSizer(wx.HORIZONTAL)
        sizer_base.Add(sizer_hpl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 15)
        txt_link = wx.StaticText(self, label=(_('Download additional presets or contribute to making new ones ')))
        link = hpl.HyperLinkCtrl(self, (-1), (_('Additional Presets')), URL='https://github.com/jeanslack/Videomass-presets')
        sizer_hpl.Add(txt_link)
        sizer_hpl.Add(link)
        self.SetSizerAndFit(sizer_base)
        if OS == 'Darwin':
            welcome.SetFont(wx.Font(13, wx.SWISS, wx.NORMAL, wx.BOLD))
            version.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL))
        else:
            welcome.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL))
            version.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.LIGHT))
        self.Bind(wx.EVT_BUTTON, self.on_Video, self.video)
        self.Bind(wx.EVT_BUTTON, self.on_Prst_mng, self.presets_mng)
        self.Bind(wx.EVT_BUTTON, self.on_YoutubeDL, self.youtube)

    def on_Video(self, event):
        self.parent.switch_file_import(self, 'Audio/Video Conversions')

    def on_YoutubeDL(self, event):
        """
        Check the installation of youtube-dl depending on the OS in use.
        """
        if PYLIB_YDL is None:
            self.parent.switch_text_import(self, 'Youtube Downloader')
            return
            if EXEC_YDL:
                if os.path.isfile(EXEC_YDL):
                    self.parent.switch_text_import(self, 'Youtube Downloader')
                    return
                if OS in ('Windows', 'Darwin'):
                    if wx.MessageBox(msg, _('Videomass confirmation'), wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                        return
        elif wx.MessageBox(msg, _('Videomass confirmation'), wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
            return
        latest = self.parent.ydl_latest(self, msgbox=False)
        if latest[1]:
            return
        upgrade = IO_tools.youtubedl_upgrade(latest[0], EXEC_YDL)
        if upgrade[1]:
            wx.MessageBox('%s' % upgrade[1], 'Videomass error', wx.ICON_ERROR, self)
            return
        if wx.MessageBox(msgready, 'Videomass', wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
            return
            self.parent.on_Kill()
            return
        else:
            if EXEC_YDL is False:
                wx.MessageBox(msgerr, 'Videomass error', wx.ICON_ERROR)
                return

    def on_Prst_mng(self, event):
        self.parent.switch_file_import(self, 'Presets Manager')