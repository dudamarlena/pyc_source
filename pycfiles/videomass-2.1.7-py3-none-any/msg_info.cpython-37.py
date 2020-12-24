# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gianluca/Pubblici/GIThub/MASTER/Videomass/videomass3/vdms_sys/msg_info.py
# Compiled at: 2020-05-11 07:51:46
# Size of source mod 2**32: 4439 bytes


def current_release():
    """
    General info strings
    NOTE: number version > major number.minor number.micro number(patch number)
    the sub release a=alpha release, b=beta release, c= candidate release
    Example 19.1.1c1
    """
    Release_Name = 'Videomass'
    Program_Name = 'videomass'
    Version = '2.1.7'
    Release = 'May 11 2020'
    Copyright = '© 2013-2020'
    Website = 'http://jeanslack.github.io/Videomass/'
    Author = 'Gianluca Pernigotto (aka jeanslack)'
    Mail = '<jeanlucperni@gmail.com>'
    Comment = '\nThanks to:\n- Python <https://www.python.org/>, programming language\n- wxPython <https://wxpython.org/>, cross-platform\nGUI toolkit for the Python language\n- FFmpeg, FFmpeg is a trademark of Fabrice Bellard, \noriginator of the FFmpeg project:\n<http://ffmpeg.org/>\n- youtube-dl: <http://ytdl-org.github.io/youtube-dl\nDownload videos from YouTube and more sites\n- Material design icons from Google:\nhttp://google.github.io/material-design-icons/#getting-icons\n- Flat Color Icons:\nhttps://icons8.com/color-icons'
    return (
     Release_Name, Program_Name, Version, Release,
     Copyright, Website, Author, Mail, Comment)


def descriptions_release():
    """
    General info string
    """
    Copyright = current_release()
    Author = current_release()
    Mail = current_release()
    short_d = 'Videomass is a cross-platform GUI for FFmpeg and youtube-dl'
    long_d = 'Videomass is not a converter; It provides a graphical interface for writing presets and profiles to be used with FFmpeg without limits on formats and codecs; it also provides a minimal graphical interface with the basic functions for youtube_dl video downloader.\n'
    short_l = 'GPL3 (Gnu Public License)'
    license = 'Copyright - %s %s\nAuthor and Developer: %s\nMail: %s\n\nVideomass is free software: you can redistribute\nit and/or modify it under the terms of the GNU General\nPublic License as published by the Free Software\nFoundation, either version 3 of the License, or (at your\noption) any later version.\n\nVideomass is distributed in the hope that it\nwill be useful, but WITHOUT ANY WARRANTY; without\neven the implied warranty of MERCHANTABILITY or\nFITNESS FOR A PARTICULAR PURPOSE.\nSee the GNU General Public License for more details.\n\nYou should have received a copy of the GNU General\nPublic License along with this program. If not, see\nhttp://www.gnu.org/licenses/' % (
     Copyright[4],
     Author[6],
     Author[6],
     Mail[7])
    return (short_d, long_d, short_l, license)