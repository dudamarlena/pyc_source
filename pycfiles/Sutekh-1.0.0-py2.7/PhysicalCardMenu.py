# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/PhysicalCardMenu.py
# Compiled at: 2019-12-11 16:37:48
"""Menu for the Physical card collection."""
import gtk
from .FilteredViewMenu import CardListMenu
from .FrameProfileEditor import FrameProfileEditor
from .BaseConfigFile import FULL_CARDLIST
from .MessageBus import MessageBus, CONFIG_MSG

class PhysicalCardMenu(CardListMenu):
    """Menu for the Physical card collection.

       Enables actions specific to the physical card collection (export to
       file, etc), filtering and plugins.
       """

    def __init__(self, oFrame, oController, oWindow):
        super(PhysicalCardMenu, self).__init__(oFrame, oWindow, oController)
        self.__create_physical_cl_menu()
        self.create_edit_menu()
        self.create_filter_menu()
        self.create_analyze_menu()
        self.add_plugins_to_menus(self._oFrame)
        self.sort_menu(self._dMenus['Analyze'])
        MessageBus.subscribe(CONFIG_MSG, 'remove_profile', self.remove_profile)
        MessageBus.subscribe(CONFIG_MSG, 'profile_option_changed', self.profile_option_changed)

    def __create_physical_cl_menu(self):
        """Create the Actions menu for the card list."""
        oMenu = self.create_submenu(self, '_Actions')
        self.create_check_menu_item('Show Card Expansions', oMenu, self._oController.toggle_expansion, True)
        self.create_check_menu_item('Show icons for the grouping', oMenu, self._oController.toggle_icons, True)
        oMenu.add(gtk.SeparatorMenuItem())
        self.add_common_actions(oMenu)

    def create_edit_menu(self):
        """Create the edit menu and populate it"""
        oMenu = self.create_submenu(self, '_Edit')
        self.create_menu_item('Copy selection', oMenu, self.copy_selection, '<Ctrl>c')
        self.create_menu_item('Edit _Profiles', oMenu, self._edit_profiles)
        sProfile = self._oMainWindow.config_file.get_profile(FULL_CARDLIST, FULL_CARDLIST)
        self._oCardlistProfileMenu = self._create_profile_menu(oMenu, 'Cardlist Profile', FULL_CARDLIST, self._select_cardlist_profile, sProfile)
        self.add_edit_menu_actions(oMenu)

    def cleanup(self):
        """Remove the menu listener"""
        MessageBus.unsubscribe(CONFIG_MSG, 'remove_profile', self.remove_profile)
        MessageBus.unsubscribe(CONFIG_MSG, 'profile_option_changed', self.profile_option_changed)

    def _edit_profiles(self, _oWidget):
        """Open an options profiles editing dialog."""
        oDlg = FrameProfileEditor(self._oMainWindow, self._oMainWindow.config_file, FULL_CARDLIST)
        sCurProfile = self._oMainWindow.config_file.get_profile(FULL_CARDLIST, FULL_CARDLIST)
        oDlg.set_selected_profile(sCurProfile)
        oDlg.run()
        self._fix_profile_menu()

    def _fix_profile_menu(self):
        """Set the profile menu correctly"""
        sProfile = self._oMainWindow.config_file.get_profile(FULL_CARDLIST, FULL_CARDLIST)
        self._update_profile_group(self._oCardlistProfileMenu, FULL_CARDLIST, self._select_cardlist_profile, sProfile)

    def _select_cardlist_profile(self, oRadio, sProfileKey):
        """Callback to change the profile of the current card set."""
        if oRadio.get_active():
            oConfig = self._oMainWindow.config_file
            oConfig.set_profile(FULL_CARDLIST, FULL_CARDLIST, sProfileKey)

    def remove_profile(self, sType, _sProfile):
        """A profile has been removed"""
        if sType == FULL_CARDLIST:
            self._fix_profile_menu()

    def profile_option_changed(self, sType, _sProfile, sKey):
        """Update menu if profiles are renamed."""
        if sType == FULL_CARDLIST and sKey == 'name':
            self._fix_profile_menu()