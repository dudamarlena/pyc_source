# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/core/Filters.py
# Compiled at: 2019-12-11 16:37:55
"""Define all the filters provided in sutekh"""
from sqlobject.sqlbuilder import LEFTJOINOn
from sqlobject import SQLObjectNotFound, OR, LIKE, func
from sutekh.base.core.BaseTables import AbstractCard
from sutekh.base.core.BaseAdapters import ICardType
from sutekh.base.core.BaseFilters import IN, Filter, FilterAndBox, FilterOrBox, FilterNot, NullFilter, SingleFilter, MultiFilter, DirectFilter, PhysicalCardFilter, SpecificCardFilter, CardNameFilter, SpecificCardIdFilter, CardTypeFilter, SpecificPhysCardIdFilter, CardSetMultiCardCountFilter, PhysicalCardSetFilter, MultiPhysicalCardSetFilter, PhysicalCardSetInUseFilter, CardSetNameFilter, ExpansionFilter, MultiExpansionFilter, CardSetDescriptionFilter, CardSetAuthorFilter, CardSetAnnotationsFilter, ParentCardSetFilter, MultiExpansionRarityFilter, CSPhysicalCardSetInUseFilter, ExpansionRarityFilter, MultiCardTypeFilter, BaseCardTextFilter, KeywordFilter, MultiKeywordFilter, PrintingFilter, MultiPrintingFilter, PhysicalExpansionFilter, MultiPhysicalExpansionFilter, PhysicalPrintingFilter, MultiPhysicalPrintingFilter, ArtistFilter, MultiArtistFilter, split_list, make_table_alias
from sutekh.core.SutekhTables import SutekhAbstractCard, Clan, Discipline, Title, Creed, Virtue, Sect, CRYPT_TYPES
from sutekh.core.SutekhAdapters import ICreed, IVirtue, IClan, IDiscipline, ITitle, ISect, IDisciplinePair

class SutekhCardFilter(Filter):
    """Base class for filters that required joining SutekhAbstractCard
       to AbstractCard.

       Needs a table alias for when multiple filters are combined."""

    def __init__(self):
        self._oMapTable = make_table_alias('sutekh_abstract_card')
        super(SutekhCardFilter, self).__init__()

    def _get_joins(self):
        return [
         LEFTJOINOn(None, self._oMapTable, AbstractCard.q.id == self._oMapTable.q.id)]


class ClanFilter(SingleFilter):
    """Filter on Card's clan"""
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, sClan):
        self._oId = IClan(sClan).id
        self._oMapTable = make_table_alias('abs_clan_map')
        self._oIdField = self._oMapTable.q.clan_id


class MultiClanFilter(MultiFilter):
    """Filter on multiple clans"""
    keyword = 'Clan'
    islistfilter = True
    description = 'Clan'
    helptext = 'a list of clans\nReturns all cards which require or are of the specified clans'
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, aClans):
        self._aIds = [ IClan(x).id for x in aClans ]
        self._oMapTable = make_table_alias('abs_clan_map')
        self._oIdField = self._oMapTable.q.clan_id

    @classmethod
    def get_values(cls):
        return [ x.name for x in Clan.select().orderBy('name') ]


class DisciplineFilter(MultiFilter):
    """Filter on a card's disciplines"""
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, sDiscipline):
        self._aIds = [ oP.id for oP in IDiscipline(sDiscipline).pairs ]
        self._oMapTable = make_table_alias('abs_discipline_pair_map')
        self._oIdField = self._oMapTable.q.discipline_pair_id


class MultiDisciplineFilter(MultiFilter):
    """Filter on multiple disciplines"""
    keyword = 'Discipline'
    description = 'Discipline'
    helptext = 'a list of disciplines.\nReturns a list of all cards which have or require the selected disciplines.'
    islistfilter = True
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, aDisciplines):
        oPairs = []
        for sDis in aDisciplines:
            oPairs += IDiscipline(sDis).pairs

        self._aIds = [ oP.id for oP in oPairs ]
        self._oMapTable = make_table_alias('abs_discipline_pair_map')
        self._oIdField = self._oMapTable.q.discipline_pair_id

    @classmethod
    def get_values(cls):
        return [ x.fullname for x in Discipline.select().orderBy('name') ]


