# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/core/SutekhTables.py
# Compiled at: 2019-12-11 16:37:56
"""The Sutekh specific database definitions"""
from sqlobject import SQLObject, IntCol, UnicodeCol, RelatedJoin, EnumCol, MultipleJoin, DatabaseIndex, ForeignKey
from sutekh.base.core.CachedRelatedJoin import CachedRelatedJoin
from sutekh.base.core.BaseTables import AbstractCard, BASE_TABLE_LIST, MAX_ID_LENGTH

class SutekhAbstractCard(AbstractCard):
    """The abstract card specialised to the needs of VtES."""
    _inheritable = False
    tableversion = 1
    search_text = UnicodeCol(default='')
    group = IntCol(default=None, dbName='grp')
    capacity = IntCol(default=None)
    cost = IntCol(default=None)
    life = IntCol(default=None)
    costtype = EnumCol(enumValues=['pool', 'blood', 'conviction', None], default=None)
    level = EnumCol(enumValues=['advanced', None], default=None)
    discipline = CachedRelatedJoin('DisciplinePair', intermediateTable='abs_discipline_pair_map', joinColumn='abstract_card_id', createRelatedTable=False)
    clan = CachedRelatedJoin('Clan', joinColumn='abstract_card_id', intermediateTable='abs_clan_map', createRelatedTable=False)
    sect = CachedRelatedJoin('Sect', intermediateTable='abs_sect_map', joinColumn='abstract_card_id', createRelatedTable=False)
    title = CachedRelatedJoin('Title', intermediateTable='abs_title_map', joinColumn='abstract_card_id', createRelatedTable=False)
    creed = CachedRelatedJoin('Creed', intermediateTable='abs_creed_map', joinColumn='abstract_card_id', createRelatedTable=False)
    virtue = CachedRelatedJoin('Virtue', intermediateTable='abs_virtue_map', joinColumn='abstract_card_id', createRelatedTable=False)


class DisciplinePair(SQLObject):
    tableversion = 1
    discipline = ForeignKey('Discipline')
    level = EnumCol(enumValues=['inferior', 'superior'])
    disciplineLevelIndex = DatabaseIndex(discipline, level, unique=True)
    cards = RelatedJoin('SutekhAbstractCard', intermediateTable='abs_discipline_pair_map', otherColumn='abstract_card_id', createRelatedTable=False)


class Discipline(SQLObject):
    tableversion = 3
    name = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    fullname = UnicodeCol(default=None)
    pairs = MultipleJoin('DisciplinePair')


class Virtue(SQLObject):
    tableversion = 2
    name = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    fullname = UnicodeCol(default=None)
    cards = RelatedJoin('SutekhAbstractCard', intermediateTable='abs_virtue_map', otherColumn='abstract_card_id', createRelatedTable=False)


class Creed(SQLObject):
    tableversion = 2
    name = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    shortname = UnicodeCol(default=None)
    cards = RelatedJoin('SutekhAbstractCard', intermediateTable='abs_creed_map', otherColumn='abstract_card_id', createRelatedTable=False)


class Clan(SQLObject):
    tableversion = 3
    name = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    shortname = UnicodeCol(default=None)
    cards = RelatedJoin('SutekhAbstractCard', intermediateTable='abs_clan_map', otherColumn='abstract_card_id', createRelatedTable=False)


class Sect(SQLObject):
    tableversion = 2
    name = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    cards = RelatedJoin('SutekhAbstractCard', intermediateTable='abs_sect_map', otherColumn='abstract_card_id', createRelatedTable=False)


class Title(SQLObject):
    tableversion = 2
    name = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    cards = RelatedJoin('SutekhAbstractCard', intermediateTable='abs_title_map', otherColumn='abstract_card_id', createRelatedTable=False)


class MapAbstractCardToClan(SQLObject):

    class sqlmeta:
        table = 'abs_clan_map'

    tableversion = 1
    abstractCard = ForeignKey('SutekhAbstractCard', notNull=True)
    clan = ForeignKey('Clan', notNull=True)
    abstractCardIndex = DatabaseIndex(abstractCard, unique=False)
    clanIndex = DatabaseIndex(clan, unique=False)


class MapAbstractCardToDisciplinePair(SQLObject):

    class sqlmeta:
        table = 'abs_discipline_pair_map'

    tableversion = 1
    abstractCard = ForeignKey('SutekhAbstractCard', notNull=True)
    disciplinePair = ForeignKey('DisciplinePair', notNull=True)
    abstractCardIndex = DatabaseIndex(abstractCard, unique=False)
    disciplinePairIndex = DatabaseIndex(disciplinePair, unique=False)


class MapAbstractCardToSect(SQLObject):

    class sqlmeta:
        table = 'abs_sect_map'

    tableversion = 1
    abstractCard = ForeignKey('SutekhAbstractCard', notNull=True)
    sect = ForeignKey('Sect', notNull=True)
    abstractCardIndex = DatabaseIndex(abstractCard, unique=False)
    sectIndex = DatabaseIndex(sect, unique=False)


class MapAbstractCardToTitle(SQLObject):

    class sqlmeta:
        table = 'abs_title_map'

    tableversion = 1
    abstractCard = ForeignKey('SutekhAbstractCard', notNull=True)
    title = ForeignKey('Title', notNull=True)
    abstractCardIndex = DatabaseIndex(abstractCard, unique=False)
    titleIndex = DatabaseIndex(title, unique=False)


class MapAbstractCardToCreed(SQLObject):

    class sqlmeta:
        table = 'abs_creed_map'

    tableversion = 1
    abstractCard = ForeignKey('SutekhAbstractCard', notNull=True)
    creed = ForeignKey('Creed', notNull=True)
    abstractCardIndex = DatabaseIndex(abstractCard, unique=False)
    creedIndex = DatabaseIndex(creed, unique=False)


class MapAbstractCardToVirtue(SQLObject):

    class sqlmeta:
        table = 'abs_virtue_map'

    tableversion = 1
    abstractCard = ForeignKey('SutekhAbstractCard', notNull=True)
    virtue = ForeignKey('Virtue', notNull=True)
    abstractCardIndex = DatabaseIndex(abstractCard, unique=False)
    virtueIndex = DatabaseIndex(virtue, unique=False)


TABLE_LIST = BASE_TABLE_LIST + [SutekhAbstractCard,
 Discipline, DisciplinePair,
 Clan, Sect, Title, Virtue, Creed,
 MapAbstractCardToClan,
 MapAbstractCardToDisciplinePair,
 MapAbstractCardToSect,
 MapAbstractCardToTitle,
 MapAbstractCardToVirtue,
 MapAbstractCardToCreed]
CRYPT_TYPES = ('Vampire', 'Imbued')