# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/GuiIconManager.py
# Compiled at: 2019-12-11 16:37:54
"""GTK gui icon manager."""
import os, gtk
from sutekh.base.Utility import prefs_dir, ensure_dir_exists
from sutekh.base.gui.SutekhDialog import do_complaint
from sutekh.base.gui.CachedIconManager import CachedIconManager
from sutekh.io.IconManager import IconManager
from sutekh.SutekhInfo import SutekhInfo

class GuiIconManager(CachedIconManager, IconManager):
    """Gui Manager for the VTES Icons.

       Also provides gui interface for setup
       """

    def __init__(self, sPath):
        if not sPath:
            sPath = os.path.join(prefs_dir(SutekhInfo.NAME), 'icons')
        super(GuiIconManager, self).__init__(sPath)

    def setup(self):
        """Prompt the user to download the icons if the icon directory
           doesn't exist"""
        if os.path.lexists(self._sPrefsDir):
            if os.path.lexists('%s/clans' % self._sPrefsDir):
                return
            ensure_dir_exists('%s/clans' % self._sPrefsDir)
            if os.path.exists('%s/IconClanAbo.gif' % self._sPrefsDir):
                iResponse = do_complaint("Sutekh has switched to using the icons from the V:EKN site.\nIcons won't work until you re-download them.\n\nDownload icons?", gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO, False)
            else:
                return
        else:
            ensure_dir_exists(self._sPrefsDir)
            ensure_dir_exists('%s/clans' % self._sPrefsDir)
            iResponse = do_complaint('Sutekh can download icons for the cards from the V:EKN site\nThese icons will be stored in %s\n\nDownload icons?' % self._sPrefsDir, gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO, False)
        if iResponse == gtk.RESPONSE_YES:
            self.download_with_progress()
        else:
            do_complaint('Icon download skipped.\nYou can choose to download the icons from the File menu.\nYou will not be prompted again unless you delete %s' % self._sPrefsDir, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, False)