class DisciplineLevelFilter(MultiFilter):
    """Filter on discipline & level combo"""
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, tDiscLevel):
        sDiscipline, sLevel = tDiscLevel
        sLevel = sLevel.lower()
        assert sLevel in ('inferior', 'superior')
        self._aIds = [ oP.id for oP in IDiscipline(sDiscipline).pairs if oP.level == sLevel
                     ]
        self._oMapTable = make_table_alias('abs_discipline_pair_map')
        self._oIdField = self._oMapTable.q.discipline_pair_id


class MultiDisciplineLevelFilter(MultiFilter):
    """Filter on multiple discipline & level combos"""
    keyword = 'Discipline_with_Level'
    description = 'Discipline with Level'
    helptext = 'a list of disciplines with levels (each element specified as a discipline with associated level, i.e. superior or inferior)\nReturns all matching cards.'
    iswithfilter = True
    islistfilter = True
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, aDiscLevels):
        self._aIds = []
        if isinstance(aDiscLevels[0], basestring):
            aValues = split_list(aDiscLevels)
        else:
            aValues = aDiscLevels
        for sDiscipline, sLevel in aValues:
            sLevel = sLevel.lower()
            assert sLevel in ('inferior', 'superior')
            self._aIds.extend([ oP.id for oP in IDiscipline(sDiscipline).pairs if oP.level == sLevel
                              ])

        self._oMapTable = make_table_alias('abs_discipline_pair_map')
        self._oIdField = self._oMapTable.q.discipline_pair_id

    @classmethod
    def get_values(cls):
        oTemp = MultiDisciplineFilter([])
        aDisciplines = oTemp.get_values()
        aResults = []
        for sDisc in aDisciplines:
            for sLevel in ('inferior', 'superior'):
                try:
                    IDisciplinePair((sDisc, sLevel))
                except SQLObjectNotFound:
                    continue

                aResults.append('%s with %s' % (sDisc, sLevel))

        return aResults


class CryptCardFilter(MultiFilter):
    """Filter on crypt card types"""
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self):
        self._aIds = [ ICardType(x).id for x in CRYPT_TYPES ]
        self._oMapTable = make_table_alias('abs_type_map')
        self._oIdField = self._oMapTable.q.card_type_id


class SectFilter(SingleFilter):
    """Filter on Sect"""
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, sSect):
        self._oId = ISect(sSect).id
        self._oMapTable = make_table_alias('abs_sect_map')
        self._oIdField = self._oMapTable.q.sect_id


class MultiSectFilter(MultiFilter):
    """Filter on Multiple Sects"""
    keyword = 'Sect'
    description = 'Sect'
    helptext = 'a list of sects.\nReturns all cards belonging to the given sects'
    islistfilter = True
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, aSects):
        self._aIds = [ ISect(x).id for x in aSects ]
        self._oMapTable = make_table_alias('abs_sect_map')
        self._oIdField = self._oMapTable.q.sect_id

    @classmethod
    def get_values(cls):
        return [ x.name for x in Sect.select().orderBy('name') ]


class TitleFilter(SingleFilter):
    """Filter on Title"""
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, sTitle):
        self._oId = ITitle(sTitle).id
        self._oMapTable = make_table_alias('abs_title_map')
        self._oIdField = self._oMapTable.q.title_id


class MultiTitleFilter(MultiFilter):
    """Filter on Multiple Titles"""
    keyword = 'Title'
    description = 'Title'
    helptext = 'a list of titles.\nReturns all cards with the selected titles.'
    islistfilter = True
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, aTitles):
        self._aIds = [ ITitle(x).id for x in aTitles ]
        self._oMapTable = make_table_alias('abs_title_map')
        self._oIdField = self._oMapTable.q.title_id

    @classmethod
    def get_values(cls):
        return [ x.name for x in Title.select().orderBy('name') ]


