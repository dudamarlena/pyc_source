# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/plugins/ExtraCardSetListViewColumns.py
# Compiled at: 2019-12-11 16:37:54
"""Display extra columns in the tree view"""
from sutekh.gui.PluginManager import SutekhPlugin
from sutekh.base.core.BaseTables import MapPhysicalCardToPhysicalCardSet
from sutekh.base.core.BaseFilters import PhysicalCardSetFilter, FilterAndBox
from sutekh.core.Filters import CryptCardFilter
from sutekh.base.gui.plugins.BaseExtraColumns import get_number, format_number
from sutekh.base.gui.plugins.BaseExtraCSListViewColumns import BaseExtraCSListViewColumns

class ExtraCardSetListViewColumns(SutekhPlugin, BaseExtraCSListViewColumns):
    """Add extra columns to the card set list view.

       Allow the card set list to be sorted on these columns
       """
    COLUMNS = BaseExtraCSListViewColumns.COLUMNS.copy()
    COLUMNS.update({'Library': (100, '_render_library', '_get_data_library'), 
       'Crypt': (100, '_render_crypt', '_get_data_crypt')})
    CS_KEYS = ('Total Cards', 'Library', 'Crypt')
    sMenuName = 'Extra Columns -- card set list view'
    sHelpCategory = 'card_set_list:profile'
    sHelpText = 'Only card set names are shown in the card set list by                    default as well.  You can select additional columns                    to display as part of the card set list profile.\n\n                   The possible extra columns are:\n\n                   * _Author_: Show the card set author.\n                   * _Description_: Show the card set description.\n                   * _Total cards_: Show the total number of cards in the                      card set.\n                   * _Crypt_: Show the number of crypt cards in the card set.\n                   * _Library_: Show the number of library cards in the                      card set.\n                   * _All Children_: Show the number of child card sets each                      card set has\n                   * _In-Use Children_: Show the number of child card sets                      marked as in use.\n\n                   The display can be sorted on these columns by clicking on                    the column headers.'

    @classmethod
    def get_help_list_text(cls):
        return ' Select which extra columns of data are shown.                    See the *Extra Columns -- card set list* section                    for more details.'

    def _get_data_library(self, sCardSet, bGetIcons=True):
        """Return the number of library cards in the card set"""

        def query(oCardSet):
            """Query the database"""
            oFilter = FilterAndBox([PhysicalCardSetFilter(oCardSet.name),
             CryptCardFilter()])
            iCrypt = oFilter.select(MapPhysicalCardToPhysicalCardSet).distinct().count()
            iTot = MapPhysicalCardToPhysicalCardSet.selectBy(physicalCardSetID=oCardSet.id).count()
            return iTot - iCrypt

        if sCardSet:
            dInfo = self._dCache[sCardSet]
            aIcons = []
            iTotal = get_number(dInfo, 'Library', query)
            if bGetIcons:
                aIcons = [
                 None]
            return (iTotal, aIcons)
        else:
            return (
             -1, [])

    def _render_library(self, _oColumn, oCell, _oModel, oIter):
        """display the library count"""
        sCardSet = self._get_iter_data(oIter)
        iCount, aIcons = self._get_data_library(sCardSet, True)
        aText = format_number(iCount)
        oCell.set_data(aText, aIcons, self._iShowMode)

    def _get_data_crypt(self, sCardSet, bGetIcons=True):
        """Return the number of crypt cards in the card set"""

        def query(oCardSet):
            """Query the database"""
            oFilter = FilterAndBox([PhysicalCardSetFilter(oCardSet.name),
             CryptCardFilter()])
            return oFilter.select(MapPhysicalCardToPhysicalCardSet).distinct().count()

        if sCardSet:
            dInfo = self._dCache[sCardSet]
            aIcons = []
            iTotal = get_number(dInfo, 'Crypt', query)
            if bGetIcons:
                aIcons = [
                 None]
            return (iTotal, aIcons)
        else:
            return (
             -1, [])

    def _render_crypt(self, _oColumn, oCell, _oModel, oIter):
        """display the crypt count"""
        sCardSet = self._get_iter_data(oIter)
        iCount, aIcons = self._get_data_crypt(sCardSet, True)
        aText = format_number(iCount)
        oCell.set_data(aText, aIcons, self._iShowMode)


plugin = ExtraCardSetListViewColumns