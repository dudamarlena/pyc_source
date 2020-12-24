# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/plugins/ClanDisciplineStats.py
# Compiled at: 2019-12-11 16:37:54
"""Plugin for analysing all clans and determining the discipline
   spreads of the vampires in each.
   """
import gtk, pango, gobject
from sqlobject import SQLObjectNotFound
from sutekh.base.core.BaseTables import PhysicalCard
from sutekh.base.core.BaseAdapters import ICardType, IKeyword
from sutekh.core.SutekhTables import Clan, SutekhAbstractCard
from sutekh.gui.PluginManager import SutekhPlugin
from sutekh.base.gui.SutekhDialog import SutekhDialog
from sutekh.base.gui.AutoScrolledWindow import AutoScrolledWindow

class ClanDisciplineStats(SutekhPlugin):
    """Display discipline spread for all clans.

       A dialog listing discipline spreads per clan is shown,
       along with useful stats about the disciline spread.
       The user can break down the analysis by vampire groups.
       """
    dTableVersions = {}
    aModelsSupported = (
     PhysicalCard,)
    sMenuName = 'Clan Discipline Stats'
    sHelpCategory = 'card_list:analysis'
    sHelpText = "This shows an analysis of all the different clans in the\n                   White Wolf card list. For each clan, it displays the total\n                   number of vampires in the clan, the sum of the vampires'\n                   capacities, and the most common disciplines. It also shows\n                   the score for the disciplines, and various stats about how\n                   the disciplines are distributed.\n\n                   You can expand the tree view to show the details for each\n                   legal grouping combination.\n\n                   The score is intended to give you some indication of how\n                   common disciplines are within the clan. Vampires without\n                   a discipline score 0 for that discipline, vampires with\n                   the inferior discipline score 1 and vampires with the\n                   superior discipline score 2.\n\n                   Note that this will only include cards not legal for\n                   tournament play (such as banned cards or storyline only\n                   cards) if the current profile for the full card list shows\n                   those cards."

    def __init__(self, *args, **kwargs):
        super(ClanDisciplineStats, self).__init__(*args, **kwargs)
        self._oStatsVbox = None
        return

    def get_menu_item(self):
        """Register on the 'Analyze' menu"""
        oClanStats = gtk.MenuItem(self.sMenuName)
        oClanStats.connect('activate', self.activate)
        return ('Analyze', oClanStats)

    def activate(self, _oWidget):
        """Handle response from menu"""
        oDlg = self.make_dialog()
        oDlg.run()
        self._oStatsVbox = None
        return

    def make_dialog(self):
        """Create the dialog to display the statistics"""
        oDlg = SutekhDialog('Clan Vampire Statistics', self.parent, gtk.DIALOG_DESTROY_WITH_PARENT)
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

        oView = StatsView(self.model.hideillegal)
        self._oStatsVbox.pack_start(AutoScrolledWindow(oView, True))
        self._oStatsVbox.show_all()


class GroupStats(object):
    """Manage statistics for a set of vampire groups."""

    def __init__(self):
        self.iVamps = 0
        self.iTotalCapacity = 0
        self.dDisciplines = {}

    def add_vamp(self, oVamp):
        """Process a single vampire from the group and clan"""
        self.iVamps += 1
        self.iTotalCapacity += oVamp.capacity
        for oPair in oVamp.discipline:
            oDis = oPair.discipline
            aStats = self.dDisciplines.get(oDis.id, [oDis, 0, 0, 0])
            if oPair.level == 'inferior':
                aStats[2] += 1
                aStats[3] += 1
            else:
                aStats[1] += 1
                aStats[3] += 2
            self.dDisciplines[oDis.id] = aStats

    def top_n(self, iNum):
        """Return the iNum highest scoring stats"""
        aScores = [ (oId, aStats[3]) for oId, aStats in self.dDisciplines.items()
                  ]
        aScores.sort(key=lambda x: x[1])
        aScores.reverse()
        aScores = aScores[:iNum]
        return [ self.dDisciplines[oId] for oId, _iScore in aScores ]