class CreedFilter(SingleFilter):
    """Filter on Creed"""
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, sCreed):
        self._oId = ICreed(sCreed).id
        self._oMapTable = make_table_alias('abs_creed_map')
        self._oIdField = self._oMapTable.q.creed_id


class MultiCreedFilter(MultiFilter):
    """Filter on Multiple Creed"""
    keyword = 'Creed'
    description = 'Creed'
    helptext = 'a list of creeds.\nReturns all cards requiring or of the selected creeds'
    islistfilter = True
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, aCreeds):
        self._aIds = [ ICreed(x).id for x in aCreeds ]
        self._oMapTable = make_table_alias('abs_creed_map')
        self._oIdField = self._oMapTable.q.creed_id

    @classmethod
    def get_values(cls):
        return [ x.name for x in Creed.select().orderBy('name') ]


class VirtueFilter(SingleFilter):
    """Filter on Virtue"""
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, sVirtue):
        self._oId = IVirtue(sVirtue).id
        self._oMapTable = make_table_alias('abs_virtue_map')
        self._oIdField = self._oMapTable.q.virtue_id


class MultiVirtueFilter(MultiFilter):
    """Filter on Multiple Virtues"""
    keyword = 'Virtue'
    description = 'Virtue'
    helptext = 'a list of virtues.\nReturns all cards requiring or having the selected virtues'
    islistfilter = True
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, aVirtues):
        self._aIds = [ IVirtue(x).id for x in aVirtues ]
        self._oMapTable = make_table_alias('abs_virtue_map')
        self._oIdField = self._oMapTable.q.virtue_id

    @classmethod
    def get_values(cls):
        return [ x.fullname for x in Virtue.select().orderBy('name') ]


class GroupFilter(SutekhCardFilter):
    """Filter on Group"""
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, iGroup):
        super(GroupFilter, self).__init__()
        self.__iGroup = iGroup

    def _get_expression(self):
        return self._oMapTable.q.grp == self.__iGroup


class MultiGroupFilter(SutekhCardFilter):
    """Filter on multiple Groups"""
    keyword = 'Group'
    description = 'Group'
    helptext = 'a list of groups.\nReturns all cards belonging to the listed group.'
    islistfilter = True
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, aGroups):
        super(MultiGroupFilter, self).__init__()
        self.__aGroups = [ int(sV) for sV in aGroups if sV != 'Any' ]
        if 'Any' in aGroups:
            self.__aGroups.append(-1)

    @classmethod
    def get_values(cls):
        iMax = SutekhAbstractCard.select().max(SutekhAbstractCard.q.group)
        return [ str(x) for x in range(1, iMax + 1) ] + ['Any']

    def _get_expression(self):
        return IN(self._oMapTable.q.grp, self.__aGroups)


class CapacityFilter(SutekhCardFilter):
    """Filter on Capacity"""
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, iCap):
        super(CapacityFilter, self).__init__()
        self.__iCap = iCap

    def _get_expression(self):
        return self._oMapTable.q.capacity == self.__iCap


class MultiCapacityFilter(SutekhCardFilter):
    """Filter on a list of Capacities"""
    keyword = 'Capacity'
    description = 'Capacity'
    helptext = 'a list of capacities.\nReturns all cards of the selected capacities'
    islistfilter = True
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, aCaps):
        super(MultiCapacityFilter, self).__init__()
        self.__aCaps = [ int(sV) for sV in aCaps ]

    @classmethod
    def get_values(cls):
        iMax = SutekhAbstractCard.select().max(SutekhAbstractCard.q.capacity)
        return [ str(x) for x in range(1, iMax + 1) ]

    def _get_expression(self):
        return IN(self._oMapTable.q.capacity, self.__aCaps)


