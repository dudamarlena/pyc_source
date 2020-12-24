# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/eclib/elistmix.py
# Compiled at: 2010-12-05 17:39:30
"""
Editra Control Library: EListMixins

Class ListRowHighlighter:
This mixin class can be used to add automatic highlighting of alternate rows
in a ListCtrl.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: elistmix.py 66204 2010-11-18 14:00:28Z CJP $'
__revision__ = '$Revision: 66204 $'
__all__ = [
 'ListRowHighlighter', 'HIGHLIGHT_EVEN', 'HIGHLIGHT_ODD']
import wx
HIGHLIGHT_ODD = 1
HIGHLIGHT_EVEN = 2

class ListRowHighlighter:
    """This mixin can be used to add automatic highlighting of alternate rows
    in a list control.

    """

    def __init__(self, color=None, mode=HIGHLIGHT_EVEN):
        """Initialize the highlighter
        @keyword color: Set a custom highlight color (default uses system color)
        @keyword mode: HIGHLIGHT_EVEN (default) or HIGHLIGHT_ODD

        """
        self._color = color
        self._defaultb = wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX)
        self._mode = mode
        self._refresh_timer = wx.Timer(self)
        self.Bind(wx.EVT_LIST_INSERT_ITEM, lambda evt: self._RestartTimer())
        self.Bind(wx.EVT_LIST_DELETE_ITEM, lambda evt: self._RestartTimer())
        self.Bind(wx.EVT_TIMER, lambda evt: self.RefreshRows(), self._refresh_timer)

    def _RestartTimer(self):
        if self._refresh_timer.IsRunning():
            self._refresh_timer.Stop()
        self._refresh_timer.Start(100, oneShot=True)

    def RefreshRows(self):
        """Re-color all the rows"""
        for row in range(self.GetItemCount()):
            if self._defaultb is None:
                self._defaultb = self.GetItemBackgroundColour(row)
            if self._mode & HIGHLIGHT_EVEN:
                dohlight = not row % 2
            else:
                dohlight = row % 2
            if dohlight:
                if self._color is None:
                    if wx.Platform in ('__WXGTK__', '__WXMSW__'):
                        color = wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DLIGHT)
                    else:
                        color = wx.Colour(237, 243, 254)
                else:
                    color = self._color
            else:
                color = self._defaultb
            self.SetItemBackgroundColour(row, color)

        return

    def SetHighlightColor(self, color):
        """Set the color used to highlight the rows. Call L{RefreshRows} after
        this if you wish to update all the rows highlight colors.
        @param color: wx.Colour or None to set default

        """
        self._color = color

    def SetHighlightMode(self, mode):
        """Set the highlighting mode to either HIGHLIGHT_EVEN or to
        HIGHLIGHT_ODD. Call L{RefreshRows} afterwards to update the list
        state.
        @param mode: HIGHLIGHT_* mode value

        """
        self._mode = mode