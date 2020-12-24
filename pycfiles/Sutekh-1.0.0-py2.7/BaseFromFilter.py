# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/plugins/BaseFromFilter.py
# Compiled at: 2019-12-11 16:37:39
"""Converts a filter into a card set"""
import gtk
from ...core.BaseTables import PhysicalCardSet, PhysicalCard
from ...core.BaseAdapters import IPhysicalCard, IPhysicalCardSet
from ..BasePluginManager import BasePlugin
from ..GuiCardSetFunctions import create_card_set

class BaseFromFilter(BasePlugin):
    """Converts a filter into a Card Set."""
    dTableVersions = {PhysicalCardSet: (4, 5, 6, 7)}
    aModelsSupported = (
     PhysicalCardSet, PhysicalCard)
    sMenuName = 'Card Set From Filter'
    sHelpCategory = 'card_list:filter'
    sHelpText = 'Create a new card set containing the results\n                   of the current filter. The new card set will\n                   be opened automatically and will be set editable.'

    def get_menu_item(self):
        """Register on the 'Filter' Menu"""
        oGenPCS = gtk.MenuItem('Card Set From Filter')
        oGenPCS.connect('activate', self.activate)
        return ('Filter', oGenPCS)

    def activate(self, _oWidget):
        """Create the dialog.

           Prompt the user for Card Set Properties, and so forth.
           """
        sCSName = create_card_set(self.parent)
        if sCSName:
            oCardSet = self.make_cs_from_filter(sCSName)
            if oCardSet:
                self._open_cs(sCSName, True)

    def make_cs_from_filter(self, sCSName):
        """Create the actual PCS."""
        oCS = IPhysicalCardSet(sCSName)
        aCards = [ IPhysicalCard(x) for x in self.model.get_card_iterator(self.model.get_current_filter())
                 ]
        self._commit_cards(oCS, aCards)
        return oCS