class ClanStats(object):
    """Manage combined statistics for a clan"""

    def __init__(self, iMaxGrp):
        self.oAllStats = GroupStats()
        self.dSubStats = {}
        for iGrp in range(1, iMaxGrp):
            self.dSubStats[(iGrp, iGrp + 1)] = GroupStats()

    def add_vamp(self, oVamp):
        """Process a vampire to the total"""
        self.oAllStats.add_vamp(oVamp)
        for tGrps, oStats in self.dSubStats.items():
            if oVamp.group in tGrps:
                oStats.add_vamp(oVamp)


class StatsView(gtk.TreeView):
    """TreeView used to display clan discipline stats"""

    def __init__(self, bHideIllegal):
        self._oModel = StatsModel(bHideIllegal)
        self._aLabels = [
         'Clan', 'Groups', '#', 'Total Cap.', 'Top 5 Disps.',
         '# Sup / # Inf', 'Score', 'Score / Vamp', 'Score / Total Cap.']
        super(StatsView, self).__init__(self._oModel)
        oCell = gtk.CellRendererText()
        oCell.set_property('style', pango.STYLE_ITALIC)
        for iCol, sLabel in enumerate(self._aLabels):
            oColumn = gtk.TreeViewColumn(sLabel, oCell, text=iCol)
            oColumn.set_sort_column_id(iCol)
            self.append_column(oColumn)

        self.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)


class StatsModel(gtk.TreeStore):
    """TreeStore to hold the data about the clan statistics"""

    def __init__(self, bHideIllegal):
        super(StatsModel, self).__init__(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_INT, gobject.TYPE_INT, *([
         gobject.TYPE_STRING] * 5))
        self.oExcludedKeyword = None
        if bHideIllegal:
            try:
                self.oExcludedKeyword = IKeyword('not for legal play')
            except SQLObjectNotFound:
                self.oExcludedKeyword = None

        self.load()
        return

    def load(self):
        """Populate the contents of the TreeStore"""
        self.clear()
        for oClan, oClanStats in self.gather_stats():
            oClanIter = self.append(None)
            self.set_iter_values(oClanIter, oClan, None, oClanStats.oAllStats)
            atGrps = oClanStats.dSubStats.keys()
            atGrps.sort()
            for tGrps in atGrps:
                oSubStats = oClanStats.dSubStats[tGrps]
                if oSubStats.iVamps:
                    oIter = self.append(oClanIter)
                    self.set_iter_values(oIter, oClan, tGrps, oSubStats)

        return

    def set_iter_values(self, oIter, oClan, tGrps, oGrpStats):
        """Fill in the the values for the newly added row oIter"""
        if tGrps:
            sGrps = (',').join([ str(i) for i in tGrps ])
        else:
            sGrps = None
        aTopN = oGrpStats.top_n(5)
        sDisps = (' ').join([ x[0].name.upper() for x in aTopN ])
        sSupInfCnts = (' ').join([ '%d/%d' % (x[1], x[2]) for x in aTopN ])
        sScores = (' ').join([ str(x[3]) for x in aTopN ])
        sScoresPerVamp = (' ').join([ '%.2f' % (float(x[3]) / oGrpStats.iVamps) for x in aTopN
                                    ])
        sScoresPerCap = (' ').join([ '%.2f' % (float(x[3]) / oGrpStats.iTotalCapacity) for x in aTopN
                                   ])
        self.set(oIter, 0, oClan.name, 1, sGrps, 2, oGrpStats.iVamps, 3, oGrpStats.iTotalCapacity, 4, sDisps, 5, sSupInfCnts, 6, sScores, 7, sScoresPerVamp, 8, sScoresPerCap)
        return

    def gather_stats(self):
        """Collect up information on vampires from all clans."""
        iMaxGrp = SutekhAbstractCard.select().max(SutekhAbstractCard.q.group)
        aClans = list(Clan.select())
        aClans.sort(key=lambda x: x.name)
        for oClan in aClans:
            yield (oClan, self.gather_clan_stats(oClan, iMaxGrp))

    def gather_clan_stats(self, oClan, iMaxGrp):
        """Collect information on vampires from a particular clan."""
        oVampType = ICardType('Vampire')
        oClanStats = ClanStats(iMaxGrp)
        for oCard in oClan.cards:
            if oVampType in oCard.cardtype:
                if self.oExcludedKeyword is None or self.oExcludedKeyword not in oCard.keywords:
                    oClanStats.add_vamp(oCard)

        return oClanStats


plugin = ClanDisciplineStats