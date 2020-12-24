# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/plugins/BaseExpansionStats.py
# Compiled at: 2019-12-11 16:37:39
"""Plugin for analysing all expansions and reporting the number of cards
   of each rarity."""
import gtk, pango, gobject
from ...core.BaseTables import PhysicalCard, AbstractCard, Expansion
from ...core.BaseAdapters import IExpansion
from ...core.BaseFilters import NullFilter, make_illegal_filter
from ..BasePluginManager import BasePlugin
from ..SutekhDialog import SutekhDialog
from ..AutoScrolledWindow import AutoScrolledWindow
from ...Utility import get_expansion_date

class BaseExpansionStats(BasePlugin):
    """Display card counts and stats for each expansion, rarity grouping.

       A dialog listing cards for each expansion, split by the rarity,
       with a special category for cards only included in the precon decks.
       The cards are grouped by the current grouping used by the WW card
       list view.
       """
    dTableVersions = {Expansion: (4, 5)}
    aModelsSupported = (
     PhysicalCard,)
    sMenuName = 'Expansion Stats'
    sHelpCategory = 'card_list:analysis'
    sHelpText = 'This lists some statistics about the different\n                   expansions and rarities.\n\n                   For each expansion, this lists the number of cards of each\n                   rarity. It also notes which cards are found only in the\n                   preconstructed decks for that expansion if needed. For each\n                   rarity, the individual cards are list, grouped according\n                   to the current grouping of the full card list.\n\n                   Note that this will only include cards not legal for\n                   tournament play (such as banned cards or storyline only\n                   cards) if the current profile for the full card list shows\n                   those cards.'
    GROUPING = None

    def __init__(self, *args, **kwargs):
        super(BaseExpansionStats, self).__init__(*args, **kwargs)
        self._oStatsVbox = None
        return

    def get_menu_item(self):
        """Register on the 'Analyze' menu"""
        oExpStats = gtk.MenuItem(self.sMenuName)
        oExpStats.connect('activate', self.activate)
        return ('Analyze', oExpStats)

    def activate(self, _oWidget):
        """Handle response from menu"""
        oDlg = self.make_dialog()
        oDlg.run()
        self._oStatsVbox = None
        return

    def make_dialog(self):
        """Create the dialog to display the statistics"""
        oDlg = SutekhDialog('Expansion Statistics', self.parent, gtk.DIALOG_DESTROY_WITH_PARENT)
        oDlg.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        oDlg.connect('response', lambda oW, oR: oDlg.destroy())
        self._oStatsVbox = gtk.VBox(False, 0)
        oDlg.vbox.pack_start(self._oStatsVbox)
        oDlg.set_size_request(600, 400)
        oDlg.show_all()
        self.populate_stats_box()
        return oDlg

    def populate_stats_box(self):
        """Create a tree view of stats in self._oStatsVbox."""
        for oChild in self._oStatsVbox.get_children():
            self._oStatsVbox.remove(oChild)

        oView = StatsView(self.model.groupby, self.GROUPING, self.model.hideillegal)
        self._oStatsVbox.pack_start(AutoScrolledWindow(oView, True))
        self._oStatsVbox.show_all()


class StatsView(gtk.TreeView):
    """TreeView used to display expansion stats"""

    def __init__(self, cGrping, cExpRarityGrping, bHideIllegal):
        self._oModel = StatsModel(cGrping, cExpRarityGrping, bHideIllegal)
        self._aLabels = ['Expansion', 'Date', 'Count']
        super(StatsView, self).__init__(self._oModel)
        oCell = gtk.CellRendererText()
        oCell.set_property('style', pango.STYLE_ITALIC)
        for iCol, sLabel in enumerate(self._aLabels):
            oColumn = gtk.TreeViewColumn(sLabel, oCell, text=iCol)
            oColumn.set_sort_column_id(iCol)
            self.append_column(oColumn)

        self.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)


class StatsModel(gtk.TreeStore):
    """TreeStore to hold the data about the expansion statistics"""

    def __init__(self, cGrping, cExpRarityGrping, bHideIllegal):
        super(StatsModel, self).__init__(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_INT)
        self.cExpRarityGrping = cExpRarityGrping
        self.oLegalFilter = NullFilter()
        if bHideIllegal:
            self.oLegalFilter = make_illegal_filter()
        self.load(cGrping)

    def load(self, cSubGrping):
        """Populate the contents of the TreeStore"""
        self.clear()
        aCards = self.oLegalFilter.select(AbstractCard)
        oGrouping = self.cExpRarityGrping(aCards)
        aTopLevel = []
        oExpIter = None
        iTotal = 0
        dSeenCards = {}
        for sGroup, oGroupIter in sorted(oGrouping):
            oExp = None
            sDate = 'Unknown Date'
            if sGroup != 'Promo':
                sExp, sRarity = sGroup.split(':')
                oExp = IExpansion(sExp.strip())
                oRelDate = get_expansion_date(oExp)
                if oRelDate:
                    sDate = oRelDate.strftime('%Y-%m-%d')
            else:
                sExp, sRarity = ('Promo', None)
                sDate = ''
            if sExp not in aTopLevel:
                dSeenCards[sExp] = set()
                oExpIter = self.append(None)
                self.set(oExpIter, 0, sExp.strip(), 1, sDate)
                aTopLevel.append(sExp)
                iTotal = 0
            aSubCards = list(oGroupIter)
            if sRarity:
                oIter = self.append(oExpIter)
                self.set(oIter, 0, sRarity.strip(), 1, sDate)
                for oCard in aSubCards:
                    if oCard in dSeenCards[sExp]:
                        continue
                    dSeenCards[sExp].add(oCard)
                    iTotal += 1

                self.set(oExpIter, 2, iTotal)
            else:
                oIter = oExpIter
            self.set(oIter, 2, len(aSubCards))
            oSubGroup = cSubGrping(aSubCards)
            for sInfo, oSubGrpIter in sorted(oSubGroup):
                oChildIter = self.append(oIter)
                if not sInfo:
                    sInfo = '<< None >>'
                self.set(oChildIter, 0, sInfo, 1, sDate, 2, len(list(oSubGrpIter)))
                for oCard in sorted(oSubGrpIter, key=lambda x: x.name):
                    oCardIter = self.append(oChildIter)
                    sCard = oCard.name
                    self.set(oCardIter, 0, sCard, 1, sDate, 2, 1)
                    if sGroup == 'Promo':
                        for oPair in oCard.rarity:
                            if not oPair.expansion.name.startswith('Promo-'):
                                continue
                            oExp = oPair.expansion
                            oRelDate = get_expansion_date(oExp)
                            if oRelDate:
                                sDate = oRelDate.strftime('%Y-%m-%d')
                                self.set(oCardIter, 1, sDate)

        return