# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/LogViewMenu.py
# Compiled at: 2019-12-11 16:37:48
"""Menu for the card set pane"""
import logging, gtk
from .SutekhMenu import SutekhMenu
from .SutekhFileWidget import ExportDialog

class LogViewMenu(SutekhMenu):
    """Log View Menu.

       Provides options for filtering the log messages on severity,
       and an options to export the current filtered list to a file.
       """

    def __init__(self, oFrame, oWindow):
        super(LogViewMenu, self).__init__(oWindow)
        self._oLogFrame = oFrame
        self._create_actions_menu()

    def _create_actions_menu(self):
        """Create the Actions menu for Card Sets."""
        oMenu = self.create_submenu(self, '_Actions')
        oFilterList = self.create_submenu(oMenu, '_Filter log level')
        self._create_filter_list(oFilterList)
        oMenu.add(gtk.SeparatorMenuItem())
        self.create_menu_item('_Save current view to File', oMenu, self._save_to_file)

    def _create_filter_list(self, oSubMenu):
        """Create list of 'Filter' radio options."""
        oAll = gtk.RadioMenuItem(None, 'Show all log messages')
        oInfo = gtk.RadioMenuItem(oAll, 'Ignore debugging log messages')
        oWarn = gtk.RadioMenuItem(oAll, 'Also Ignore Info messages')
        oError = gtk.RadioMenuItem(oAll, 'Only show Error log messages')
        oAll.connect('activate', self._change_log_level, logging.NOTSET)
        oInfo.connect('activate', self._change_log_level, logging.INFO)
        oWarn.connect('activate', self._change_log_level, logging.WARN)
        oError.connect('activate', self._change_log_level, logging.ERROR)
        oAll.set_active(True)
        oSubMenu.add(oAll)
        oSubMenu.add(oInfo)
        oSubMenu.add(oWarn)
        oSubMenu.add(oError)
        return

    def _save_to_file(self, _oWidget):
        """Popup the Save File dialog."""
        oDlg = ExportDialog('Save logs as', self._oMainWindow)
        oDlg.add_filter_with_pattern('TXT files', ['*.txt'])
        oDlg.run()
        self._oLogFrame.view.save_to_file(oDlg.get_name())

    def _change_log_level(self, _oWidget, iNewLevel):
        """Pass the new log level to the view"""
        self._oLogFrame.set_filter_level(iNewLevel)