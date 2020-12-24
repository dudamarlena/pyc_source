# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/plugins/BaseExtraCardViewColumns.py
# Compiled at: 2019-12-11 16:37:39
"""Display extra columns in the tree view"""
from sqlobject import SQLObjectNotFound
from ...core.BaseTables import PhysicalCard, PhysicalCardSet
from ..CellRendererIcons import SHOW_TEXT_ONLY
from .BaseExtraColumns import BaseExtraColumns

class BaseExtraCardViewColumns(BaseExtraColumns):
    """Add extra columns to the card list view.

       This handles the very generic cases
       """
    POS_COLUMN_OFFSET = 3
    COLUMNS = {'Card Type': (100, '_render_card_type', '_get_data_card_type'), 
       'Expansions': (600, '_render_expansions', '_get_data_expansions'), 
       'Card Text': (100, '_render_card_text', '_get_data_card_text')}
    dTableVersions = {}
    aModelsSupported = (
     PhysicalCardSet, PhysicalCard)
    dPerPaneConfig = {}
    dCardListConfig = dPerPaneConfig

    @classmethod
    def update_config(cls):
        """Fix the config to use the right keys."""
        cls.fix_config(cls.dPerPaneConfig)
        cls.dCardListConfig = cls.dPerPaneConfig

    def _get_iter_data(self, oIter):
        """For the given iterator, get the associated abstract card"""
        if self.model.iter_depth(oIter) == 1:
            try:
                oAbsCard = self.model.get_abstract_card_from_iter(oIter)
                return oAbsCard
            except SQLObjectNotFound:
                return

        else:
            return
        return

    def _get_data_card_type(self, oCard, bGetIcons=True):
        """Return the card type"""
        if oCard is not None:
            aTypes = [ x.name for x in oCard.cardtype ]
            aTypes.sort()
            aIcons = []
            if bGetIcons:
                dIcons = self.icon_manager.get_icon_list(oCard.cardtype)
                if dIcons:
                    aIcons = [ dIcons[x] for x in aTypes ]
                else:
                    aIcons = [
                     None] * len(aTypes)
            return (
             (' /|').join(aTypes).split('|'), aIcons)
        else:
            return ([], [])

    def _render_card_type(self, _oColumn, oCell, _oModel, oIter):
        """display the card type(s)"""
        oCard = self._get_iter_data(oIter)
        aText, aIcons = self._get_data_card_type(oCard, True)
        oCell.set_data(aText, aIcons, self._iShowMode)

    def _get_data_expansions(self, oCard, bGetIcons=True):
        """get expansion info"""
        if oCard is not None:
            aExp = [ oP.expansion.shortname + '(' + oP.rarity.name + ')' for oP in oCard.rarity ]
            aExp.sort()
            aIcons = []
            if bGetIcons:
                aIcons = [
                 None] * len(aExp)
            return (aExp, aIcons)
        else:
            return ([], [])

    def _render_expansions(self, _oColumn, oCell, _oModel, oIter):
        """Display expansion info"""
        oCard = self._get_iter_data(oIter)
        aText, aIcons = self._get_data_expansions(oCard)
        oCell.set_data(aText, aIcons, self._iShowMode)

    def _get_data_card_text(self, oCard, bGetIcons=True):
        """Get the card's card text."""
        if oCard is not None:
            aTexts = [
             oCard.text.replace('\n', ' ')]
            aIcons = []
            if bGetIcons:
                aIcons = [
                 None] * len(aTexts)
            return (aTexts, aIcons)
        else:
            return ([], [])

    def _render_card_text(self, _oColumn, oCell, _oModel, oIter):
        """Display card text in the column"""
        oCard = self._get_iter_data(oIter)
        aTexts, aIcons = self._get_data_card_text(oCard)
        oCell.set_data(aTexts, aIcons, SHOW_TEXT_ONLY)