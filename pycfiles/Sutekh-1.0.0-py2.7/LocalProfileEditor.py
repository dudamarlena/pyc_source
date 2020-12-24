# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/LocalProfileEditor.py
# Compiled at: 2019-12-11 16:37:48
"""This handles editing the local profile editor, (for temporary options)"""
import gtk
from .SutekhDialog import SutekhDialog
from .AutoScrolledWindow import AutoScrolledWindow
from .PreferenceTable import PreferenceTable
from .BaseConfigFile import FRAME

class LocalProfileEditor(SutekhDialog):
    """Dialog which allows the user to set temporary option profiles.
       """
    RESPONSE_CLOSE = 1
    RESPONSE_CANCEL = 2

    def __init__(self, oParent, oConfig, sFrame, sCardSet):
        super(LocalProfileEditor, self).__init__('Edit Local Profile', oParent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
        self.__oParent = oParent
        self.__oConfig = oConfig
        self.__sFrame = sFrame
        self.__sCardSet = sCardSet
        self.__dUnsavedChanges = None
        aOptions = []
        for sKey in self.__oConfig.profile_options(FRAME):
            if sKey == 'name':
                continue
            aOptions.append((sKey, self.__oConfig.get_option_spec(FRAME, sKey),
             True))

        self.__oOptionsTable = PreferenceTable(aOptions, oConfig.get_validator())
        self.vbox.pack_start(AutoScrolledWindow(self.__oOptionsTable, bUseViewport=True))
        self.set_default_size(600, 550)
        self.connect('response', self._button_response)
        self.add_button('Cancel', self.RESPONSE_CANCEL)
        self.add_button('Close', self.RESPONSE_CLOSE)
        self.show_all()
        self._repopulate_options()
        return

    def _button_response(self, _oWidget, iResponse):
        """Handle dialog response"""
        if iResponse != self.RESPONSE_CLOSE:
            self.destroy()
            return
        self._store_active_profile()
        if self._check_unsaved_changes():
            self._save_unsaved_changes()
            self.destroy()
        else:
            self.destroy()
            oDlg = LocalProfileEditor(self.__oParent, self.__oConfig, self.__sFrame, self.__sCardSet)
            oDlg.run()

    def _repopulate_options(self):
        """Refresh the contents of the options box."""
        dNewValues = {}
        dInherited = {}
        sFrame, sCardSet = self.__sFrame, self.__sCardSet
        for sKey in self.__oConfig.profile_options(FRAME):
            dNewValues[sKey] = self.__oConfig.get_local_frame_option(sFrame, sKey)
            dInherited[sKey] = self.__oConfig.get_deck_option(sFrame, sCardSet, sKey, bUseLocal=False)

        self.__oOptionsTable.update_values(dNewValues, {}, {}, dInherited)

    def _check_unsaved_changes(self):
        """Check that none of the changes make are bad.

        Return True if the changes are safe for saving, False otherwise.
        """
        return True

    def _save_unsaved_changes(self):
        """Save all the unsaved changes."""
        sFrame = self.__sFrame
        for sKey, sValue in self.__dUnsavedChanges.items():
            self.__oConfig.set_local_frame_option(sFrame, sKey, sValue)

    def _store_active_profile(self):
        """Store the unsaved local profile changes."""
        self.__dUnsavedChanges = self.__oOptionsTable.get_values()