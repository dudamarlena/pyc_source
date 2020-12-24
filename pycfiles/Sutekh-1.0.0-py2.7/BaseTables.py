# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/core/BaseTables.py
# Compiled at: 2019-12-11 16:37:48
"""The base database definitions"""
from sqlobject import sqlmeta, SQLObject, IntCol, UnicodeCol, RelatedJoin, MultipleJoin, BoolCol, DatabaseIndex, ForeignKey
from sqlobject.inheritance import InheritableSQLObject
from .CachedRelatedJoin import CachedRelatedJoin
MAX_ID_LENGTH = 512

class VersionTable(SQLObject):
    TableName = UnicodeCol(alternateID=True, length=50)
    Version = IntCol(default=None)
    tableversion = 1


class Metadata(SQLObject):
    tableversion = 2
    dataKey = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    value = UnicodeCol()


class AbstractCard(InheritableSQLObject):
    tableversion = 7
    sqlmeta.lazyUpdate = True
    canonicalName = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    name = UnicodeCol()
    text = UnicodeCol()
    rarity = CachedRelatedJoin('RarityPair', intermediateTable='abs_rarity_pair_map', joinColumn='abstract_card_id', createRelatedTable=False)
    cardtype = CachedRelatedJoin('CardType', intermediateTable='abs_type_map', joinColumn='abstract_card_id', createRelatedTable=False)
    rulings = CachedRelatedJoin('Ruling', intermediateTable='abs_ruling_map', joinColumn='abstract_card_id', createRelatedTable=False)
    artists = CachedRelatedJoin('Artist', intermediateTable='abs_artist_map', joinColumn='abstract_card_id', createRelatedTable=False)
    keywords = CachedRelatedJoin('Keyword', intermediateTable='abs_keyword_map', joinColumn='abstract_card_id', createRelatedTable=False)
    physicalCards = MultipleJoin('PhysicalCard')


class PhysicalCard(SQLObject):
    tableversion = 3
    abstractCard = ForeignKey('AbstractCard')
    abstractCardIndex = DatabaseIndex(abstractCard)
    printing = ForeignKey('Printing', notNull=False)
    sets = RelatedJoin('PhysicalCardSet', intermediateTable='physical_map', createRelatedTable=False)


class PhysicalCardSet(SQLObject):
    tableversion = 7
    name = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    author = UnicodeCol(default='')
    comment = UnicodeCol(default='')
    annotations = UnicodeCol(default='')
    inuse = BoolCol(default=False)
    parent = ForeignKey('PhysicalCardSet', default=None)
    cards = RelatedJoin('PhysicalCard', intermediateTable='physical_map', createRelatedTable=False)
    parentIndex = DatabaseIndex(parent)


class RarityPair(SQLObject):
    tableversion = 1
    expansion = ForeignKey('Expansion')
    rarity = ForeignKey('Rarity')
    cards = RelatedJoin('AbstractCard', intermediateTable='abs_rarity_pair_map', createRelatedTable=False)
    expansionRarityIndex = DatabaseIndex(expansion, rarity, unique=True)


class Expansion(SQLObject):
    tableversion = 5
    name = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    shortname = UnicodeCol(default=None)
    pairs = MultipleJoin('RarityPair')
    printings = MultipleJoin('Printing')


class PrintingProperty(SQLObject):
    tableversion = 1
    canonicalValue = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    value = UnicodeCol(length=MAX_ID_LENGTH)
    printings = RelatedJoin('Printing', intermediateTable='printing_data_map', createRelatedTable=False)


class Printing(SQLObject):
    tableversion = 1
    expansion = ForeignKey('Expansion', notNull=True)
    name = UnicodeCol(length=MAX_ID_LENGTH, default=None, notNull=False)
    properties = CachedRelatedJoin('PrintingProperty', intermediateTable='printing_data_map', joinColumn='printing_id', createRelatedTable=False)


class Rarity(SQLObject):
    tableversion = 3
    name = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    shortname = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)


class CardType(SQLObject):
    tableversion = 2
    name = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    cards = RelatedJoin('AbstractCard', intermediateTable='abs_type_map', createRelatedTable=False)


class Ruling(SQLObject):
    tableversion = 2
    text = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    code = UnicodeCol()
    url = UnicodeCol(default=None)
    cards = RelatedJoin('AbstractCard', intermediateTable='abs_ruling_map', createRelatedTable=False)


