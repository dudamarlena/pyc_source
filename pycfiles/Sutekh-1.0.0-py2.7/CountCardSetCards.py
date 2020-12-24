# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/plugins/CountCardSetCards.py
# Compiled at: 2019-12-11 16:37:54
"""Display a running total of the cards in a card set"""
from sutekh.gui.PluginManager import SutekhPlugin
from sutekh.base.gui.plugins.BaseCountCSCards import BaseCountCSCards
from sutekh.SutekhUtility import is_crypt_card
CRYPT, LIB = ('crypt', 'lib')
FORMAT = 'Tot: <b>%(total)d</b> L: <b>%(lib)d</b> C: <b>%(crypt)d</b>'
TOOLTIP = 'Total Cards: <b>%(total)d</b> (Library: <b>%(lib)d</b> Crypt: <b>%(crypt)d</b>)'

class CountCardSetCards(SutekhPlugin, BaseCountCSCards):
    """Displayy a running count of the cards in the card
       set, the library cards and the crypt cards
       """
    TOT_FORMAT = FORMAT
    TOT_TOOLTIP = TOOLTIP

    def _get_card_keys(self, oAbsCard):
        """Return 'crypt' or 'lib' as approriate"""
        if is_crypt_card(oAbsCard):
            return [CRYPT]
        return [
         LIB]

    def _add_dict_keys(self):
        """Add 'crypt' and 'lib' to the totals dict"""
        self.dInfo[CRYPT] = 0
        self.dInfo[LIB] = 0


plugin = CountCardSetCards