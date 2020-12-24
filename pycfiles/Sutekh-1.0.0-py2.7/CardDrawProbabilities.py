# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/plugins/CardDrawProbabilities.py
# Compiled at: 2019-12-11 16:37:54
"""Calculate probabilities for drawing the current selection."""
import gtk
from sutekh.SutekhUtility import is_crypt_card
from sutekh.gui.PluginManager import SutekhPlugin
from sutekh.base.core.BaseAdapters import IAbstractCard
from sutekh.base.gui.SutekhDialog import do_complaint_error
from sutekh.base.gui.plugins.BaseDrawProbabilities import BaseDrawProbPlugin

class CardDrawSimPlugin(SutekhPlugin, BaseDrawProbPlugin):
    """Displays the probabilities for drawing cards from the current
       selection."""
    sHelpText = 'This tool displays the probabilities of drawing the selected\n                   cards from the library or the crypt. Unlike the _simulate\n                   opening hand_ tool, this displays results for longer\n                   sequences of card draws.\n\n                   The first row of the table shows the probabilities of\n                   drawing a single card in the selected list. Sub-rows show\n                   the individual probabilities for each possible combination\n                   of selected cards. The second row shows the probabilities of\n                   drawing all possible combinations of two selected cards,\n                   etc..\n\n                   Each probability cell in the table displays two values: the\n                   probability of drawing at least that combination of cards,\n                   and the probability of drawing exactly that combination of\n                   cards (shown in brackets).\n\n                   The tool has the following settings:\n\n                   * _columns in table_: Set the number of draws shown in                    the table. You must specify a number from one to eight                    (the default is eight). The first column shows the                    probabilities of drawing the given cards in your opening                    hand or crypt draw. Subsequent columns show the total                    probabilities of drawing the cards after you have drawn                    the number of extra cards shown in the column header.\n                   * _step between columns_: Set the number of cards drawn                    between columns. You must specify a number from one to                    ten (the default is one).\n                   * _cards of interest_: Set the number of rows in the                    table. You must specify a number from one to the total                    number of cards selected.\n\n                   The selected changes are only applied when you press the\n                   the _recalculate table_ button.'

    def _set_draw_title_and_size(self, oMainTitle):
        """Setup title and draw sizes"""
        if self.bCrypt:
            oMainTitle.set_markup('<b>Crypt:</b> Drawing from <b>%d</b> cards' % self.iTotal)
            self.iOpeningDraw = 4
            self.iNumSteps = min(2, self.iTotal - self.iOpeningDraw)
        else:
            oMainTitle.set_markup('<b>Library:</b> Drawing from <b>%d</b> cards' % self.iTotal)
            self.iOpeningDraw = 7
            self.iNumSteps = min(8, self.iTotal - self.iOpeningDraw)

    def _complain_size(self):
        """Correct complaint about the number of cards."""
        if self.bCrypt:
            do_complaint_error('Crypt must be larger than the opening draw')
        else:
            do_complaint_error('Library must be larger than the opening hand')

    def _setup_cardlists(self, aSelectedCards):
        """Extract the needed card info from the model"""
        aAllAbsCards = [ IAbstractCard(oCard) for oCard in self._get_all_cards()
                       ]
        iCryptSize = 0
        iLibrarySize = 0
        self.dSelectedCounts = {}
        self.iSelectedCount = 0
        for oCard in aSelectedCards:
            self.dSelectedCounts.setdefault(oCard, 0)

        for oCard in aAllAbsCards:
            if is_crypt_card(oCard):
                iCryptSize += 1
            else:
                iLibrarySize += 1
            if oCard in self.dSelectedCounts:
                self.dSelectedCounts[oCard] += 1
                self.iSelectedCount += 1

        if self.bCrypt:
            self.iTotal = iCryptSize
        else:
            self.iTotal = iLibrarySize

    def _check_selection(self, aSelectedCards):
        """Check that selection is useable."""
        bCrypt = False
        bLibrary = False
        for oCard in aSelectedCards:
            if is_crypt_card(oCard):
                bCrypt = True
            else:
                bLibrary = True

        if bLibrary and bCrypt:
            do_complaint_error("Can't operate on selections including both Crypt and Library cards")
            return False
        self.bCrypt = bCrypt
        return True

    def _get_table_draw_title(self):
        """Set the label for the results tabel"""
        if self.bCrypt:
            oLabel = gtk.Label('Opening Draw')
        else:
            oLabel = gtk.Label('Opening Hand')
        return oLabel


plugin = CardDrawSimPlugin