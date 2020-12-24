# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/CachedIconManager.py
# Compiled at: 2019-12-11 16:37:48
"""Icon manager which returns gtk pixmaps for the icons and caches lookups."""
import os, gtk, gobject
from ..io.BaseIconManager import BaseIconManager
from .ProgressDialog import ProgressDialog, SutekhCountLogHandler

def _crop_alpha(oPixbuf):
    """Crop the transparent padding from a pixbuf.

       Needed to reduce scaling issues with the clan icons.
       """

    def _check_margins(iVal, iMax, iMin):
        """Check if the margins need to be updated"""
        if iVal < iMin:
            iMin = iVal
        if iVal > iMax:
            iMax = iVal
        return (
         iMax, iMin)

    iRowLength = oPixbuf.get_width() * 4
    iMaxX, iMaxY = (-1, -1)
    iMinX, iMinY = (1000, 1000)
    iXPos, iYPos = (0, 0)
    for cPixel in oPixbuf.get_pixels():
        if iXPos % 4 == 3:
            if ord(cPixel) == 255:
                iMaxX, iMinX = _check_margins(iXPos // 4, iMaxX, iMinX)
                iMaxY, iMinY = _check_margins(iYPos, iMaxY, iMinY)
        iXPos += 1
        if iXPos == iRowLength:
            iYPos += 1
            iXPos = 0

    if iMinX >= iMaxX or iMinY >= iMaxY:
        return oPixbuf
    return oPixbuf.subpixbuf(iMinX + 1, iMinY + 1, iMaxX - iMinX, iMaxY - iMinY)


class CachedIconManager(BaseIconManager):
    """Managed icons for the gui application.

       Subclass BaseIconManager to return gtk pixbufs, not filenames.
       Also provides gui interface for downloading icons.
       """

    def __init__(self, sPath):
        self._dIconCache = {}
        super(CachedIconManager, self).__init__(sPath)

    def _get_icon(self, sFileName, iSize=12):
        """get the cached icon, or load it if needed."""
        if not sFileName:
            return
        else:
            if sFileName in self._dIconCache:
                return self._dIconCache[sFileName]
            try:
                sFullFilename = os.path.join(self._sPrefsDir, sFileName)
                oPixbuf = gtk.gdk.pixbuf_new_from_file(sFullFilename)
                oPixbuf = _crop_alpha(oPixbuf)
                iHeight = iSize
                iWidth = iSize
                iPixHeight = oPixbuf.get_height()
                iPixWidth = oPixbuf.get_width()
                fAspect = iPixHeight / float(iPixWidth)
                if iPixWidth > iPixHeight:
                    iHeight = int(fAspect * iSize)
                elif iPixHeight > iPixWidth:
                    iWidth = int(iSize / fAspect)
                oPixbuf = oPixbuf.scale_simple(iWidth, iHeight, gtk.gdk.INTERP_TILES)
            except gobject.GError:
                oPixbuf = None

            self._dIconCache[sFileName] = oPixbuf
            return oPixbuf

    def setup(self):
        """Prompt the user to download the icons if the icon directory
           doesn't exist"""
        raise NotImplementedError

    def download_with_progress(self):
        """Wrap download_icons in a progress dialog"""
        self._dIconCache = {}
        oLogHandler = SutekhCountLogHandler()
        oProgressDialog = ProgressDialog()
        oProgressDialog.set_description('Downloading icons')
        oLogHandler.set_dialog(oProgressDialog)
        oProgressDialog.show()
        oLogHandler.set_total(self.get_icon_total())
        self.download_icons(oLogHandler)
        oProgressDialog.destroy()