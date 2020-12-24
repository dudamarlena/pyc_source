# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/FrameProfileEditor.py
# Compiled at: 2019-12-11 16:37:48
"""Dialog for editing profiles.

The type of profile to edit (cardset, cardset list, etc.) is a parameter
passed in when the dialog is created.
"""
import gtk, gobject
from .SutekhDialog import SutekhDialog
from .AutoScrolledWindow import AutoScrolledWindow
from .PreferenceTable import PreferenceTable

class FrameProfileEditor(SutekhDialog):
    """Dialog which allows the user to edit profiles of the specified type.
       """
    RESPONSE_SAVE_AND_CLOSE = 1
    RESPONSE_CANCEL = 2

    def __init__(self, oParent, oConfig, sType):
        super(FrameProfileEditor, self).__init__('Edit Per-Deck Profiles', oParent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
        self.__oParent = oParent
        self.__oConfig = oConfig
        self._sType = sType
        self.__dUnsavedChanges = {}
        self.__sActiveProfile = None
        oModel = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
        oCell = gtk.CellRendererText()
        self.__oSelectorCombo = gtk.ComboBox(oModel)
        self.__oSelectorCombo.pack_start(oCell, True)
        self.__oSelectorCombo.add_attribute(oCell, 'text', 1)
        self.__oSelectorCombo.set_wrap_width(1)
        self.__oSelectorCombo.connect('changed', self._selector_changed)
        self.__oSelectorCombo.connect('notify::popup-shown', self._selector_opened)
        self.vbox.pack_start(self.__oSelectorCombo, expand=False)
        aOptions = []
        for sKey in self.__oConfig.profile_options(self._sType):
            bInherit = sKey != 'name'
            aOptions.append((
             sKey, self.__oConfig.get_option_spec(self._sType, sKey),
             bInherit))

        self.__oOptionsTable = PreferenceTable(aOptions, oConfig.get_validator())
        self.vbox.pack_start(AutoScrolledWindow(self.__oOptionsTable, bUseViewport=True))
        self.set_default_size(600, 550)
        self.connect('response', self._button_response)
        self.add_button('Cancel', self.RESPONSE_CANCEL)
        self.add_button('Save and Close', self.RESPONSE_SAVE_AND_CLOSE)
        self._repopulate_selector()
        self.show_all()
        self.__oSelectorCombo.set_active(0)
        return

    def set_selected_profile(self, sProfile):
        """Set the selected profile for editing to given one"""
        oModel = self.__oSelectorCombo.get_model()
        oIter = oModel.get_iter_root()
        while oIter:
            if oModel.get_value(oIter, 0) == sProfile:
                self.__oSelectorCombo.set_active_iter(oIter)
                return
            oIter = oModel.iter_next(oIter)

    def _button_response(self, _oWidget, iResponse):
        """Handle dialog response"""
        if iResponse != self.RESPONSE_SAVE_AND_CLOSE:
            self.destroy()
            return
        self._store_active_profile()
        if self._check_unsaved_changes():
            self._save_unsaved_changes()
            self.destroy()
        else:
            self.destroy()
            oDlg = FrameProfileEditor(self.__oParent, self.__oConfig, self._sType)
            oDlg.run()

    def _all_profile_keys(self):
        """Return a set of all profile keys (including unsaved profiles)."""
        aProfiles = set(self.__oConfig.profiles(self._sType))
        aProfiles.add('defaults')
        aProfiles.update(self.__dUnsavedChanges)
        return aProfiles

    def _profile_options(self, sProfile):
        """Return a dict of option values from a (possibly unsaved) profile."""
        if sProfile in self.__dUnsavedChanges:
            dValues = self.__dUnsavedChanges[sProfile]
        elif sProfile in self.__oConfig.profiles(self._sType) or sProfile == 'defaults':
            dValues = {}
            if sProfile == 'defaults':
                sProfile = None
            for sKey in self.__oConfig.profile_options(self._sType):
                dValues[sKey] = self.__oConfig.get_profile_option(self._sType, sProfile, sKey)

        else:
            dValues = dict.fromkeys(self.__oConfig.profile_options(self._sType), None)
            dValues['name'] = 'New Profile (%s)' % sProfile
        return dValues

    def _next_key(self):
        """Return the next unused profile name."""
        iProfile = 0
        aProfiles = self._all_profile_keys()
        while True:
            sProfile = 'profile_%d' % iProfile
            if sProfile not in aProfiles:
                break
            iProfile += 1

        return sProfile

    def _repopulate_selector(self):
        """Refresh the contents of the selector box."""
        oModel = self.__oSelectorCombo.get_model()
        oModel.clear()
        aProfiles = self._all_profile_keys()
        aProfiles.discard('defaults')
        for sProfile in ['defaults'] + list(sorted(aProfiles)):
            dValues = self._profile_options(sProfile)
            _oIter = oModel.append((sProfile, dValues['name']))

        oModel.append((self._next_key(), 'New Profile ...'))

    def _selector_opened(self, _oSelectorCombo, _oPopupShown):
        """Callback for when selector combo is popped up"""
        if self.__oSelectorCombo.props.popup_shown:
            self._store_active_profile()
            self._repopulate_selector()
        elif self.__oSelectorCombo.get_active_iter() is None:
            self._reset_active_profile()
        return

    def _selector_changed(self, oSelectorCombo):
        """Callback for changes to selector combo."""
        oModel = oSelectorCombo.get_model()
        oActiveIter = oSelectorCombo.get_active_iter()
        if oActiveIter is None:
            return
        else:
            sActiveProfile = oModel.get_value(oActiveIter, 0)
            self._repopulate_options(sActiveProfile)
            return

    def _store_active_profile(self):
        """Add the active profile to the unsaved changes dict."""
        if self.__sActiveProfile is not None:
            self.__dUnsavedChanges[self.__sActiveProfile] = self.__oOptionsTable.get_values()
        return

    def _reset_active_profile(self):
        """Set the selector combo back to the current active profile."""
        if self.__sActiveProfile is None:
            return
        else:

            def set_func(oModel, _oPath, oIter):
                """Helper function used in foreach loop. Sets the correct
               iter active."""
                if oModel.get_value(oIter, 0) == self.__sActiveProfile:
                    self.__oSelectorCombo.set_active_iter(oIter)
                    return True

            self.__oSelectorCombo.get_model().foreach(set_func)
            return

    def _repopulate_options(self, sActiveProfile):
        """Refresh the contents of the options box."""
        if sActiveProfile == self.__sActiveProfile:
            return
        else:
            self._store_active_profile()
            self.__sActiveProfile = None
            dNewValues = self._profile_options(sActiveProfile)
            dInheritedValues = self._profile_options('defaults')
            if sActiveProfile == 'defaults':
                dInherit = dict.fromkeys(dNewValues.keys(), False)
                dEdit = {'name': False}
            else:
                dInherit = {'name': False}
                dEdit = {}
            self.__dUnsavedChanges[sActiveProfile] = dNewValues
            self.__oOptionsTable.update_values(dNewValues, dInherit, dEdit, dInheritedValues)
            self.__sActiveProfile = sActiveProfile
            return

    def _check_unsaved_changes(self):
        """Check that none of the changes make are bad.

        Return True if the changes are safe for saving, False otherwise.
        """
        return True

    def _save_unsaved_changes(self):
        """Save all the unsaved changes."""
        for sProfile, dValues in self.__dUnsavedChanges.items():
            if sProfile == 'defaults':
                sProfile = None
            for sKey, sValue in dValues.items():
                self.__oConfig.set_profile_option(self._sType, sProfile, sKey, sValue)

        return