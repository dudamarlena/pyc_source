# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/plugins/CountWWListCards.py
# Compiled at: 2019-12-11 16:37:54
"""Provide count card options for the WW card list"""
from sutekh.gui.PluginManager import SutekhPlugin
from sutekh.SutekhUtility import is_crypt_card
from sutekh.base.gui.plugins.BaseCardListCount import BaseCardListCount
from sutekh.gui.plugins.CountCardSetCards import FORMAT, TOOLTIP, CRYPT, LIB
SORT_COLUMN_OFFSET = 300

class CountWWListCards(SutekhPlugin, BaseCardListCount):
    """Listen to changes on the card list views, and display a toolbar
       containing a label with a running count of the cards in the card
       set, the library cards and the crypt cards
       """
    TOT_FORMAT = FORMAT
    TOT_TOOLTIP = TOOLTIP
    OPTION_NAME = 'White Wolf Card List Count Mode'
    dCardListConfig = {OPTION_NAME: 'option(%s, default="%s")' % (
                   BaseCardListCount.OPTION_STR, BaseCardListCount.NO_COUNT_OPT)}

    def _get_card_keys(self, oAbsCard):
        """Listen on load events & update counts"""
        if is_crypt_card(oAbsCard):
            return [CRYPT]
        return [
         LIB]

    def _add_dict_keys(self):
        """Add 'crypt' and 'library' to the correct dicts"""
        self._dCardTotals[CRYPT] = 0
        self._dCardTotals[LIB] = 0
        self._dExpTotals[CRYPT] = 0
        self._dExpTotals[LIB] = 0


plugin = CountWWListCards