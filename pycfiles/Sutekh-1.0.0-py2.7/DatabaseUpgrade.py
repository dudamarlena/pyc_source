# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/core/DatabaseUpgrade.py
# Compiled at: 2019-12-11 16:37:55
"""Handles the heavy lifting of upgrading the database.

   Holds methods to copy database contents around, utility classes
   to talk to old database versions, and so forth.

   We only support upgrading from the previous stable version
   (currently 0.8)
   """
from sqlobject import sqlhub, SQLObject, IntCol, UnicodeCol, RelatedJoin, EnumCol, MultipleJoin, ForeignKey, DateCol, BoolCol, SQLObjectNotFound
from sutekh.base.core.BaseTables import PhysicalCard, AbstractCard, PhysicalCardSet, Expansion, RarityPair, LookupHints, Rarity, CardType, PrintingProperty, Printing, Metadata, MAX_ID_LENGTH
from sutekh.core.SutekhTables import SutekhAbstractCard, Clan, Virtue, Discipline, Creed, DisciplinePair, Sect, Title, TABLE_LIST
from sutekh.io.WhiteWolfTextParser import strip_braces
from sutekh.base.core.BaseDatabaseUpgrade import BaseDBUpgradeManager
from sutekh.base.core.DatabaseVersion import DatabaseVersion

class Metadata_v1(SQLObject):
    """Table used to upgrade from Metasa v1"""

    class sqlmeta:
        """meta class used to set the correct table"""
        table = Metadata.sqlmeta.table

    key = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    value = UnicodeCol()


class AbstractCard_v5(SQLObject):
    """Table used to upgrade AbstractCard from v5"""

    class sqlmeta:
        """meta class used to set the correct table"""
        table = AbstractCard.sqlmeta.table
        cacheValues = False

    canonicalName = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    name = UnicodeCol()
    text = UnicodeCol()
    group = IntCol(default=None, dbName='grp')
    capacity = IntCol(default=None)
    cost = IntCol(default=None)
    life = IntCol(default=None)
    costtype = EnumCol(enumValues=['pool', 'blood', 'conviction', None], default=None)
    level = EnumCol(enumValues=['advanced', None], default=None)
    discipline = RelatedJoin('DisciplinePair', intermediateTable='abs_discipline_pair_map', createRelatedTable=False)
    rarity = RelatedJoin('RarityPair', intermediateTable='abs_rarity_pair_map', createRelatedTable=False)
    clan = RelatedJoin('Clan', intermediateTable='abs_clan_map', createRelatedTable=False)
    cardtype = RelatedJoin('CardType', intermediateTable='abs_type_map', createRelatedTable=False)
    sect = RelatedJoin('Sect', intermediateTable='abs_sect_map', createRelatedTable=False)
    title = RelatedJoin('Title', intermediateTable='abs_title_map', createRelatedTable=False)
    creed = RelatedJoin('Creed', intermediateTable='abs_creed_map', createRelatedTable=False)
    virtue = RelatedJoin('Virtue', intermediateTable='abs_virtue_map', createRelatedTable=False)
    rulings = RelatedJoin('Ruling', intermediateTable='abs_ruling_map', createRelatedTable=False)
    artists = RelatedJoin('Artist', intermediateTable='abs_artist_map', createRelatedTable=False)
    keywords = RelatedJoin('Keyword', intermediateTable='abs_keyword_map', createRelatedTable=False)
    physicalCards = MultipleJoin('PhysicalCard')


