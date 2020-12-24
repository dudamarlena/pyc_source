# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_dialogs/infoprg.py
# Compiled at: 2020-05-11 07:27:34
# Size of source mod 2**32: 3492 bytes
import wx, wx.adv
from videomass3.vdms_sys.msg_info import current_release
from videomass3.vdms_sys.msg_info import descriptions_release
cr = current_release()
Name = cr[0]
name = cr[1]
Version = cr[2]
Release = cr[3]
Copyright = cr[4]
Website = cr[5]
Author = cr[6]
Mail = cr[7]
Comment = cr[8]
dr = descriptions_release()
Short_Dscrp = dr[0]
Long_Dscrp = dr[1]
Short_Lic = dr[2]
Long_Lic = dr[3]

def info(parent, videomass_icon):
    """
    It's a predefined template to create a dialogue on
    the program information

    """
    info = wx.adv.AboutDialogInfo()
    info.SetIcon(wx.Icon(videomass_icon, type=(wx.BITMAP_TYPE_PNG)))
    info.SetName('%s' % Name)
    info.SetVersion('v%s' % Version)
    info.SetDescription(_('Multi-platform graphical interface for FFmpeg and youtube-dl.\n'))
    info.SetCopyright('Copyright %s %s' % (Copyright, Author))
    info.SetWebSite(Website)
    info.SetLicence(Long_Lic)
    info.AddDeveloper('%s %s' % (Author, Mail))
    info.AddDeveloper('Thanks to:')
    info.AddDeveloper('Python <https://www.python.org/>, programming language')
    info.AddDeveloper('wxPython <https://wxpython.org/>, cross-platform GUI toolkit for the Python language')
    info.AddDeveloper('FFmpeg <http://ffmpeg.org/>, a complete, cross-platform solution for media')
    info.AddDeveloper('youtube-dl <http://ytdl-org.github.io/youtube-dl/>, Download videos from YouTube and more sites')
    info.AddDocWriter('Gianluca Pernigotto <jeanlucperni@gmail.com>')
    info.SetArtists(['Gianluca Pernigotto <jeanlucperni@gmail.com>',
     'Material design icons http://google.github.io/material-design-icons/#getting-icons',
     'Flat Color Icons, http://icons8.com/color-icons'])
    info.AddTranslator('Gianluca Pernigotto <jeanlucperni@gmail.com> English to Italian translations.')
    wx.adv.AboutBox(info)