class CostFilter(SutekhCardFilter):
    """Filter on Cost"""
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, iCost):
        super(CostFilter, self).__init__()
        self.__iCost = iCost
        if not iCost:
            self.__iCost = None
        return

    def _get_expression(self):
        return self._oMapTable.q.cost == self.__iCost


class MultiCostFilter(SutekhCardFilter):
    """Filter on a list of Costs"""
    keyword = 'Cost'
    description = 'Cost'
    helptext = 'a list of costs.\nReturns all cards with the given costs.'
    islistfilter = True
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, aCost):
        super(MultiCostFilter, self).__init__()
        self.__aCost = [ int(sV) for sV in aCost if sV != 'X' ]
        self.__bZeroCost = False
        if 'X' in aCost:
            self.__aCost.append(-1)
        if 0 in self.__aCost:
            self.__bZeroCost = True
            self.__aCost.remove(0)

    @classmethod
    def get_values(cls):
        iMax = SutekhAbstractCard.select().max(SutekhAbstractCard.q.cost)
        return [ str(x) for x in range(0, iMax + 1) ] + ['X']

    def _get_expression(self):
        if self.__bZeroCost:
            if self.__aCost:
                return OR(IN(self._oMapTable.q.cost, self.__aCost), self._oMapTable.q.cost == None)
            return self._oMapTable.q.cost == None
        else:
            return IN(self._oMapTable.q.cost, self.__aCost)


class CostTypeFilter(SutekhCardFilter):
    """Filter on cost type"""
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, sCostType):
        super(CostTypeFilter, self).__init__()
        self.__sCostType = sCostType.lower()
        assert self.__sCostType in ('blood', 'pool', 'conviction', None)
        return

    def _get_expression(self):
        return self._oMapTable.q.costtype == self.__sCostType.lower()


class MultiCostTypeFilter(SutekhCardFilter):
    """Filter on a list of cost types"""
    keyword = 'CostType'
    islistfilter = True
    description = 'Cost Type'
    helptext = 'a list of cost types.\nReturns cards requiring the selected cost types.'
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, aCostTypes):
        super(MultiCostTypeFilter, self).__init__()
        self.__aCostTypes = [ x.lower() for x in aCostTypes if x is not None ]
        for sCostType in self.__aCostTypes:
            assert sCostType in ('blood', 'pool', 'conviction')

        if None in aCostTypes:
            self.__aCostTypes.append(None)
        return

    @classmethod
    def get_values(cls):
        return ['blood', 'pool', 'conviction']

    def _get_expression(self):
        return IN(self._oMapTable.q.costtype, self.__aCostTypes)


class LifeFilter(SutekhCardFilter):
    """Filter on life"""
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, iLife):
        super(LifeFilter, self).__init__()
        self.__iLife = iLife

    def _get_expression(self):
        return self._oMapTable.q.life == self.__iLife


class MultiLifeFilter(SutekhCardFilter):
    """Filter on a list of list values"""
    keyword = 'Life'
    description = 'Life'
    helptext = 'a list of life values.\nReturns allies (both library and crypt cards) and retainers with the selected life.\nFor cases where the life varies, only the base value for life is used.'
    islistfilter = True
    types = ('AbstractCard', 'PhysicalCard')

    def __init__(self, aLife):
        super(MultiLifeFilter, self).__init__()
        self.__aLife = [ int(sV) for sV in aLife ]

    @classmethod
    def get_values(cls):
        iMax = SutekhAbstractCard.select().max(SutekhAbstractCard.q.life)
        return [ str(x) for x in range(1, iMax + 1) ]

    def _get_expression(self):
        return IN(self._oMapTable.q.life, self.__aLife)


class CardTextFilter(BaseCardTextFilter):
    """Filter on Card Text"""

    def __init__(self, sPattern):
        super(CardTextFilter, self).__init__(sPattern)
        self._bBraces = '{' in self._sPattern or '}' in self._sPattern
        self._oMapTable = make_table_alias('sutekh_abstract_card')

    def _get_joins(self):
        return [
         LEFTJOINOn(None, self._oMapTable, AbstractCard.q.id == self._oMapTable.q.id)]

    @classmethod
    def get_values(cls):
        return ''

    def _get_expression(self):
        if self._bBraces:
            return super(CardTextFilter, self)._get_expression()
        return LIKE(func.LOWER(self._oMapTable.q.search_text), '%' + self._sPattern + '%')