class Artist(SQLObject):
    tableversion = 1
    canonicalName = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    name = UnicodeCol()
    cards = RelatedJoin('AbstractCard', intermediateTable='abs_artist_map', createRelatedTable=False)


class Keyword(SQLObject):
    tableversion = 1
    keyword = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    cards = RelatedJoin('AbstractCard', intermediateTable='abs_keyword_map', createRelatedTable=False)


class MapPhysicalCardToPhysicalCardSet(SQLObject):

    class sqlmeta:
        table = 'physical_map'

    tableversion = 1
    physicalCard = ForeignKey('PhysicalCard', notNull=True)
    physicalCardSet = ForeignKey('PhysicalCardSet', notNull=True)
    physicalCardIndex = DatabaseIndex(physicalCard, unique=False)
    physicalCardSetIndex = DatabaseIndex(physicalCardSet, unique=False)
    jointIndex = DatabaseIndex(physicalCard, physicalCardSet, unique=False)


class MapAbstractCardToRarityPair(SQLObject):

    class sqlmeta:
        table = 'abs_rarity_pair_map'

    tableversion = 1
    abstractCard = ForeignKey('AbstractCard', notNull=True)
    rarityPair = ForeignKey('RarityPair', notNull=True)
    abstractCardIndex = DatabaseIndex(abstractCard, unique=False)
    rarityPairIndex = DatabaseIndex(rarityPair, unique=False)


class MapAbstractCardToRuling(SQLObject):

    class sqlmeta:
        table = 'abs_ruling_map'

    tableversion = 1
    abstractCard = ForeignKey('AbstractCard', notNull=True)
    ruling = ForeignKey('Ruling', notNull=True)
    abstractCardIndex = DatabaseIndex(abstractCard, unique=False)
    rulingIndex = DatabaseIndex(ruling, unique=False)


class MapAbstractCardToCardType(SQLObject):

    class sqlmeta:
        table = 'abs_type_map'

    tableversion = 1
    abstractCard = ForeignKey('AbstractCard', notNull=True)
    cardType = ForeignKey('CardType', notNull=True)
    abstractCardIndex = DatabaseIndex(abstractCard, unique=False)
    cardTypeIndex = DatabaseIndex(cardType, unique=False)


class MapAbstractCardToArtist(SQLObject):

    class sqlmeta:
        table = 'abs_artist_map'

    tableversion = 1
    abstractCard = ForeignKey('AbstractCard', notNull=True)
    artist = ForeignKey('Artist', notNull=True)
    abstractCardIndex = DatabaseIndex(abstractCard, unique=False)
    artistIndex = DatabaseIndex(artist, unique=False)


class MapAbstractCardToKeyword(SQLObject):

    class sqlmeta:
        table = 'abs_keyword_map'

    tableversion = 1
    abstractCard = ForeignKey('AbstractCard', notNull=True)
    keyword = ForeignKey('Keyword', notNull=True)
    abstractCardIndex = DatabaseIndex(abstractCard, unique=False)
    keywordIndex = DatabaseIndex(keyword, unique=False)


class LookupHints(SQLObject):
    tableversion = 1
    domain = UnicodeCol(length=MAX_ID_LENGTH)
    lookup = UnicodeCol()
    value = UnicodeCol()


class MapPrintingToPrintingProperty(SQLObject):

    class sqlmeta:
        table = 'printing_data_map'

    tableversion = 1
    printing = ForeignKey('Printing', notNull=True)
    printingProperty = ForeignKey('PrintingProperty', notNull=True)
    printingIndex = DatabaseIndex(printing, unique=False)
    propertyIndex = DatabaseIndex(printingProperty, unique=False)


BASE_TABLE_LIST = [
 AbstractCard, Expansion, Printing, PhysicalCard,
 PhysicalCardSet, Rarity, RarityPair, CardType, Ruling,
 Artist, Keyword, LookupHints, PrintingProperty,
 Metadata,
 MapPhysicalCardToPhysicalCardSet,
 MapAbstractCardToRarityPair,
 MapAbstractCardToRuling,
 MapAbstractCardToCardType,
 MapAbstractCardToArtist,
 MapAbstractCardToKeyword,
 MapPrintingToPrintingProperty]
PHYSICAL_SET_LIST = [
 PhysicalCardSet, MapPhysicalCardToPhysicalCardSet]
PHYSICAL_LIST = [
 PhysicalCard] + PHYSICAL_SET_LIST