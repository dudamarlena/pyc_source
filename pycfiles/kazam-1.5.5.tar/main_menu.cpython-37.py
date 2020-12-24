# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../kazam/frontend/main_menu.py
# Compiled at: 2019-08-17 21:55:54
# Size of source mod 2**32: 2834 bytes
from gettext import gettext as _
from gi.repository import Gtk, GObject
MENUBAR = "\n    <ui>\n        <menubar name='MenuBar'>\n            <menu action='FileMenu'>\n                <menuitem action='FilePreferences' />\n                <menuitem action='FileQuit' />\n            </menu>\n            <menu action='HelpMenu'>\n                <menuitem action='HelpAbout' />\n            </menu>\n        </menubar>\n</ui>\n"

class MainMenu(GObject.GObject):
    __gsignals__ = {'file-preferences':(
      GObject.SIGNAL_RUN_LAST,
      None,
      ()), 
     'file-quit':(
      GObject.SIGNAL_RUN_LAST,
      None,
      ()), 
     'help-about':(
      GObject.SIGNAL_RUN_LAST,
      None,
      ())}

    def __init__(self):
        GObject.GObject.__init__(self)
        self.action_group = Gtk.ActionGroup('kazam_actions')
        self.action_group.add_actions([
         (
          'FileMenu', None, _('File')),
         (
          'FileQuit', Gtk.STOCK_QUIT, _('Quit'), None, _('Quit Kazam'),
          self.cb_file_quit),
         (
          'FilePreferences', Gtk.STOCK_PREFERENCES, _('Preferences'), None, _('Open preferences'),
          self.cb_file_preferences),
         (
          'HelpMenu', None, _('Help')),
         (
          'HelpAbout', None, _('About'), None, _('About Kazam'),
          self.cb_help_about)])
        self.uimanager = Gtk.UIManager()
        self.uimanager.add_ui_from_string(MENUBAR)
        self.uimanager.insert_action_group(self.action_group)
        self.menubar = self.uimanager.get_widget('/MenuBar')

    def cb_file_quit(self, action):
        self.emit('file-quit')

    def cb_file_preferences(self, action):
        self.emit('file-preferences')

    def cb_help_about(self, action):
        self.emit('help-about')