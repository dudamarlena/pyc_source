# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/SutekhMainWindow.py
# Compiled at: 2019-12-11 16:37:54
"""Main window for Sutekh."""
import logging, datetime, gtk
from sqlobject import SQLObjectNotFound
from sutekh.base.core.BaseAdapters import IAbstractCard
from sutekh.base.core.DBUtility import CARDLIST_UPDATE_DATE, flush_cache, get_metadata_date
from sutekh.base.gui.AppMainWindow import AppMainWindow
from sutekh.base.gui.GuiDataPack import gui_error_handler
from sutekh.base.gui.SutekhDialog import do_complaint
from sutekh.base.gui.UpdateDialog import UpdateDialog
from sutekh.core.SutekhObjectCache import SutekhObjectCache
from sutekh.io.PhysicalCardSetWriter import PhysicalCardSetWriter
from sutekh.io.WwUrls import WW_CARDLIST_DATAPACK
from sutekh.io.DataPack import find_all_data_packs
from sutekh.gui.AboutDialog import SutekhAboutDialog
from sutekh.gui.MainMenu import MainMenu
from sutekh.gui.PluginManager import PluginManager
from sutekh.gui.GuiDBManagement import GuiDBManager
from sutekh.gui import SutekhIcon
from sutekh.gui.GuiIconManager import GuiIconManager
from sutekh.gui.CardTextFrame import CardTextFrame

class SutekhMainWindow(AppMainWindow):
    """Window that has a configurable number of panes."""

    def __init__(self):
        super(SutekhMainWindow, self).__init__()
        self._cPCSWriter = PhysicalCardSetWriter
        self._sResourceName = 'sutekh'
        self.set_size_request(100, 100)
        self.set_default_size(800, 600)
        self._cDBManager = GuiDBManager
        gtk.window_set_default_icon(SutekhIcon.SUTEKH_ICON)
        self.__oSutekhObjectCache = None
        return

    def _verify_database(self):
        """Check that the database is correctly populated"""
        try:
            _oCard = IAbstractCard('Ossian')
        except SQLObjectNotFound:
            logging.warn('Ossian not found in the database')
            iResponse = do_complaint('Database is missing cards. Try import the cardlist now?', gtk.MESSAGE_ERROR, gtk.BUTTONS_YES_NO, False)
            if iResponse == gtk.RESPONSE_YES:
                self.do_refresh_card_list()

        self.__oSutekhObjectCache = SutekhObjectCache()

    def setup(self, oConfig):
        """After database checks are passed, setup what we need to display
           data from the database."""
        oPluginManager = PluginManager()
        oIconManager = GuiIconManager(oConfig.get_icon_path())
        oCardTextPane = CardTextFrame(self, oIconManager)
        self._do_app_setup(oConfig, oCardTextPane, oIconManager, oPluginManager)

    def _create_app_menu(self):
        """Create the main application menu."""
        self._oMenu = MainMenu(self, self._oConfig)

    def update_to_new_db(self):
        """Resync panes against the database.

           Needed because ids aren't kept across re-reading the WW
           cardlist, since card sets with children are always created
           before there children are added.
           """
        flush_cache()
        self.__oSutekhObjectCache = SutekhObjectCache()
        super(SutekhMainWindow, self).update_to_new_db()

    def clear_cache(self):
        """Remove the cached set of objects, for card list reloads, etc."""
        del self.__oSutekhObjectCache

    def show_about_dialog(self, _oWidget):
        """Display the about dialog"""
        oDlg = SutekhAboutDialog()
        oDlg.run()
        oDlg.destroy()

    def show_tutorial(self):
        """Show the HTML Tutorial"""
        self._do_html_dialog('Tutorial.html')

    def show_manual(self):
        """Show the HTML Manual"""
        self._do_html_dialog('Manual.html')

    def check_updated_cardlist(self):
        """Check if an updated cardlist is available"""
        aUrls, aDates, aHashes = find_all_data_packs(WW_CARDLIST_DATAPACK, fErrorHandler=gui_error_handler)
        if not aUrls:
            return
        else:
            oCLDate = datetime.datetime.strptime(aDates[0], '%Y-%m-%d').date()
            oLastDate = get_metadata_date(CARDLIST_UPDATE_DATE)
            if oLastDate is None or oLastDate < oCLDate:
                oDlg = UpdateDialog(['CardList and Rulings'])
                iResponse = oDlg.run()
                oDlg.destroy()
                if iResponse != gtk.RESPONSE_OK:
                    return
                self.do_refresh_from_zip_url(oCLDate, aUrls[0], aHashes[0])
            return