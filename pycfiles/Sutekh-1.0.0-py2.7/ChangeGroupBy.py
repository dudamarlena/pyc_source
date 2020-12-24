# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/plugins/ChangeGroupBy.py
# Compiled at: 2019-12-11 16:37:54
"""Allow the use to change how the cards are grouped in the CardListView"""
from sutekh.core.Groupings import ClanGrouping, DisciplineGrouping, CryptLibraryGrouping, SectGrouping, TitleGrouping, CostGrouping, GroupGrouping, GroupPairGrouping, DisciplineLevelGrouping
from sutekh.gui.PluginManager import SutekhPlugin
from sutekh.base.gui.plugins.BaseChangeGroupBy import BaseGroupBy

class GroupCardList(SutekhPlugin, BaseGroupBy):
    """Plugin to allow the user to change how cards are grouped."""
    GROUPINGS = BaseGroupBy.GROUPINGS.copy()
    GROUPINGS.update({'Crypt or Library': CryptLibraryGrouping, 
       'Clans and Creeds': ClanGrouping, 
       'Disciplines and Virtues': DisciplineGrouping, 
       'Disciplines (by level) and Virtues': DisciplineLevelGrouping, 
       'Sect': SectGrouping, 
       'Title': TitleGrouping, 
       'Cost': CostGrouping, 
       'Group': GroupGrouping, 
       'Group pairs': GroupPairGrouping})


plugin = GroupCardList