# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/plugins/ExtraCardViewColumns.py
# Compiled at: 2019-12-11 16:37:54
"""Display extra columns in the tree view"""
from sutekh.gui.PluginManager import SutekhPlugin
from sutekh.base.gui.CellRendererIcons import SHOW_TEXT_ONLY
from sutekh.base.gui.plugins.BaseExtraColumns import format_number
from sutekh.base.gui.plugins.BaseExtraCardViewColumns import BaseExtraCardViewColumns

class ExtraCardViewColumns(SutekhPlugin, BaseExtraCardViewColumns):
    """Add extra columns to the card list view.

       Allow the card list to be sorted on these columns
       """
    COLUMNS = BaseExtraCardViewColumns.COLUMNS.copy()
    COLUMNS.update({'Clans and Creeds': (100, '_render_clan', '_get_data_clan'), 
       'Disciplines and Virtues': (150, '_render_disciplines', '_get_data_disciplines'), 
       'Group': (40, '_render_group', '_get_data_group'), 
       'Title': (100, '_render_title', '_get_data_title'), 
       'Sect': (100, '_render_sect', '_get_data_sect'), 
       'Capacity or Life': (40, '_render_capacity', '_get_data_capacity'), 
       'Cost': (100, '_render_cost', '_get_data_cost_sortkey')})
    sMenuName = 'Extra Columns -- card sets'
    sHelpCategory = 'card_sets:profile'
    sHelpText = "By default, Sutekh only shows card names in the White\n                   Wolf Card List, and card names and card counts in other\n                   card set card lists.  You can select additional columns\n                   to display as part of the pane profile.\n\n                   The possible extra columns are:\n\n                   * _Clans and Creeds:_ Show the Clans or Creeds listed                      on the card.\n                   * _Group:_ Show the group number for the card.\n                   * _Disciplines and Virtues:_ Show the Disciplines or                      Virtues listed on the card.\n                   * _Card Type:_ Show the card type.\n                   * _Expansions:_ Show the expansions in which the card                      has been printed.\n                   * _Capacity or Life:_ Show the capacity associated with                      the card, or its life.\n                   * _Sect_: Show the Sect associated with the card.\n                   * _Title_: Show the political titles listed on the card,                      if it is a crypt card.  Titles listed on library cards                      will not be shown.\n                   * _Card Text_: Show the text printed on the card.\n                   * _Cost_: Show the cost of the card, together with the                      cost type.\n\n                   You can sort the display by a particular column by clicking\n                   on the column header. Click on the same header repeatedly\n                   to toggle between ascending and descending order.\n\n                   Cards which have equal values within the column selected\n                   for sorting are further sorted by the card name. Because\n                   the different cost types aren't comparable, if you choose\n                   to sort by cost, cards will be grouped by cost type first\n                   and sorted within those types.\n\n                   If you have downloaded the icons from the V:EKN site,\n                   you will be able to toggle the display between the\n                   _Show Icons and Names_, _Show Text only_ and\n                   _Show Icons only_ options using the combo box. This setting\n                   will affect all selected columns that can use icons."

    @classmethod
    def get_help_list_text(cls):
        return 'Select which extra columns of data are shown. See the                   *Extra Columns -- card sets* section for more details.'

    def _get_data_clan(self, oCard, bGetIcons=True):
        """get the clan for the card"""
        if oCard is not None:
            aClans = [ x.name for x in oCard.clan ]
            aIcons = []
            if aClans:
                aClans.sort()
                if bGetIcons:
                    dIcons = self.icon_manager.get_icon_list(oCard.clan)
                    if dIcons:
                        aIcons = [ dIcons[x] for x in aClans ]
                return (
                 (' /|').join(aClans).split('|'), aIcons)
            aCreed = [ x.name for x in oCard.creed ]
            aCreed.sort()
            if bGetIcons:
                dIcons = self.icon_manager.get_icon_list(oCard.creed)
                if dIcons:
                    aIcons = [ dIcons[x] for x in aCreed ]
            return (
             (' /|').join(aCreed).split('|'), aIcons)
        return ([], [])

    def _render_clan(self, _oColumn, oCell, _oModel, oIter):
        """display the clan"""
        oCard = self._get_iter_data(oIter)
        aText, aIcons = self._get_data_clan(oCard)
        oCell.set_data(aText, aIcons, self._iShowMode)

    def _get_data_disciplines(self, oCard, bGetIcons=True):
        """get discipline info for card"""
        if oCard is not None:
            aInfo = [ (oP.level != 'superior' and oP.discipline.name or oP.discipline.name.upper(), oP.discipline.name) for oP in oCard.discipline
                    ]
            if aInfo:
                aInfo.sort(key=lambda x: x[0].swapcase())
                if bGetIcons:
                    dIcons = self.icon_manager.get_icon_list(oCard.discipline)
                    aIcons = [ dIcons[x[1]] for x in aInfo ]
                else:
                    aIcons = []
                aDis = (', ').join([ x[0] for x in aInfo ]).split(' ')
                return (
                 aDis, aIcons)
            aInfo = [ oV.name for oV in oCard.virtue ]
            if aInfo:
                aInfo.sort()
                if bGetIcons:
                    dIcons = self.icon_manager.get_icon_list(oCard.virtue)
                    aIcons = [ dIcons[x] for x in aInfo ]
                else:
                    aIcons = []
                aVirt = (', ').join(aInfo).split(' ')
                return (
                 aVirt, aIcons)
        return ([], [])

    def _render_disciplines(self, _oColumn, oCell, _oModel, oIter):
        """display the card disciplines"""
        oCard = self._get_iter_data(oIter)
        aText, aIcons = self._get_data_disciplines(oCard)
        oCell.set_data(aText, aIcons, self._iShowMode)

    def _get_data_group(self, oCard, _bGetIcons=True):
        """get the group info for the card"""
        if oCard is not None and oCard.group is not None:
            return (oCard.group, [None])
        else:
            return (
             -100, [None])

    def _render_group(self, _oColumn, oCell, _oModel, oIter):
        """Display the group info"""
        oCard = self._get_iter_data(oIter)
        iGrp, aIcons = self._get_data_group(oCard)
        if iGrp != -100:
            if iGrp == -1:
                oCell.set_data(['Any'], aIcons, SHOW_TEXT_ONLY)
            else:
                oCell.set_data([str(iGrp)], aIcons, SHOW_TEXT_ONLY)
        else:
            oCell.set_data([''], aIcons, SHOW_TEXT_ONLY)

    def _get_data_capacity(self, oCard, _bGetIcons=True):
        """Get the card's capacity"""
        if oCard is not None and oCard.capacity is not None:
            return (oCard.capacity, [None])
        else:
            if oCard is not None and oCard.life is not None:
                return (oCard.life, [None])
            return (
             -1, [None])

    def _render_capacity(self, _oColumn, oCell, _oModel, oIter):
        """Display capacity in the column"""
        oCard = self._get_iter_data(oIter)
        iCap, aIcons = self._get_data_capacity(oCard)
        aText = format_number(iCap)
        oCell.set_data(aText, aIcons, SHOW_TEXT_ONLY)

    def _get_data_cost(self, oCard, _bGetIcons=True):
        """Get the card's cost"""
        if oCard is not None and oCard.cost is not None:
            return (oCard.cost, oCard.costtype, [None])
        else:
            return (
             0, '', [None])

    def _get_data_cost_sortkey(self, oCard, bGetIcons=True):
        """Get the sort key for sorting by cost.

           We want to group the cost types together, since the different
           types aren't comparable, hence the key is constructed as
           costtype + cost.
           We ensure that cost X cards sort after other values.
           """
        iCost, sCostType, aIcons = self._get_data_cost(oCard, bGetIcons)
        if iCost > 0:
            sKey = '%s %d' % (sCostType, iCost)
        elif iCost == -1:
            sKey = '%s X' % sCostType
        else:
            sKey = ''
        return (
         sKey, aIcons)

    def _render_cost(self, _oColumn, oCell, _oModel, oIter):
        """Display cost in the column"""
        oCard = self._get_iter_data(oIter)
        iCost, sCostType, aIcons = self._get_data_cost(oCard)
        if iCost > 0:
            oCell.set_data(['%d %s' % (iCost, sCostType)], aIcons, SHOW_TEXT_ONLY)
        elif iCost == -1:
            oCell.set_data(['X %s' % sCostType], aIcons, SHOW_TEXT_ONLY)
        else:
            oCell.set_data([''], aIcons, SHOW_TEXT_ONLY)

    def _get_data_title(self, oCard, bGetIcons=True):
        """Get the card's title."""
        if oCard is not None:
            aTitles = [ oT.name for oT in oCard.title ]
            aTitles.sort()
            aIcons = []
            if bGetIcons:
                aIcons = [
                 None] * len(aTitles)
            return (aTitles, aIcons)
        else:
            return ([], [])

    def _render_title(self, _oColumn, oCell, _oModel, oIter):
        """Display title in the column"""
        oCard = self._get_iter_data(oIter)
        aTitles, aIcons = self._get_data_title(oCard)
        oCell.set_data(aTitles, aIcons, SHOW_TEXT_ONLY)

    def _get_data_sect(self, oCard, bGetIcons=True):
        """Get the card's sect."""
        if oCard is not None:
            aSects = [ oS.name for oS in oCard.sect ]
            aSects.sort()
            aIcons = []
            if bGetIcons:
                aIcons = [
                 None] * len(aSects)
            return (aSects, aIcons)
        else:
            return ([], [])

    def _render_sect(self, _oColumn, oCell, _oModel, oIter):
        """Display sect in the column"""
        oCard = self._get_iter_data(oIter)
        aSects, aIcons = self._get_data_sect(oCard)
        oCell.set_data(aSects, aIcons, SHOW_TEXT_ONLY)


plugin = ExtraCardViewColumns