# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/wxcompat.py
# Compiled at: 2011-09-03 19:19:45
"""
@summary: wx Compatibility helper module

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: wxcompat.py 68998 2011-09-03 22:03:32Z CJP $'
__revision__ = '$Revision: 68998 $'
import os, wx
if wx.Platform == '__WXMAC__':
    if not hasattr(wx, 'MacThemeColour'):

        def MacThemeColour(theme_id):
            """Get a specified Mac theme colour
            @param theme_id: Carbon theme id
            @return: wx.Colour

            """
            brush = wx.Brush(wx.BLACK)
            brush.MacSetTheme(theme_id)
            return brush.GetColour()


        wx.MacThemeColour = MacThemeColour
    wx.SystemOptions.SetOptionInt('mac.textcontrol-use-spell-checker', 1)
elif wx.Platform == '__WXGTK__':
    os.environ['LIBOVERLAY_SCROLLBAR'] = '0'
if wx.VERSION < (2, 8, 6, 0, ''):
    wx.MenuItem.GetItemLabel = wx.MenuItem.GetText
    wx.MenuItem.GetItemLabelText = wx.MenuItem.GetLabel