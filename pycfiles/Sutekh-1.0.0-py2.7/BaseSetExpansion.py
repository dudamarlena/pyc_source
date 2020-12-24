# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/plugins/BaseSetExpansion.py
# Compiled at: 2019-12-11 16:37:39
"""Force all cards which can only belong to 1 expansion to that expansion"""
import gtk
from ...core.BaseTables import PhysicalCardSet, MapPhysicalCardToPhysicalCardSet
from ...core.BaseAdapters import IExpansion, IPhysicalCard, IAbstractCard, IPrinting
from ...core.DBSignals import send_changed_signal
from ..BasePluginManager import BasePlugin
from ..SutekhDialog import SutekhDialog, do_complaint_error
from ..ScrolledList import ScrolledList

class BaseSetExpansion(BasePlugin):
    """Set al the selected cards in the card list to a single expansion

       Find the common subset of expansions for the selected list, and allow
       the user to choose which expansion to set all the cards too.
       """
    dTableVersions = {PhysicalCardSet: (5, 6, 7)}
    aModelsSupported = (
     PhysicalCardSet,)

    def get_menu_item(self):
        """Return a gtk.MenuItem to activate this plugin."""
        oMenuItem = gtk.MenuItem('Set selected cards to a single expansion')
        oMenuItem.connect('activate', self.activate)
        return ('Actions', oMenuItem)

    def activate(self, _oWidget):
        """Handle menu activation"""
        self.create_dialog()

    def create_dialog(self):
        """Find the common subset of the selected cards, and prompt the user
           for the expansion.
           """
        dSelected = self.view.process_selection()
        aAbsCards = set(self._get_selected_abs_cards())
        if not aAbsCards:
            do_complaint_error('Need to select some cards for this plugin')
            return
        else:
            aExpansions = self.find_common_expansions(aAbsCards)
            oDialog = SutekhDialog('Select expansion', self.parent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (
             gtk.STOCK_OK, gtk.RESPONSE_OK,
             gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
            oExpList = ScrolledList('Possible Expansions')
            oDialog.vbox.pack_start(oExpList)
            oExpList.set_size_request(150, 300)
            oExpList.fill_list(sorted(aExpansions))
            oExpList.set_select_single()
            if oDialog.run() == gtk.RESPONSE_OK:
                aExpNames = oExpList.get_selection()
                if not aExpNames:
                    sExpName = None
                    do_complaint_error('No Expansion selected')
                else:
                    sExpName = aExpNames[0]
                    if sExpName == self.model.sUnknownExpansion:
                        oPrinting = None
                    else:
                        oExpansion = IExpansion(sExpName)
                        oPrinting = IPrinting((oExpansion, None))
                    self.do_set_printing(dSelected, oPrinting)
            oDialog.destroy()
            return

    def do_set_printing(self, dSelected, oPrinting):
        """Iterate over the cards, setting the correct expansion"""
        oCS = self._get_card_set()
        for oCard in self.model.get_card_iterator(self.model.get_current_filter()):
            oAbsCard = IAbstractCard(oCard)
            if oAbsCard.id in dSelected:
                oPhysCard = IPhysicalCard(oCard)
                if oPhysCard.printing is oPrinting:
                    continue
                if oPhysCard.id in dSelected[oAbsCard.id]:
                    oNewCard = IPhysicalCard((oAbsCard, oPrinting))
                    MapPhysicalCardToPhysicalCardSet.delete(oCard.id)
                    oCS.addPhysicalCard(oNewCard.id)
                    oCS.syncUpdate()
                    send_changed_signal(oCS, oPhysCard, -1)
                    send_changed_signal(oCS, oNewCard, +1)

        self.view.reload_keep_expanded()

    def find_common_expansions(self, aCardList):
        """Find the common possible set of expansions for the given list
           of abstract cards."""
        oFirstCard = aCardList.pop()
        aCandExpansions = set([ x.expansion.name for x in oFirstCard.rarity ])
        for oCard in aCardList:
            aThisExpansions = set([ x.expansion.name for x in oCard.rarity ])
            aCandExpansions = aThisExpansions.intersection(aCandExpansions)

        aCandExpansions.add(self.model.sUnknownExpansion)
        return aCandExpansions