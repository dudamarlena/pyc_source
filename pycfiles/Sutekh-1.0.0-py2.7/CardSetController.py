# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/CardSetController.py
# Compiled at: 2019-12-11 16:37:48
"""Controller for the card sets"""
import collections
from sqlobject import SQLObjectNotFound
from .GuiCardSetFunctions import check_ok_to_delete, update_card_set
from .CardSetView import CardSetView
from .MessageBus import MessageBus, CARD_TEXT_MSG
from ..core.DBSignals import send_changed_signal
from ..core.BaseTables import PhysicalCardSet, PhysicalCard, MapPhysicalCardToPhysicalCardSet
from ..core.BaseAdapters import IPhysicalCardSet
from ..core.CardSetUtilities import delete_physical_card_set

class CardSetController(object):
    """Controller class for the Card Sets."""
    _sFilterType = 'PhysicalCard'

    def __init__(self, sName, oMainWindow, oFrame, bStartEditable):
        self._oMainWindow = oMainWindow
        self._aUndoList = collections.deque([], 50)
        self._aRedoList = collections.deque([], 50)
        self._oFrame = oFrame
        self._oView = CardSetView(oMainWindow, self, sName, bStartEditable)
        self.__oPhysCardSet = IPhysicalCardSet(sName)
        self.model.set_controller(self)

    view = property(fget=lambda self: self._oView, doc='Associated View')
    model = property(fget=lambda self: self._oView._oModel, doc="View's Model")
    frame = property(fget=lambda self: self._oFrame, doc='Associated Frame')
    filtertype = property(fget=lambda self: self._sFilterType, doc='Associated Type')

    def cleanup(self):
        """Remove the signal handlers."""
        self.model.cleanup()

    def set_card_text(self, oCard):
        """Set card text to reflect selected card."""
        MessageBus.publish(CARD_TEXT_MSG, 'set_card_text', oCard)

    def inc_card(self, oPhysCard, sCardSetName, bAddUndo=True):
        """Returns the exact PhysicalCard that was successfully added,
           or None if the operation failed."""
        return self.add_card(oPhysCard, sCardSetName, bAddUndo)

    def dec_card(self, oPhysCard, sCardSetName, bAddUndo=True):
        """Returns the specific PhysicalCard that was successfully removed
           (which can differ from the card passed by the user)
           or None is if the operation failed."""
        try:
            if sCardSetName:
                oThePCS = IPhysicalCardSet(sCardSetName)
            else:
                oThePCS = self.__oPhysCardSet
            aPhysCards = [
             oPhysCard]
            if not oPhysCard.printing:
                iCardCount = MapPhysicalCardToPhysicalCardSet.selectBy(physicalCardID=oPhysCard.id, physicalCardSetID=oThePCS.id).count()
                if iCardCount == 0:
                    aPhysCards = list(PhysicalCard.selectBy(abstractCardID=oPhysCard.abstractCard.id))
        except SQLObjectNotFound:
            return

        for oCard in aPhysCards:
            aCandCards = list(MapPhysicalCardToPhysicalCardSet.selectBy(physicalCardID=oCard.id, physicalCardSetID=oThePCS.id))
            if aCandCards:
                MapPhysicalCardToPhysicalCardSet.delete(aCandCards[(-1)].id)
                oThePCS.syncUpdate()
                send_changed_signal(oThePCS, oCard, -1)
                if bAddUndo:
                    if sCardSetName:
                        dOperation = {sCardSetName: [(oCard, 1)]}
                    else:
                        dOperation = {self.view.sSetName: [(oCard, 1)]}
                    self._add_undo_operation(dOperation)
                return oCard

        return

    def add_card(self, oPhysCard, sCardSetName, bAddUndo=True):
        """Returns the exact PhysicalCard that was successfully added,
           or None if the operation failed."""
        try:
            if sCardSetName:
                oThePCS = IPhysicalCardSet(sCardSetName)
            else:
                oThePCS = self.__oPhysCardSet
        except SQLObjectNotFound:
            return

        oThePCS.addPhysicalCard(oPhysCard.id)
        oThePCS.syncUpdate()
        send_changed_signal(oThePCS, oPhysCard, 1)
        if bAddUndo:
            if sCardSetName:
                dOperation = {sCardSetName: [(oPhysCard, -1)]}
            else:
                dOperation = {self.view.sSetName: [(oPhysCard, -1)]}
            self._add_undo_operation(dOperation)
        return oPhysCard

    def edit_properties(self, _oMenuWidget):
        """Run the dialog to update the card set properties"""
        update_card_set(self.__oPhysCardSet, self._oMainWindow)

    def _clear_undo_lists(self):
        """Clear the list of undo / redo operations to avoid
           inconsistencies."""
        self._aUndoList.clear()
        self._aRedoList.clear()

    def _fix_undo_status(self):
        """Fix the state of the undo menu items."""
        if self._aUndoList:
            self._oFrame.menu.set_undo_sensitive(True)
        else:
            self._oFrame.menu.set_undo_sensitive(False)
        if self._aRedoList:
            self._oFrame.menu.set_redo_sensitive(True)
        else:
            self._oFrame.menu.set_redo_sensitive(False)

    def update_to_new_db(self):
        """Update the internal card set to the new DB."""
        try:
            self._clear_undo_lists()
            self._fix_undo_status()
            self.__oPhysCardSet = IPhysicalCardSet(self.view.sSetName)
            self.model.update_to_new_db(self.view.sSetName)
        except SQLObjectNotFound:
            self._oFrame.close_frame()

    def delete_card_set(self):
        """Delete this card set from the database."""
        if check_ok_to_delete(self.__oPhysCardSet):
            self._oMainWindow.config_file.clear_cardset_profile(self.model.cardset_id)
            self._oFrame.close_frame()
            for oFrame in self._oMainWindow.find_cs_pane_by_set_name(self.view.sSetName):
                oFrame.close_frame()

            delete_physical_card_set(self.view.sSetName)
            self._oMainWindow.reload_pcs_list()

    def save_iter_state(self, aIters):
        """Ask the view to save the state for us"""
        dStates = {}
        self.view.save_iter_state(aIters, dStates)
        return dStates

    def restore_iter_state(self, aIters, dStates):
        """Ask the view to restore the state"""
        self.view.restore_iter_state(aIters, dStates)

    def add_paste_data(self, sSource, aCards):
        """Helper function for drag+drop and copy+paste.

           Only works when we're editable.
           """
        aSources = sSource.split(':')
        aUndoCards = []
        if not self.model.bEditable:
            return False
        else:
            if aSources[0] in ('Phys', PhysicalCardSet.sqlmeta.table):
                for iCount, oPhysCard in aCards:
                    if aSources[0] == 'Phys':
                        self.add_card(oPhysCard, None, False)
                        aUndoCards.append((oPhysCard, -1))
                    else:
                        for _iLoop in range(iCount):
                            self.add_card(oPhysCard, None, False)
                            aUndoCards.append((oPhysCard, -1))

                dOperation = {self.view.sSetName: aUndoCards}
                self._add_undo_operation(dOperation)
                return True
            return False

    def change_selected_card_count(self, dSelectedData):
        """Helper function to set the selected cards to the specified number"""
        dOperation = {}
        for oPhysCard in dSelectedData:
            for sCardSetName, (iCardCount, iNewCnt) in dSelectedData[oPhysCard].iteritems():
                aCards = []
                if iNewCnt < iCardCount:
                    for _iAttempt in range(iCardCount - iNewCnt):
                        oCard = self.dec_card(oPhysCard, sCardSetName, False)
                        if oCard:
                            aCards.append((oCard, 1))

                elif iNewCnt > iCardCount:
                    for _iAttempt in range(iNewCnt - iCardCount):
                        oCard = self.inc_card(oPhysCard, sCardSetName, False)
                        aCards.append((oCard, -1))

                dOperation.setdefault(sCardSetName, [])
                dOperation[sCardSetName].extend(aCards)

        self._add_undo_operation(dOperation)

    def _add_undo_operation(self, dOperation):
        """Handle adding an item to the undo list."""
        self._aUndoList.append(dOperation)
        self._aRedoList.clear()
        self._fix_undo_status()

    def undo_edit(self):
        """Undo the last edit operation"""
        if not self._aUndoList:
            return
        dOperation = self._aUndoList.pop()
        for sCardSetName, aCards in dOperation.iteritems():
            for oPhysCard, iCnt in aCards:
                if iCnt < 0:
                    self.dec_card(oPhysCard, sCardSetName, False)
                else:
                    self.add_card(oPhysCard, sCardSetName, False)

        self._aRedoList.append(dOperation)
        self._fix_undo_status()

    def redo_edit(self):
        """Redo the last 'Undone' edit operation"""
        if not self._aRedoList:
            return
        dOperation = self._aRedoList.pop()
        for sCardSetName, aCards in dOperation.iteritems():
            for oPhysCard, iCnt in aCards:
                if iCnt > 0:
                    self.dec_card(oPhysCard, sCardSetName, False)
                else:
                    self.add_card(oPhysCard, sCardSetName, False)

        self._aUndoList.append(dOperation)
        self._fix_undo_status()