class AbstractCard_v6(SQLObject):
    """Table used to upgrade AbstractCard from v6"""

    class sqlmeta:
        """meta class used to set the correct table"""
        table = AbstractCard.sqlmeta.table
        cacheValues = False

    canonicalName = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    name = UnicodeCol()
    text = UnicodeCol()
    search_text = UnicodeCol(default='')
    group = IntCol(default=None, dbName='grp')
    capacity = IntCol(default=None)
    cost = IntCol(default=None)
    life = IntCol(default=None)
    costtype = EnumCol(enumValues=['pool', 'blood', 'conviction', None], default=None)
    level = EnumCol(enumValues=['advanced', None], default=None)
    discipline = RelatedJoin('DisciplinePair', intermediateTable='abs_discipline_pair_map', createRelatedTable=False)
    rarity = RelatedJoin('RarityPair', intermediateTable='abs_rarity_pair_map', createRelatedTable=False)
    clan = RelatedJoin('Clan', intermediateTable='abs_clan_map', createRelatedTable=False)
    cardtype = RelatedJoin('CardType', intermediateTable='abs_type_map', createRelatedTable=False)
    sect = RelatedJoin('Sect', intermediateTable='abs_sect_map', createRelatedTable=False)
    title = RelatedJoin('Title', intermediateTable='abs_title_map', createRelatedTable=False)
    creed = RelatedJoin('Creed', intermediateTable='abs_creed_map', createRelatedTable=False)
    virtue = RelatedJoin('Virtue', intermediateTable='abs_virtue_map', createRelatedTable=False)
    rulings = RelatedJoin('Ruling', intermediateTable='abs_ruling_map', createRelatedTable=False)
    artists = RelatedJoin('Artist', intermediateTable='abs_artist_map', createRelatedTable=False)
    keywords = RelatedJoin('Keyword', intermediateTable='abs_keyword_map', createRelatedTable=False)
    physicalCards = MultipleJoin('PhysicalCard')


class PhysicalCard_ACv5(SQLObject):
    """Table used to upgrade AbstractCard from v5"""

    class sqlmeta:
        """meta class used to set the correct table"""
        table = PhysicalCard.sqlmeta.table
        cacheValues = False

    abstractCard = ForeignKey('AbstractCard_v5')
    expansion = ForeignKey('Expansion_v3', notNull=False)
    sets = RelatedJoin('PhysicalCardSet', intermediateTable='physical_map', createRelatedTable=False)


class PhysicalCard_ACv6(SQLObject):
    """Table used to upgrade AbstractCard from v6"""

    class sqlmeta:
        """meta class used to set the correct table"""
        table = PhysicalCard.sqlmeta.table
        cacheValues = False

    abstractCard = ForeignKey('AbstractCard_v6')
    expansion = ForeignKey('Expansion', notNull=False)
    sets = RelatedJoin('PhysicalCardSet', intermediateTable='physical_map', createRelatedTable=False)


class Expansion_v3(SQLObject):
    """Table used to update Expansion from v3"""

    class sqlmeta:
        """meta class used to set the correct table"""
        table = Expansion.sqlmeta.table
        cacheValues = False

    name = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    shortname = UnicodeCol(default=None)
    pairs = MultipleJoin('RarityPair_Ev3')


class RarityPair_Ev3(SQLObject):
    """Table used to update Expansion from v3"""

    class sqlmeta:
        """meta class used to set the correct table"""
        table = RarityPair.sqlmeta.table
        cacheValues = False

    expansion = ForeignKey('Expansion_v3')
    rarity = ForeignKey('Rarity')


class PhysicalCard_v2(SQLObject):
    """Table used to upgrade PhysicalCard from v2"""

    class sqlmeta:
        """meta class used to set the correct table"""
        table = PhysicalCard.sqlmeta.table
        cacheValues = False

    abstractCard = ForeignKey('AbstractCard')
    expansion = ForeignKey('Expansion_v4', notNull=False)
    sets = RelatedJoin('PhysicalCardSet', intermediateTable='physical_map', createRelatedTable=False)


class PhysicalCardSet_PCv3(SQLObject):
    """Physical Card Set to update from Physical Card v2"""

    class sqlmeta:
        """meta class used to set the correct table"""
        table = PhysicalCardSet.sqlmeta.table
        cacheValues = False

    name = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    author = UnicodeCol(default='')
    comment = UnicodeCol(default='')
    annotations = UnicodeCol(default='')
    inuse = BoolCol(default=False)
    parent = ForeignKey('PhysicalCardSet_PCv3', default=None)
    cards = RelatedJoin('PhysicalCard_v2', intermediateTable='physical_map', createRelatedTable=False)


