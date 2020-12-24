# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\chirp\gui\HelpWindow.py
# Compiled at: 2013-12-11 23:17:46
"""
Display help information in HTML dialogs
"""
from chirp import version
from matplotlib import __version__ as mplver
import wx, wx.html
vers = dict(wxver=wx.VERSION_STRING, mplver=mplver, **version.lib_versions())
about_txt = '\n<p>This is Chirp version %(chirp)s, Copyright (C) 2012 Dan Meliza</p>\n\n<br/>\n<table border="0" cellpadding="0">\n<tr>\n<td colspan="2">Component libraries:</td>\n</tr>\n<tr><td>Python</td><td>%(python)s</td></tr>\n<tr><td>wxpython</td><td>%(wxver)s</td></tr>\n<tr><td>matplotlib</td><td>%(mplver)s</td></tr>\n<tr><td>libtfr</td><td>%(libtfr)s</td></tr>\n<tr><td>GEOS/shapely</td><td>%(geos)s</td></tr>\n</table>\n<br/>\n\n<p><a href="http://github.com/dmeliza/chirp">Project Site</a></p>\n' % vers
help_txt = '\n<table border="0" cellpadding="0">\n<tr>\n<td colspan="2">Spectrogram Navigation:</td>\n</tr>\n<tr><td>left mouse:</td><td>start drawing polygon; click to close</td></tr>\n<tr><td>middle mouse:</td><td>drag to highlight temporal interval</td></tr>\n<tr><td>right mouse:</td><td>drag to zoom to frequency range</td></tr>\n<tr><td>down arrow:</td><td>zoom in to temporal interval</td></tr>\n<tr><td>up arrow:</td><td>zoom out to previous temporal range</td></tr>\n<tr><td>shift up arrow:</td><td>zoom out to previous freqency range</td></tr>\n<tr><td>left arrow:</td><td>pan to earlier segment</td></tr>\n<tr><td>right arrow:</td><td>pan to later segment</td></tr>\n</table>\n<p>\n\n<table border="0" cellpadding="0">\n<tr>\n<td colspan="2">Element creation:</td>\n</tr>\n<tr><td>s:</td><td>create element using current selection (temporal interval or polygon)</td></tr>\n<tr><td>x:</td><td>subtract current drawn polygon from all polygon elements</td></tr>\n<tr><td>a:</td><td>add current drawn polygon to all polygon elements</td></tr>\n<tr><td>p:</td><td>play audio of current selection (if supported)</td></tr>\n</table>\n'

class HtmlWindow(wx.html.HtmlWindow):

    def __init__(self, parent, id, size=(600, 400)):
        wx.html.HtmlWindow.__init__(self, parent, id, size=size)
        if 'gtk2' in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())


class AboutBox(wx.Dialog):

    def __init__(self, parent=None, title='', text=''):
        wx.Dialog.__init__(self, parent, -1, title, style=wx.DEFAULT_DIALOG_STYLE | wx.THICK_FRAME | wx.RESIZE_BORDER)
        hwin = HtmlWindow(self, -1, size=(400, 200))
        hwin.SetPage(text)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth() + 25, irep.GetHeight() + 10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()