class CardFunctionFilter(DirectFilter):
    """Filter for various interesting card properties - unlock,
       stealth, etc."""
    keyword = 'CardFunction'
    description = 'Card Function'
    helptext = 'the chosen function from the list of supported types.\nFunctions include roles such as unlock or bleed modifier.\nReturns all cards matching the given functions.'
    islistfilter = True
    types = ('AbstractCard', 'PhysicalCard')
    __sStealth = 'Stealth action modifiers'
    __sIntercept = 'Intercept reactions'
    __sUnlock = 'Unlock reactions (Wake)'
    __sBounce = 'Bleed redirection reactions (Bounce)'
    __sEnterCombat = 'Enter combat actions (Rush)'
    __sBleedModifier = 'Increased bleed action modifiers'
    __sBleedAction = 'Increased bleed actions'
    __sBleedReduction = 'Bleed reduction reactions'

    def __init__(self, aTypes):
        aFilters = []
        if self.__sStealth in aTypes:
            aFilters.append(FilterAndBox([CardTypeFilter('Action Modifier'),
             CardTextFilter('+_ stealth')]))
        if self.__sIntercept in aTypes:
            aFilters.append(FilterAndBox([CardTypeFilter('Reaction'),
             CardTextFilter('+_ intercept')]))
        if self.__sUnlock in aTypes:
            aFilters.append(FilterAndBox([
             CardTypeFilter('Reaction'),
             FilterOrBox([CardTextFilter('this vampire untaps'),
              CardTextFilter('this reacting vampire untaps'),
              CardTextFilter('untap this vampire'),
              CardTextFilter('untap this reacting vampire'),
              CardTextFilter('as though untapped'),
              CardTextFilter('this vampire unlocks'),
              CardTextFilter('this reacting vampire unlocks'),
              CardTextFilter('unlock this vampire'),
              CardTextFilter('unlock this reacting vampire'),
              CardTextFilter('as though unlocked'),
              CardTextFilter('vampire wakes'),
              CardTextFilter('minion wakes')])]))
        if self.__sBounce in aTypes:
            aFilters.append(FilterAndBox([CardTypeFilter('Reaction'),
             CardTextFilter('is now bleeding')]))
        if self.__sEnterCombat in aTypes:
            aFilters.append(FilterAndBox([CardTypeFilter('Action'),
             CardTextFilter('(D) Enter combat')]))
        if self.__sBleedModifier in aTypes:
            aFilters.append(FilterAndBox([CardTypeFilter('Action Modifier'),
             CardTextFilter('+_ bleed')]))
        if self.__sBleedAction in aTypes:
            aFilters.append(FilterAndBox([
             CardTypeFilter('Action'),
             FilterOrBox([CardTextFilter('(D) bleed%at +_ bleed'),
              CardTextFilter('(D) bleed%with +_ bleed')])]))
        if self.__sBleedReduction in aTypes:
            aFilters.append(FilterAndBox([CardTypeFilter('Reaction'),
             CardTextFilter('bleed'),
             CardTextFilter('reduce')]))
        self._oFilter = FilterOrBox(aFilters)

    @classmethod
    def get_values(cls):
        """Values supported by this filter"""
        aVals = sorted([cls.__sStealth, cls.__sIntercept, cls.__sUnlock,
         cls.__sBounce, cls.__sEnterCombat,
         cls.__sBleedModifier, cls.__sBleedAction,
         cls.__sBleedReduction])
        return aVals

    def _get_joins(self):
        """Joins for the constructed filter"""
        return self._oFilter._get_joins()

    def _get_expression(self):
        """Expression for the constructed filter"""
        return self._oFilter._get_expression()