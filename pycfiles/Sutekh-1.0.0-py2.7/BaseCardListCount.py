# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/plugins/BaseCardListCount.py
# Compiled at: 2019-12-11 16:37:39
"""Provide count card options for the full card list"""
import gtk
from ...core.BaseTables import PhysicalCard
from ...core.BaseAdapters import IAbstractCard
from ..BasePluginManager import BasePlugin
from ..MessageBus import MessageBus
from .BaseCountCSCards import TOTAL
SORT_COLUMN_OFFSET = 300

class BaseCardListCount(BasePlugin):
    """Listen to changes on the card list views, and display a toolbar
       containing a label with a running count of the cards in the list.
       """
    dTableVersions = {PhysicalCard: (2, 3)}
    aModelsSupported = (
     PhysicalCard,)
    NO_COUNT, COUNT_CARDS, COUNT_EXP = range(3)
    COLUMN_NAME = '#'
    NO_COUNT_OPT = "Don't show card counts"
    COUNT_CARD_OPT = 'Show counts for each distinct card'
    COUNT_EXP_OPT = 'Show counts for each expansion'
    MODES = {NO_COUNT_OPT: NO_COUNT, 
       COUNT_CARD_OPT: COUNT_CARDS, 
       COUNT_EXP_OPT: COUNT_EXP}
    OPTION_NAME = 'Full Card List Count Mode'
    OPTION_STR = (', ').join('"%s"' % sKey for sKey in sorted(MODES.keys()))
    dCardListConfig = {OPTION_NAME: 'option(%s, default="%s")' % (OPTION_STR, NO_COUNT_OPT)}
    TOT_FORMAT = ''
    TOT_TOOLTIP = ''

    def __init__(self, *args, **kwargs):
        super(BaseCardListCount, self).__init__(*args, **kwargs)
        self._oTextLabel = None
        self._iMode = self.NO_COUNT
        self._dExpCounts = {}
        self._dAbsCounts = {}
        self._dCardTotals = {TOTAL: 0}
        self._dExpTotals = {TOTAL: 0}
        self._add_dict_keys()
        MessageBus.subscribe(self.model, 'load', self.load)
        self.perpane_config_updated()
        return

    def cleanup(self):
        """Remove the listener"""
        MessageBus.unsubscribe(self.model, 'load', self.load)
        super(BaseCardListCount, self).cleanup()

    def _get_card_count(self, oAbsCard):
        """Get the count for the card for the current mode"""
        if self._iMode == self.COUNT_EXP:
            return self._dExpCounts.get(oAbsCard, 0)
        return self._dAbsCounts[oAbsCard]

    def get_toolbar_widget(self):
        """Overrides method from base class."""
        if self._iMode == self.COUNT_CARDS:
            dInfo = self._dCardTotals
        else:
            dInfo = self._dExpTotals
        self._oTextLabel = gtk.Label(self.TOT_FORMAT % dInfo)
        self._oTextLabel.set_tooltip_markup(self.TOT_TOOLTIP % dInfo)
        if self._iMode != self.NO_COUNT:
            self._oTextLabel.show()
        else:
            self._oTextLabel.hide()
        return self._oTextLabel

    def update_numbers(self):
        """Update the label"""
        if self._oTextLabel:
            if self._iMode == self.NO_COUNT:
                self._oTextLabel.hide()
                return
            if self._iMode == self.COUNT_CARDS:
                dInfo = self._dCardTotals
            else:
                dInfo = self._dExpTotals
            self._oTextLabel.set_markup(self.TOT_FORMAT % dInfo)
            self._oTextLabel.set_tooltip_markup(self.TOT_TOOLTIP % dInfo)
            self._oTextLabel.show()

    def load(self, aCards):
        """Listen on load events & update counts"""
        self._dAbsCounts = {}
        self._dExpCounts = {}
        self._dCardTotals = {TOTAL: 0}
        self._dExpTotals = {TOTAL: 0}
        self._add_dict_keys()
        for oCard in aCards:
            oAbsCard = IAbstractCard(oCard)
            if oAbsCard not in self._dAbsCounts:
                self._dAbsCounts[oAbsCard] = 1
                iAbsCount = 1
            else:
                iAbsCount = 0
            if oCard.printingID:
                iExpCount = 1
                if oAbsCard not in self._dExpCounts:
                    self._dExpCounts[oAbsCard] = 1
                else:
                    self._dExpCounts[oAbsCard] += 1
            else:
                iExpCount = 0
            aKeys = self._get_card_keys(oAbsCard)
            for sKey in aKeys:
                self._dCardTotals[sKey] += iAbsCount
                self._dExpTotals[sKey] += iExpCount

            self._dCardTotals[TOTAL] += iAbsCount
            self._dExpTotals[TOTAL] += iExpCount

        self.update_numbers()

    def perpane_config_updated(self, _bDoReload=True):
        """Called by base class on config updates."""
        sCountMode = self.get_perpane_item(self.OPTION_NAME)
        self._iMode = self.MODES.get(sCountMode, self.NO_COUNT)
        if self._iMode == self.NO_COUNT:
            self.clear_col()
        else:
            self.add_col()
        self.update_numbers()

    def _get_cols(self):
        """Get a list holding the column"""
        return [ oCol for oCol in self.view.get_columns() if oCol.get_property('title') == self.COLUMN_NAME
               ]

    def clear_col(self):
        """Remove the column if it's in use"""
        for oCol in self._get_cols():
            self.view.remove_column(oCol)

    def add_col(self):
        """Add the count col"""
        aCols = self._get_cols()
        if aCols:
            return
        oCell = gtk.CellRendererText()
        oColumn = gtk.TreeViewColumn(self.COLUMN_NAME, oCell)
        oColumn.set_cell_data_func(oCell, self._render_count)
        oColumn.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        oColumn.set_fixed_width(40)
        oColumn.set_resizable(True)
        self.view.insert_column(oColumn, 0)
        oColumn.set_sort_column_id(SORT_COLUMN_OFFSET)
        self.model.set_sort_func(SORT_COLUMN_OFFSET, self._sort_count)

    def _get_count(self, oIter):
        """Get the count for this iter"""
        if self.model.iter_depth(oIter) == 0:
            iTot = 0
            oSubIter = self.model.iter_children(oIter)
            while oSubIter:
                iTot += self._get_count(oSubIter)
                oSubIter = self.model.iter_next(oSubIter)

            return iTot
        if self.model.iter_depth(oIter) == 1:
            oAbsCard = self.model.get_abstract_card_from_iter(oIter)
            return self._get_card_count(oAbsCard)
        if self.model.iter_depth(oIter) == 2 and self._iMode == self.COUNT_EXP:
            oPhysCard = self.model.get_physical_card_from_iter(oIter)
            if oPhysCard.printingID:
                return 1
        return 0

    def _render_count(self, _oColumn, oCell, _oModel, oIter):
        """Render the count for the card"""
        iVal = self._get_count(oIter)
        oCell.set_property('text', iVal)

    def _sort_count(self, _oModel, oIter1, oIter2):
        """Card count Comparision of oIter1 and oIter2.

           Return -1 if oIter1 < oIter, 0 in ==, 1 if >
           """
        iVal1 = self._get_count(oIter1)
        iVal2 = self._get_count(oIter2)
        if iVal1 < iVal2:
            return -1
        if iVal1 > iVal2:
            return 1
        return self.model.sort_equal_iters(oIter1, oIter2)

    def _get_card_keys(self, oAbsCard):
        """Get the list of applicable dictionary keys for this card."""
        raise NotImplementedError('Subclasses must implement _get_card_keys')

    def _add_dict_keys(self):
        """Ensure the totals dictionary has all the required keys."""
        raise NotImplementedError('Subclasses must implement _add_dict_keys')