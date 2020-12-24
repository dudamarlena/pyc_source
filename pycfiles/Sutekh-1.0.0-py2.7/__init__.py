# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/__init__.py
# Compiled at: 2019-12-11 16:38:02
"""This is the sutekh package.
   """
from sutekh.base.core.BaseTables import AbstractCard, PhysicalCard, PhysicalCardSet, RarityPair, Expansion, Rarity, CardType, Ruling
from sutekh.core.SutekhTables import DisciplinePair, Discipline, Clan
from sutekh.base.core.BaseFilters import FilterAndBox, FilterOrBox, CardTypeFilter, MultiCardTypeFilter, PhysicalCardSetFilter, PhysicalCardFilter, ExpansionFilter, MultiExpansionFilter, PhysicalExpansionFilter, CardNameFilter, MultiPhysicalExpansionFilter, CardSetNameFilter, CardSetDescriptionFilter, CardSetAuthorFilter, CardSetAnnotationsFilter
from sutekh.base.core.DBUtility import make_adapter_caches
from sutekh.core.Filters import ClanFilter, DisciplineFilter, CardTextFilter, MultiDisciplineFilter, MultiClanFilter, GroupFilter, MultiGroupFilter
from sutekh.base.core.BaseGroupings import CardTypeGrouping, ExpansionGrouping, RarityGrouping
from sutekh.core.Groupings import ClanGrouping, DisciplineGrouping
from sutekh.core.CardListTabulator import CardListTabulator
from sutekh.SutekhCli import main_with_args

def start(aArgs=[
 'sutekh']):
    """Initialise SQLObject connection and so forth, for working in the
       python interpreter"""
    main_with_args(aArgs)
    make_adapter_caches()


ALL = [
 AbstractCard, PhysicalCard, PhysicalCardSet,
 RarityPair, Expansion, Rarity, DisciplinePair, Discipline,
 Clan, CardType, Ruling,
 FilterAndBox, FilterOrBox, ClanFilter, DisciplineFilter,
 CardTypeFilter, CardTextFilter, MultiCardTypeFilter,
 MultiDisciplineFilter, MultiClanFilter, PhysicalCardSetFilter,
 PhysicalCardFilter, GroupFilter, MultiGroupFilter,
 ExpansionFilter, MultiExpansionFilter, CardNameFilter,
 CardSetNameFilter, CardSetAuthorFilter, CardSetDescriptionFilter,
 CardSetAnnotationsFilter, PhysicalExpansionFilter,
 MultiPhysicalExpansionFilter,
 CardTypeGrouping, ClanGrouping, DisciplineGrouping,
 ExpansionGrouping, RarityGrouping,
 start, CardListTabulator]
__all__ = [ x.__name__ for x in ALL ]