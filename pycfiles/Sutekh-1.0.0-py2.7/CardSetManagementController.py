# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/CardSetManagementController.py
# Compiled at: 2019-12-11 16:37:48
"""Controller class the card set list."""
from sqlobject import SQLObjectNotFound
from ..core.BaseTables import PhysicalCardSet
from ..core.BaseAdapters import IPhysicalCardSet
from ..core.CardSetUtilities import delete_physical_card_set
from .CardSetManagementView import CardSetManagementView
from .GuiCardSetFunctions import create_card_set, update_card_set, check_ok_to_delete, break_existing_loops

class CardSetManagementController(object):
    """Controller object for the card set list."""
    _sFilterType = 'PhysicalCardSet'

    def __init__(self, oMainWindow, oFrame):
        self._oMainWindow = oMainWindow
        self._oFrame = oFrame
        break_existing_loops()
        self._oView = CardSetManagementView(self, oMainWindow)
        self._oModel = self._oView.get_model()

    view = property(fget=lambda self: self._oView, doc='Associated View')
    model = property(fget=lambda self: self._oModel, doc="View's Model")
    frame = property(fget=lambda self: self._oFrame, doc='Associated Frame')
    filtertype = property(fget=lambda self: self._sFilterType, doc='Associated Type')

    def create_new_card_set(self, _oWidget):
        """Create a new card set"""
        sName = create_card_set(self._oMainWindow)
        if sName:
            self._oMainWindow.add_new_physical_card_set(sName, True)

    def edit_card_set_properties(self, _oWidget):
        """Create a new card set"""
        sSetName = self._oView.get_selected_card_set()
        if not sSetName:
            return
        oCardSet = IPhysicalCardSet(sSetName)
        update_card_set(oCardSet, self._oMainWindow)

    def delete_card_set(self, _oWidget):
        """Delete the selected card set."""
        sSetName = self._oView.get_selected_card_set()
        if not sSetName:
            return
        try:
            oCS = PhysicalCardSet.byName(sSetName)
        except SQLObjectNotFound:
            return

        if check_ok_to_delete(oCS):
            for oFrame in self._oMainWindow.find_cs_pane_by_set_name(sSetName):
                oFrame.close_frame()

            self._oMainWindow.config_file.clear_cardset_profile('cs%d' % oCS.id)
            delete_physical_card_set(sSetName)
            self.view.reload_keep_expanded(False)

    def toggle_in_use_flag(self, _oMenuWidget):
        """Toggle the in-use status of the card set"""
        sSetName = self._oView.get_selected_card_set()
        if not sSetName:
            return
        try:
            oCS = PhysicalCardSet.byName(sSetName)
        except SQLObjectNotFound:
            return

        oCS.inuse = not oCS.inuse
        oCS.syncUpdate()
        self.view.reload_keep_expanded(True)