class Expansion_v4(SQLObject):
    """Table used to update Expansion from v4"""

    class sqlmeta:
        """meta class used to set the correct table"""
        table = Expansion.sqlmeta.table
        cacheValues = False

    name = UnicodeCol(alternateID=True, length=MAX_ID_LENGTH)
    shortname = UnicodeCol(default=None)
    releasedate = DateCol(default=None)
    pairs = MultipleJoin('RarityPair_Ev3')


class RarityPair_Ev4(SQLObject):
    """Table used to update Expansion from v4"""

    class sqlmeta:
        """meta class used to set the correct table"""
        table = RarityPair.sqlmeta.table
        cacheValues = False

    expansion = ForeignKey('Expansion_v4')
    rarity = ForeignKey('Rarity')


def _lookup_printing_for_exp(oExpID, oConn):
    if oExpID is None:
        return
    else:
        oPrinting = Printing.selectBy(expansionID=oExpID, name=None, connection=oConn).getOne()
        return oPrinting.id


class DBUpgradeManager(BaseDBUpgradeManager):
    """Class to handle database upgrades,"""
    SUPPORTED_TABLES = BaseDBUpgradeManager.SUPPORTED_TABLES
    SUPPORTED_TABLES.update({'Discipline': (
                    Discipline, (Discipline.tableversion,)), 
       'Clan': (
              Clan, (Clan.tableversion,)), 
       'Creed': (
               Creed, (Creed.tableversion,)), 
       'Virtue': (
                Virtue, (Virtue.tableversion,)), 
       'Sect': (
              Sect, (Sect.tableversion,)), 
       'DisciplinePair': (
                        DisciplinePair, (DisciplinePair.tableversion,)), 
       'Title': (
               Title, (Title.tableversion,))})
    SUPPORTED_TABLES['Expansion'] = (
     Expansion, (Expansion.tableversion, 3, 4))
    SUPPORTED_TABLES['AbstractCard'] = (AbstractCard,
     (
      AbstractCard.tableversion, 5, 6))
    SUPPORTED_TABLES['PhysicalCardSet'] = (PhysicalCardSet,
     (
      PhysicalCardSet.tableversion, 6))
    SUPPORTED_TABLES['Metadata'] = (Metadata, (-1, 1, Expansion.tableversion))
    COPY_OLD_DB = [
     (
      '_copy_old_discipline', 'Discipline table', False),
     (
      '_copy_old_clan', 'Clan table', False),
     (
      '_copy_old_creed', 'Creed table', False),
     (
      '_copy_old_virtue', 'Virtue table', False),
     (
      '_copy_old_discipline_pair', 'DisciplinePair table', False),
     (
      '_copy_old_sect', 'Sect table', False),
     (
      '_copy_old_title', 'Title table', False)] + BaseDBUpgradeManager.COPY_OLD_DB
    COPY_DB = [
     (
      '_copy_discipline', 'Discipline table', False),
     (
      '_copy_clan', 'Clan table', False),
     (
      '_copy_creed', 'Creed table', False),
     (
      '_copy_virtue', 'Virtue table', False),
     (
      '_copy_discipline_pair', 'DisciplinePair table', False),
     (
      '_copy_sect', 'Sect table', False),
     (
      '_copy_title', 'Title table', False)] + BaseDBUpgradeManager.COPY_DB
    cAbstractCardCls = SutekhAbstractCard
    _aTableList = TABLE_LIST

    def old_database_count(self, oConn):
        """Check number of items in old DB fro progress bars, etc."""
        oVer = DatabaseVersion()
        iCount = 14
        if oVer.check_tables_and_versions([AbstractCard], [
         AbstractCard.tableversion], oConn):
            iCount += AbstractCard.select(connection=oConn).count()
        elif oVer.check_tables_and_versions([AbstractCard], [5], oConn):
            iCount += AbstractCard_v5.select(connection=oConn).count()
        if oVer.check_tables_and_versions([PhysicalCard], [
         PhysicalCard.tableversion], oConn):
            iCount += PhysicalCard.select(connection=oConn).count()
        elif oVer.check_tables_and_versions([PhysicalCard], [2], oConn):
            iCount += PhysicalCard_v2.select(connection=oConn).count()
        if oVer.check_tables_and_versions([PhysicalCardSet], [
         PhysicalCardSet.tableversion], oConn):
            iCount += PhysicalCardSet.select(connection=oConn).count()
        elif oVer.check_tables_and_versions([PhysicalCardSet], [6], oConn):
            iCount += PhysicalCardSet.select(connection=oConn).count()
        return iCount

    def cur_database_count(self, oConn):
        """Current number of items in the database."""
        return 14 + self._get_card_counts(oConn)

    def _upgrade_metadata(self, oOrigConn, oTrans, oVer):
        """Upgrade Metadata table"""
        aMessages = []
        if oVer.check_tables_and_versions([Metadata], [-1], oOrigConn):
            aMessages = [
             'Incomplete information to fill the Metadata table. You will need to reimport the cardlist information.']
        elif oVer.check_tables_and_versions([Metadata], [1], oOrigConn):
            for oObj in Metadata_v1.select(connection=oOrigConn):
                oCopy = Metadata(id=oObj.id, dataKey=oObj.key, value=oObj.value, connection=oTrans)

        else:
            return (
             False, ['Unknown Version for Metadata'])
        return (
         True, aMessages)

    def _upgrade_expansion(self, oOrigConn, oTrans, oVer):
        """Copy Expansion, updating as needed"""
        aMessages = []
        if oVer.check_tables_and_versions([Expansion], [3], oOrigConn):
            aMessages.append('Missing date information for expansions. You will need to reimport the card list for these to be correct')
            for oObj in Expansion_v3.select(connection=oOrigConn):
                oCopy = Expansion(id=oObj.id, name=oObj.name, shortname=oObj.shortname, connection=oTrans)
                _oPrint = Printing(expansionID=oCopy.id, name=None, connection=oTrans)

        elif oVer.check_tables_and_versions([Expansion], [4], oOrigConn):
            for oObj in Expansion_v4.select(connection=oOrigConn):
                oCopy = Expansion(id=oObj.id, name=oObj.name, shortname=oObj.shortname, connection=oTrans)
                oPrint = Printing(expansionID=oCopy.id, name=None, connection=oTrans)
                if oObj.releasedate:
                    sDateVal = 'Release Date: %s' % oObj.releasedate.strftime('%Y-%m-%d')
                    try:
                        oPrintDate = PrintingProperty.byCanonicalValue(sDateVal.lower(), connection=oTrans)
                    except SQLObjectNotFound:
                        oPrintDate = PrintingProperty(value=sDateVal, canonicalValue=sDateVal.lower(), connection=oTrans)

                    oPrint.addPrintingProperty(oPrintDate)

        else:
            return (
             False, ['Unknown Expansion Version'])
        return (
         True, aMessages)

    def _upgrade_printing(self, oOrigConn, _oTrans, oVer):
        """Upgrade printing table."""
        aMessages = []
        if oVer.check_tables_and_versions([Printing], [-1], oOrigConn):
            aMessages = [
             'Incomplete information to fill the Printing table. You will need to reimport the cardlist information.']
        else:
            return (
             False, ['Unknown Version for Printing'])
        return (
         True, aMessages)

    def _upgrade_lookup_hints(self, oOrigConn, oTrans, oVer):
        """Create lookup hints table in the case of v3 Expansion data"""
        aMessages = []
        if oVer.check_tables_and_versions([Expansion], [3, 4], oOrigConn) and oVer.check_tables_and_versions([LookupHints], [
         -1], oOrigConn):
            aMessages = [
             'Incomplete information to fill the LookupHints table. You will need to reimport the cardlist information.']
            for oObj in Rarity.select(connection=oOrigConn):
                _oEntry = LookupHints(domain='Rarities', lookup=oObj.name, value=oObj.name, connection=oTrans)
                if oObj.name != oObj.shortname:
                    _oEntry = LookupHints(domain='Rarities', lookup=oObj.shortname, value=oObj.name, connection=oTrans)

            for oObj in CardType.select(connection=oOrigConn):
                _oEntry = LookupHints(domain='CardTypes', lookup=oObj.name, value=oObj.name, connection=oTrans)

            for oObj in Expansion_v3.select(connection=oOrigConn):
                _oEntry = LookupHints(domain='Expansions', lookup=oObj.name, value=oObj.name, connection=oTrans)
                if oObj.name != oObj.shortname:
                    _oEntry = LookupHints(domain='Expansions', lookup=oObj.shortname, value=oObj.name, connection=oTrans)

        else:
            return super(DBUpgradeManager, self)._upgrade_lookup_hints(oOrigConn, oTrans, oVer)
        return (
         True, aMessages)

    def _copy_discipline(self, oOrigConn, oTrans):
        """Copy Discipline, assuming versions match"""
        for oObj in Discipline.select(connection=oOrigConn):
            _oCopy = Discipline(id=oObj.id, name=oObj.name, fullname=oObj.fullname, connection=oTrans)

    def _copy_old_discipline(self, oOrigConn, oTrans, oVer):
        """Copy disciplines, upgrading as needed."""
        if oVer.check_tables_and_versions([Discipline], [
         Discipline.tableversion], oOrigConn):
            self._copy_discipline(oOrigConn, oTrans)
        else:
            return (
             False, ['Unknown Discipline version'])
        return (
         True, [])

    def _copy_clan(self, oOrigConn, oTrans):
        """Copy Clan, assuming database versions match"""
        for oObj in Clan.select(connection=oOrigConn):
            _oCopy = Clan(id=oObj.id, name=oObj.name, shortname=oObj.shortname, connection=oTrans)

    def _copy_old_clan(self, oOrigConn, oTrans, oVer):
        """Copy clan, upgrading as needed."""
        if oVer.check_tables_and_versions([Clan], [Clan.tableversion], oOrigConn):
            self._copy_clan(oOrigConn, oTrans)
        else:
            return (
             False, ['Unknown Clan Version'])
        return (
         True, [])

    def _copy_creed(self, oOrigConn, oTrans):
        """Copy Creed, assuming versions match"""
        for oObj in Creed.select(connection=oOrigConn):
            _oCopy = Creed(id=oObj.id, name=oObj.name, shortname=oObj.shortname, connection=oTrans)

    def _copy_old_creed(self, oOrigConn, oTrans, oVer):
        """Copy Creed, updating if needed"""
        if oVer.check_tables_and_versions([Creed], [Creed.tableversion], oOrigConn):
            self._copy_creed(oOrigConn, oTrans)
        else:
            return (
             False, ['Unknown Creed Version'])
        return (
         True, [])

    def _copy_virtue(self, oOrigConn, oTrans):
        """Copy Virtue, assuming versions match"""
        for oObj in Virtue.select(connection=oOrigConn):
            _oCopy = Virtue(id=oObj.id, name=oObj.name, fullname=oObj.fullname, connection=oTrans)

    def _copy_old_virtue(self, oOrigConn, oTrans, oVer):
        """Copy Virtue, updating if needed"""
        if oVer.check_tables_and_versions([Virtue], [Virtue.tableversion], oOrigConn):
            self._copy_virtue(oOrigConn, oTrans)
        else:
            return (
             False, ['Unknown Virtue Version'])
        return (
         True, [])

    def _copy_discipline_pair(self, oOrigConn, oTrans):
        """Copy DisciplinePair, assuming versions match"""
        for oObj in DisciplinePair.select(connection=oOrigConn):
            oObj._connection = oOrigConn
            _oCopy = DisciplinePair(id=oObj.id, level=oObj.level, discipline=oObj.discipline, connection=oTrans)

    def _copy_old_discipline_pair(self, oOrigConn, oTrans, oVer):
        """Copy DisciplinePair, upgrading if needed"""
        if oVer.check_tables_and_versions([DisciplinePair], [
         DisciplinePair.tableversion], oOrigConn):
            self._copy_discipline_pair(oOrigConn, oTrans)
        else:
            return (
             False, ['Unknown Discipline Version'])
        return (
         True, [])

    def _copy_old_rarity_pair(self, oOrigConn, oTrans, oVer):
        """Copy RarityPair, upgrading as needed"""
        if oVer.check_tables_and_versions([RarityPair], [
         RarityPair.tableversion], oOrigConn):
            if oVer.check_tables_and_versions([Expansion], [
             Expansion.tableversion], oOrigConn):
                self._copy_rarity_pair(oOrigConn, oTrans)
            elif oVer.check_tables_and_versions([Expansion], [3], oOrigConn):
                for oObj in RarityPair_Ev3.select(connection=oOrigConn):
                    oObj._connection = oOrigConn
                    _oCopy = RarityPair(id=oObj.id, expansionID=oObj.expansion.id, rarityID=oObj.rarity.id, connection=oTrans)

            elif oVer.check_tables_and_versions([Expansion], [4], oOrigConn):
                for oObj in RarityPair_Ev4.select(connection=oOrigConn):
                    oObj._connection = oOrigConn
                    _oCopy = RarityPair(id=oObj.id, expansionID=oObj.expansion.id, rarityID=oObj.rarity.id, connection=oTrans)

            else:
                return (
                 False, ['Unknown Expansion version in RarityPair'])
        else:
            return (
             False, ['Unknown RarityPair version'])
        return (
         True, [])

    def _copy_sect(self, oOrigConn, oTrans):
        """Copy Sect, assuming versions match"""
        for oObj in Sect.select(connection=oOrigConn):
            _oCopy = Sect(id=oObj.id, name=oObj.name, connection=oTrans)

    def _copy_old_sect(self, oOrigConn, oTrans, oVer):
        """Copy Sect, updating if needed"""
        if oVer.check_tables_and_versions([Sect], [Sect.tableversion], oOrigConn):
            self._copy_sect(oOrigConn, oTrans)
        else:
            return (
             False, ['Unknown Sect Version'])
        return (
         True, [])

    def _copy_title(self, oOrigConn, oTrans):
        """Copy Title, assuming versions match"""
        for oObj in Title.select(connection=oOrigConn):
            _oCopy = Title(id=oObj.id, name=oObj.name, connection=oTrans)

    def _copy_old_title(self, oOrigConn, oTrans, oVer):
        """Copy Title, updating if needed"""
        if oVer.check_tables_and_versions([Title], [Title.tableversion], oOrigConn):
            self._copy_title(oOrigConn, oTrans)
        else:
            return (
             False, ['Unknown Title Version'])
        return (
         True, [])

    def drop_old_tables(self, _oConn):
        """Nothing to drop on the upgrade from 0.8"""
        return True

    def _make_abs_card(self, oOldCard, oTrans):
        """Copy SutekhAbstractCard, assuming versions match"""
        oCardCopy = SutekhAbstractCard(id=oOldCard.id, canonicalName=oOldCard.canonicalName, name=oOldCard.name, text=oOldCard.text, search_text=oOldCard.search_text, connection=oTrans)
        oCardCopy.group = oOldCard.group
        oCardCopy.capacity = oOldCard.capacity
        oCardCopy.cost = oOldCard.cost
        oCardCopy.costtype = oOldCard.costtype
        oCardCopy.level = oOldCard.level
        oCardCopy.life = oOldCard.life
        for oData in oOldCard.discipline:
            oCardCopy.addDisciplinePair(oData)

        for oData in oOldCard.clan:
            oCardCopy.addClan(oData)

        for oData in oOldCard.sect:
            oCardCopy.addSect(oData)

        for oData in oOldCard.title:
            oCardCopy.addTitle(oData)

        for oData in oOldCard.creed:
            oCardCopy.addCreed(oData)

        for oData in oOldCard.virtue:
            oCardCopy.addVirtue(oData)

        return oCardCopy

    def _upgrade_abstract_card(self, oOrigConn, oTrans, oLogger, oVer):
        """Copy AbstractCard, upgrading as needed"""
        aMessages = []
        if oVer.check_tables_and_versions([AbstractCard], [5], oOrigConn):
            oTempConn = sqlhub.processConnection
            sqlhub.processConnection = oTrans
            sqlhub.processConnection = oTempConn
            for oCard in AbstractCard_v5.select(connection=oOrigConn).orderBy('id'):
                oCard._connection = oOrigConn
                oCardCopy = SutekhAbstractCard(id=oCard.id, canonicalName=oCard.canonicalName, name=oCard.name, text=oCard.text, connection=oTrans)
                oCardCopy.group = oCard.group
                oCardCopy.capacity = oCard.capacity
                oCardCopy.cost = oCard.cost
                oCardCopy.costtype = oCard.costtype
                oCardCopy.level = oCard.level
                oCardCopy.life = oCard.life
                oCardCopy.search_text = strip_braces(oCard.text)
                for oData in oCard.rarity:
                    oCardCopy.addRarityPair(oData)

                for oData in oCard.discipline:
                    oCardCopy.addDisciplinePair(oData)

                for oData in oCard.rulings:
                    oCardCopy.addRuling(oData)

                for oData in oCard.clan:
                    oCardCopy.addClan(oData)

                for oData in oCard.cardtype:
                    oCardCopy.addCardType(oData)

                for oData in oCard.sect:
                    oCardCopy.addSect(oData)

                for oData in oCard.title:
                    oCardCopy.addTitle(oData)

                for oData in oCard.creed:
                    oCardCopy.addCreed(oData)

                for oData in oCard.virtue:
                    oCardCopy.addVirtue(oData)

                for oData in oCard.keywords:
                    oCardCopy.addKeyword(oData)

                for oData in oCard.artists:
                    oCardCopy.addArtist(oData)

                oCardCopy.syncUpdate()
                oCardCopy._parent.syncUpdate()
                oLogger.info('copied AC %s', oCardCopy.name)

        elif oVer.check_tables_and_versions([AbstractCard], [6], oOrigConn):
            oTempConn = sqlhub.processConnection
            sqlhub.processConnection = oTrans
            sqlhub.processConnection = oTempConn
            for oCard in AbstractCard_v6.select(connection=oOrigConn).orderBy('id'):
                oCard._connection = oOrigConn
                oCardCopy = SutekhAbstractCard(id=oCard.id, canonicalName=oCard.canonicalName, name=oCard.name, text=oCard.text, connection=oTrans)
                oCardCopy.group = oCard.group
                oCardCopy.capacity = oCard.capacity
                oCardCopy.cost = oCard.cost
                oCardCopy.costtype = oCard.costtype
                oCardCopy.level = oCard.level
                oCardCopy.life = oCard.life
                oCardCopy.search_text = oCard.search_text
                for oData in oCard.rarity:
                    oCardCopy.addRarityPair(oData)

                for oData in oCard.discipline:
                    oCardCopy.addDisciplinePair(oData)

                for oData in oCard.rulings:
                    oCardCopy.addRuling(oData)

                for oData in oCard.clan:
                    oCardCopy.addClan(oData)

                for oData in oCard.cardtype:
                    oCardCopy.addCardType(oData)

                for oData in oCard.sect:
                    oCardCopy.addSect(oData)

                for oData in oCard.title:
                    oCardCopy.addTitle(oData)

                for oData in oCard.creed:
                    oCardCopy.addCreed(oData)

                for oData in oCard.virtue:
                    oCardCopy.addVirtue(oData)

                for oData in oCard.keywords:
                    oCardCopy.addKeyword(oData)

                for oData in oCard.artists:
                    oCardCopy.addArtist(oData)

                oCardCopy.syncUpdate()
                oCardCopy._parent.syncUpdate()
                oLogger.info('copied AC %s', oCardCopy.name)

        else:
            return (
             False, ['Unknown AbstractCard version'])
        return (
         True, aMessages)

    def _upgrade_physical_card(self, oOrigConn, oTrans, oLogger, oVer):
        """Copy PhysicalCards, upgrading if needed."""
        aMessages = []
        if not oVer.check_table_in_versions(PhysicalCard, [
         2, PhysicalCard.tableversion], oOrigConn):
            return (False, ['Unknown PhysicalCard version'])
        if oVer.check_tables_and_versions([AbstractCard], [5], oOrigConn):
            for oCard in PhysicalCard_ACv5.select(connection=oOrigConn).orderBy('id'):
                oPrintingID = _lookup_printing_for_exp(oCard.expansionID, oTrans)
                oCardCopy = PhysicalCard(id=oCard.id, abstractCardID=oCard.abstractCardID, printingID=oPrintingID, connection=oTrans)
                oCardCopy.syncUpdate()
                oLogger.info('copied PC %s', oCardCopy.id)

        elif oVer.check_tables_and_versions([AbstractCard], [6], oOrigConn):
            for oCard in PhysicalCard_ACv6.select(connection=oOrigConn).orderBy('id'):
                oPrintingID = _lookup_printing_for_exp(oCard.expansionID, oTrans)
                oCardCopy = PhysicalCard(id=oCard.id, abstractCardID=oCard.abstractCardID, printingID=oPrintingID, connection=oTrans)
                oCardCopy.syncUpdate()
                oLogger.info('copied PC %s', oCardCopy.id)

        elif oVer.check_tables_and_versions([PhysicalCard], [2], oOrigConn):
            for oCard in PhysicalCard_v2.select(connection=oOrigConn).orderBy('id'):
                oPrintingID = _lookup_printing_for_exp(oCard.expansionID, oTrans)
                oCardCopy = PhysicalCard(id=oCard.id, abstractCardID=oCard.abstractCardID, printingID=oPrintingID, connection=oTrans)
                oCardCopy.syncUpdate()
                oLogger.info('copied PC %s', oCardCopy.id)

        else:
            return (
             False, ['Unknown PhysicalCard version'])
        return (
         True, aMessages)

    def _copy_old_pcs_loop(self, oOrigConn, oTrans, oLogger):
        """Loop over the old card sets, copying them to the new database."""
        aSets = list(PhysicalCardSet_PCv3.select(connection=oOrigConn))
        self._copy_physical_card_set_loop(aSets, oTrans, oOrigConn, oLogger)

    def _upgrade_physical_card_set(self, oOrigConn, oTrans, oLogger, oVer):
        """Copy PCS, upgrading as needed."""
        aMessages = []
        if oVer.check_tables_and_versions([PhysicalCardSet, PhysicalCard], [
         6, 2], oOrigConn):
            self._copy_old_pcs_loop(oOrigConn, oTrans, oLogger)
        elif oVer.check_tables_and_versions([PhysicalCardSet, PhysicalCard], [
         PhysicalCardSet.tableversion, 2], oOrigConn):
            self._copy_old_pcs_loop(oOrigConn, oTrans, oLogger)
        else:
            return (
             False, ['Unknown PhysicalCardSet version'])
        return (
         True, aMessages)