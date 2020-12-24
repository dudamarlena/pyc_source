# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/FilteredViewMenu.py
# Compiled at: 2019-12-11 16:37:48
"""Base class for the pane menus"""
import gtk
from .SutekhMenu import SutekhMenu

class FilteredViewMenu(SutekhMenu):
    """Base class for individual FilteredView menus

       This provides handling for enabling and disabling the menus
       ability to receive accelerators on focus changes, expanding
       & collapsing rows, and manging the active filter.
       """

    def __init__(self, oFrame, oWindow, oController):
        super(FilteredViewMenu, self).__init__(oWindow)
        self._oFrame = oFrame
        self.oApply = None
        self._oController = oController
        return

    def cleanup(self):
        """Cleanup hook for menus"""
        pass

    def create_filter_menu(self):
        """Create the Filter Menu."""
        oMenu = self.create_submenu(self, 'F_ilter')
        self.create_menu_item('_Specify Filter', oMenu, self.set_active_filter, '<Ctrl>s')
        self.oApply = self.create_check_menu_item('_Apply Filter', oMenu, self.toggle_apply_filter, False, '<Ctrl>t')
        self.oApply.set_inconsistent(False)

    def create_edit_menu(self):
        """Create the 'Edit' menu, and populate it."""
        oMenu = self.create_submenu(self, '_Edit')
        self.add_edit_menu_actions(oMenu)

    def set_active_filter(self, _oWidget):
        """Set the current filter for the card set."""
        self._oController.view.get_filter(self)

    def toggle_apply_filter(self, oWidget):
        """Toggle the filter applied state."""
        self._oController.view.run_filter(oWidget.active)

    def set_apply_filter(self, bState):
        """Set the applied filter state to bState."""
        self.oApply.set_active(bState)

    def get_apply_filter(self):
        """Get the filter applied state"""
        return self.oApply.active

    def add_common_actions(self, oMenu):
        """Actions common to all card lists"""
        self.create_menu_item('Expand All', oMenu, self.expand_all, '<Ctrl>plus')
        self.create_menu_item('Collapse All', oMenu, self.collapse_all, '<Ctrl>minus')

    def add_edit_menu_actions(self, oMenu):
        """Add the search item to the Edit Menu."""
        self.create_menu_item('_Search', oMenu, self.show_search_dialog, '<Ctrl>f')

    def expand_all(self, _oWidget):
        """Expand all the rows in the card set."""
        self._oController.view.expand_all()

    def collapse_all(self, _oWidget):
        """Collapse all the rows in the card set."""
        self._oController.view.collapse_all()

    def show_search_dialog(self, _oWidget):
        """Show the search dialog"""
        self._oController.view.emit('start-interactive-search')

    def _create_profile_menu(self, oParentMenu, sTitle, sType, fCallback, sProfile):
        """Create a radio group sub-menu for selecting a profile."""
        oMenu = self.create_submenu(oParentMenu, sTitle)
        oConfig = self._oMainWindow.config_file
        oGroup = gtk.RadioMenuItem(None, oConfig.get_profile_option(sType, None, 'name'))
        oGroup.connect('toggled', fCallback, None)
        oMenu.append(oGroup)
        self._update_profile_group(oMenu, sType, fCallback, sProfile)
        return oMenu

    def _update_profile_group(self, oMenu, sType, fCallback, sProfile):
        """Update the profile selection menu"""
        oConfig = self._oMainWindow.config_file
        oGroup = oMenu.get_children()[0]
        aProfiles = [ (sKey, oConfig.get_profile_option(sType, sKey, 'name')) for sKey in oConfig.profiles(sType)
                    ]
        aProfiles.sort(key=lambda tProfile: tProfile[1])
        if sProfile is None or sProfile == 'Default':
            oGroup.set_active(True)
        for oRadio in oGroup.get_group():
            if oRadio is not oGroup:
                oRadio.set_group(None)
                oMenu.remove(oRadio)

        for sKey, sName in aProfiles:
            oRadio = gtk.RadioMenuItem(oGroup, sName)
            oRadio.connect('toggled', fCallback, sKey)
            if sKey == sProfile:
                oRadio.set_active(True)
            oMenu.append(oRadio)
            oRadio.show()

        return


class CardListMenu(FilteredViewMenu):
    """Base class for Card List Menus

       Adds some common methods for dealing with the card lists -
       copying selections, etc.
       """

    def copy_selection(self, _oWidget):
        """Copy the current selection to the application clipboard."""
        self._oController.view.copy_selection()

    def create_analyze_menu(self):
        """Create the Analyze Menu, to be filled in by plugins"""
        self.create_submenu(self, 'Analy_ze')