# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/core/BaseDatabaseUpgrade.py
# Compiled at: 2019-12-11 16:37:48
"""Handles the heavy lifting of upgrading the database.

   Holds methods to copy database contents around, utility classes
   to talk to old database versions, and so forth.

   We only support upgrading from the previous stable version
   (currently 0.8)
   """
from logging import Logger
from sqlobject import sqlhub, connectionForURI, SQLObjectNotFound
from .BaseTables import PhysicalCard, AbstractCard, PhysicalCardSet, Expansion, Rarity, RarityPair, CardType, Ruling, Keyword, Artist, Metadata, LookupHints, Printing, PrintingProperty
from .DBUtility import flush_cache, refresh_tables
from .BaseDBManagement import UnknownVersion
from .DatabaseVersion import DatabaseVersion

class BaseDBUpgradeManager(object):
    """Convience class to define and manage all the various aspects
       around database upgrades."""
    SUPPORTED_TABLES = {'Rarity': (
                Rarity, (Rarity.tableversion,)), 
       'Expansion': (
                   Expansion, (Expansion.tableversion,)), 
       'CardType': (
                  CardType, (CardType.tableversion,)), 
       'Keyword': (
                 Keyword, (Keyword.tableversion,)), 
       'Artist': (
                Artist, (Artist.tableversion,)), 
       'Ruling': (
                Ruling, (Ruling.tableversion,)), 
       'RarityPair': (
                    RarityPair, (RarityPair.tableversion,)), 
       'AbstractCard': (
                      AbstractCard, (AbstractCard.tableversion,)), 
       'PhysicalCard': (
                      PhysicalCard, (2, PhysicalCard.tableversion)), 
       'PhysicalCardSet': (
                         PhysicalCardSet, (PhysicalCardSet.tableversion,)), 
       'LookupHints': (
                     LookupHints, (-1, LookupHints.tableversion)), 
       'Printing': (
                  Printing, (-1, Printing.tableversion)), 
       'PrintingProperty': (
                          PrintingProperty,
                          (
                           -1, PrintingProperty.tableversion)), 
       'Metadata': (
                  Metadata, (-1, 1, Metadata.tableversion))}
    COPY_OLD_DB = [
     (
      '_copy_old_lookup_hints', 'LookupHints table', False),
     (
      '_copy_old_metadata', 'Metadata table', False),
     (
      '_copy_old_rarity', 'Rarity table', False),
     (
      '_copy_old_expansion', 'Expansion table', False),
     (
      '_copy_old_print_properties', 'PrintingProperty table', False),
     (
      '_copy_old_printing', 'Printing table', False),
     (
      '_copy_old_card_type', 'CardType table', False),
     (
      '_copy_old_ruling', 'Ruling table', False),
     (
      '_copy_old_rarity_pair', 'RarityPair table', False),
     (
      '_copy_old_artist', 'Artist table', False),
     (
      '_copy_old_keyword', 'Keyword table', False),
     (
      '_copy_old_abstract_card', 'AbstractCard table', True),
     (
      '_copy_old_physical_card', 'PhysicalCard table', True),
     (
      '_copy_old_physical_card_set', 'PhysicalCardSet table', True)]
    COPY_DB = [
     (
      '_copy_lookup_hints', 'LookupHints table', False),
     (
      '_copy_metadata', 'Metadata table', False),
     (
      '_copy_rarity', 'Rarity table', False),
     (
      '_copy_expansion', 'Expansion table', False),
     (
      '_copy_print_properties', 'PrintingProperty table', False),
     (
      '_copy_printing', 'Printing table', False),
     (
      '_copy_card_type', 'CardType table', False),
     (
      '_copy_ruling', 'Ruling table', False),
     (
      '_copy_rarity_pair', 'RarityPair table', False),
     (
      '_copy_artist', 'Artist table', False),
     (
      '_copy_keyword', 'Keyword table', False),
     (
      '_copy_abstract_card', 'AbstractCard table', True),
     (
      '_copy_physical_card', 'PhysicalCard table', True),
     (
      '_copy_physical_card_set', 'PhysicalCardSet table', True)]
    cAbstractCardCls = None
    _aTableList = []

    def check_can_read_old_database(self, oConn):
        """Can we upgrade from this database version?
           """
        oVer = DatabaseVersion()
        oVer.expire_cache()
        for sDesc, (oTable, aVersions) in self.SUPPORTED_TABLES.items():
            if not oVer.check_table_in_versions(oTable, aVersions, oConn):
                raise UnknownVersion(sDesc)

        return True

    def old_database_count(self, oConn):
        """Check number of items in old DB for progress bars, etc."""
        raise NotImplementedError('Implement old_database_count')

    def _get_card_counts(self, oConn):
        """Get the count of AbstractCards, PhysicalCards and PhysicalCardSets
           which need to be copied. Helper function for the database
           count"""
        return AbstractCard.select(connection=oConn).count() + PhysicalCard.select(connection=oConn).count() + PhysicalCardSet.select(connection=oConn).count()

    def cur_database_count(self, oConn):
        """Check number of items in upgraded DB for progress bars, etc."""
        raise NotImplementedError('Implement cur_database_count')

    def _copy_rarity(self, oOrigConn, oTrans):
        """Copy rarity tables, assuming same version"""
        for oObj in Rarity.select(connection=oOrigConn):
            _oCopy = Rarity(id=oObj.id, name=oObj.name, shortname=oObj.shortname, connection=oTrans)

    def _copy_old_lookup_hints(self, oOrigConn, oTrans, oVer):
        """Copy lookup table, upgrading versions as needed"""
        if oVer.check_tables_and_versions([LookupHints], [
         LookupHints.tableversion], oOrigConn):
            self._copy_lookup_hints(oOrigConn, oTrans)
        else:
            return self._upgrade_lookup_hints(oOrigConn, oTrans, oVer)
        return (
         True, [])

    def _upgrade_lookup_hints(self, oOrigConn, oTrans, oVer):
        """Upgrade lookup hints table"""
        if oVer.check_tables_and_versions([LookupHints], [-1], oOrigConn):
            aMessages = [
             'Incomplete information to fill the LookupHints table. You will need to reimport the cardlist information.']
            for oObj in Rarity.select(connection=oOrigConn):
                _oEntry = LookupHints(domain='Rarities', lookup=oObj.name, value=oObj.name, connection=oTrans)
                if oObj.name != oObj.shortname:
                    _oEntry = LookupHints(domain='Rarities', lookup=oObj.shortname, value=oObj.name, connection=oTrans)

            for oObj in CardType.select(connection=oOrigConn):
                _oEntry = LookupHints(domain='CardTypes', lookup=oObj.name, value=oObj.name, connection=oTrans)

            for oObj in Expansion.select(connection=oOrigConn):
                _oEntry = LookupHints(domain='Expansions', lookup=oObj.name, value=oObj.name, connection=oTrans)
                if oObj.name != oObj.shortname:
                    _oEntry = LookupHints(domain='Expansions', lookup=oObj.shortname, value=oObj.name, connection=oTrans)

        else:
            return (
             False, ['Unknown Version for LookupHints'])
        return (
         True, aMessages)

    def _copy_old_metadata(self, oOrigConn, oTrans, oVer):
        """Copy Metadata table, upgrading versions as needed"""
        if oVer.check_tables_and_versions([Metadata], [
         Metadata.tableversion], oOrigConn):
            self._copy_metadata(oOrigConn, oTrans)
        else:
            return self._upgrade_metadata(oOrigConn, oTrans, oVer)
        return (
         True, [])

    def _upgrade_metadata(self, oOrigConn, _oTrans, oVer):
        """Upgrade Metadata table"""
        if oVer.check_tables_and_versions([Metadata], [-1], oOrigConn):
            aMessages = [
             'Incomplete information to fill the Metadata table. You will need to reimport the cardlist information.']
        else:
            return (False, ['Unknown Version for Metadata'])
        return (
         True, aMessages)

    def _copy_print_properties(self, oOrigConn, oTrans):
        """Copy Keyword, assuming versions match"""
        for oObj in PrintingProperty.select(connection=oOrigConn):
            _oCopy = PrintingProperty(id=oObj.id, value=oObj.value, canonicalValue=oObj.canonicalValue, connection=oTrans)

    def _copy_old_print_properties(self, oOrigConn, oTrans, oVer):
        """Copy printing data table, upgrading versions as needed"""
        if oVer.check_tables_and_versions([PrintingProperty], [
         PrintingProperty.tableversion], oOrigConn):
            self._copy_print_properties(oOrigConn, oTrans)
        else:
            return self._upgrade_print_properties(oOrigConn, oTrans, oVer)
        return (
         True, [])

    def _upgrade_print_properties(self, oOrigConn, _oTrans, oVer):
        """Upgrade PrintingProperty hints table"""
        if oVer.check_tables_and_versions([PrintingProperty], [-1], oOrigConn):
            aMessages = [
             'Incomplete information to fill the PrintingProperty table. You will need to reimport the cardlist information.']
        else:
            return (False, ['Unknown Version for PrintingProperty'])
        return (
         True, aMessages)

    def _upgrade_printing(self, _oOrigConn, _oTrans, _oVer):
        """Default fail - subclasses should override this
           when needed."""
        return (
         False, ['Unknown Version for Printing'])

    def _copy_printing(self, oOrigConn, oTrans):
        """Copy Printing, assuming versions match"""
        for oObj in Printing.select(connection=oOrigConn):
            oPrintCopy = Printing(id=oObj.id, expansionID=oObj.expansionID, name=oObj.name, connection=oTrans)
            for oData in oObj.properties:
                oPrintCopy.addPrintingProperty(oData)

    def _copy_old_printing(self, oOrigConn, oTrans, oVer):
        """Copy printing table, upgrading versions as needed"""
        if oVer.check_tables_and_versions([Printing], [
         Printing.tableversion], oOrigConn):
            self._copy_printing(oOrigConn, oTrans)
        else:
            return self._upgrade_printing(oOrigConn, oTrans, oVer)
        return (
         True, [])

    def _copy_old_rarity(self, oOrigConn, oTrans, oVer):
        """Copy rarity table, upgrading versions as needed"""
        if oVer.check_tables_and_versions([Rarity], [Rarity.tableversion], oOrigConn):
            self._copy_rarity(oOrigConn, oTrans)
        else:
            return self._upgrade_rarity(oOrigConn, oTrans, oVer)
        return (
         True, [])

    def _upgrade_rarity(self, _oOrigConn, _oTrans, _oVer):
        """Default fail - subclasses should override this
           when needed."""
        return (
         False, ['Unknown Version for Rarity'])

    def _copy_expansion(self, oOrigConn, oTrans):
        """Copy expansion, assuming versions match"""
        for oObj in Expansion.select(connection=oOrigConn):
            _oCopy = Expansion(id=oObj.id, name=oObj.name, shortname=oObj.shortname, connection=oTrans)

    def _copy_old_expansion(self, oOrigConn, oTrans, oVer):
        """Copy Expansion, updating as needed"""
        aMessages = []
        if oVer.check_tables_and_versions([Expansion], [
         Expansion.tableversion], oOrigConn):
            self._copy_expansion(oOrigConn, oTrans)
        else:
            return self._upgrade_expansion(oOrigConn, oTrans, oVer)
        return (
         True, aMessages)

    def _upgrade_expansion(self, _oOrigConn, _oTrans, _oVer):
        """Default fail - subclasses should override this when needed."""
        return (
         False, ['Unknown Expansion Version'])

    def _copy_card_type(self, oOrigConn, oTrans):
        """Copy CardType, assuming versions match"""
        for oObj in CardType.select(connection=oOrigConn):
            _oCopy = CardType(id=oObj.id, name=oObj.name, connection=oTrans)

    def _copy_old_card_type(self, oOrigConn, oTrans, oVer):
        """Copy CardType, upgrading as needed"""
        if oVer.check_tables_and_versions([CardType], [CardType.tableversion], oOrigConn):
            self._copy_card_type(oOrigConn, oTrans)
        else:
            return self._upgrade_card_type(oOrigConn, oTrans, oVer)
        return (
         True, [])

    def _upgrade_card_type(self, _oOrigiConn, _oTrans, _oVer):
        """Default fail - subclasses should upgrade this when
           required."""
        return (
         False, ['Unknown CardType Version'])

    def _copy_ruling(self, oOrigConn, oTrans):
        """Copy Ruling, assuming versions match"""
        for oObj in Ruling.select(connection=oOrigConn):
            _oCopy = Ruling(id=oObj.id, text=oObj.text, code=oObj.code, url=oObj.url, connection=oTrans)

    def _copy_old_ruling(self, oOrigConn, oTrans, oVer):
        """Copy Ruling, upgrading as needed"""
        if oVer.check_tables_and_versions([Ruling], [
         Ruling.tableversion], oOrigConn):
            self._copy_ruling(oOrigConn, oTrans)
        else:
            return self._upgrade_ruling(oOrigConn, oTrans, oVer)
        return (
         True, [])

    def _upgrade_ruling(self, _oOrigConn, _oTrans, _oVer):
        """Upgrade rulings"""
        return (
         False, ['Unknown Ruling Version'])

    def _copy_lookup_hints(self, oOrigConn, oTrans):
        """Copy LookupHints, assuming versions match"""
        for oObj in LookupHints.select(connection=oOrigConn):
            oObj._connection = oOrigConn
            _oCopy = LookupHints(id=oObj.id, domain=oObj.domain, lookup=oObj.lookup, value=oObj.value, connection=oTrans)

    def _copy_metadata(self, oOrigConn, oTrans):
        """Copy Metadata, assuming versions match"""
        for oObj in Metadata.select(connection=oOrigConn):
            oObj._connection = oOrigConn
            _oCopy = Metadata(id=oObj.id, dataKey=oObj.dataKey, value=oObj.value, connection=oTrans)

    def _copy_rarity_pair(self, oOrigConn, oTrans):
        """Copy RairtyPair, assuming versions match"""
        for oObj in RarityPair.select(connection=oOrigConn):
            oObj._connection = oOrigConn
            _oCopy = RarityPair(id=oObj.id, expansion=oObj.expansion, rarity=oObj.rarity, connection=oTrans)

    def _copy_old_rarity_pair(self, oOrigConn, oTrans, oVer):
        """Copy RarityPair, upgrading as needed"""
        if oVer.check_tables_and_versions([RarityPair, Expansion], [
         RarityPair.tableversion,
         Expansion.tableversion], oOrigConn):
            self._copy_rarity_pair(oOrigConn, oTrans)
        else:
            return self._upgrade_rarity_pair(oOrigConn, oTrans, oVer)
        return (
         True, [])

    def _upgrade_rarity_pair(self, _oOrigConn, _oTrans, _oVer):
        """Default fail - subclasses should implement this as
           required"""
        return (
         False, ['Unknown RarityPair version'])

    def _copy_keyword(self, oOrigConn, oTrans):
        """Copy Keyword, assuming versions match"""
        for oObj in Keyword.select(connection=oOrigConn):
            _oCopy = Keyword(id=oObj.id, keyword=oObj.keyword, connection=oTrans)

    def _copy_old_keyword(self, oOrigConn, oTrans, oVer):
        """Copy Keyword, updating if needed"""
        if oVer.check_tables_and_versions([Keyword], [Keyword.tableversion], oOrigConn):
            self._copy_keyword(oOrigConn, oTrans)
        else:
            return self._upgrade_keyword(oOrigConn, oTrans, oVer)
        return (
         True, [])

    def _upgrade_keyword(self, _oOrigConn, _oTrans, _oVer):
        """Default fail - subclasses should implement this as
           required"""
        return (
         False, ['Unknown Keyword Version'])

    def _copy_artist(self, oOrigConn, oTrans):
        """Copy Artist, assuming versions match"""
        for oObj in Artist.select(connection=oOrigConn):
            _oCopy = Artist(id=oObj.id, canonicalName=oObj.canonicalName, name=oObj.name, connection=oTrans)

    def _copy_old_artist(self, oOrigConn, oTrans, oVer):
        """Copy Artist, updating if needed"""
        if oVer.check_tables_and_versions([Artist], [Artist.tableversion], oOrigConn):
            self._copy_artist(oOrigConn, oTrans)
        else:
            return self._upgrade_artist(oOrigConn, oTrans, oVer)
        return (
         True, [])

    def _upgrade_artist(self, _oOrigConn, _oTrans, _oVer):
        """Default fail - subclasses should implement this as
           required"""
        return (
         False, ['Unknown Artist Version'])

    def _copy_abstract_card(self, oOrigConn, oTrans, oLogger):
        """Copy AbstractCard, assuming versions match"""
        for oCard in self.cAbstractCardCls.select(connection=oOrigConn).orderBy('id'):
            oCard._connection = oOrigConn
            oCard._parent._connection = oOrigConn
            oCardCopy = self._make_abs_card(oCard, oTrans)
            for oData in oCard.rarity:
                oCardCopy.addRarityPair(oData)

            for oData in oCard.cardtype:
                oCardCopy.addCardType(oData)

            for oData in oCard.rulings:
                oCardCopy.addRuling(oData)

            for oData in oCard.artists:
                oCardCopy.addArtist(oData)

            for oData in oCard.keywords:
                oCardCopy.addKeyword(oData)

            oCardCopy.syncUpdate()
            oCardCopy._parent.syncUpdate()
            oLogger.info('copied AC %s', oCardCopy.name)

    def _make_abs_card(self, oOldCard, oTrans):
        """Copy the details of the old card to a new card."""
        raise NotImplementedError('Implement _make_abs_card')

    def _copy_old_abstract_card(self, oOrigConn, oTrans, oLogger, oVer):
        """Copy AbstractCard, upgrading as needed"""
        aMessages = []
        if oVer.check_tables_and_versions([
         AbstractCard, self.cAbstractCardCls], [
         AbstractCard.tableversion,
         self.cAbstractCardCls.tableversion], oOrigConn):
            self._copy_abstract_card(oOrigConn, oTrans, oLogger)
        else:
            return self._upgrade_abstract_card(oOrigConn, oTrans, oLogger, oVer)
        return (
         True, aMessages)

    def _upgrade_abstract_card(self, _oOrigConn, _oTrans, _oLogger, _oVer):
        """Default fail - subclasses should implement this as
           required"""
        return (
         False, ['Unknown AbstractCard version'])

    def _copy_physical_card(self, oOrigConn, oTrans, oLogger):
        """Copy PhysicalCard, assuming version match"""
        for oCard in PhysicalCard.select(connection=oOrigConn).orderBy('id'):
            oCardCopy = PhysicalCard(id=oCard.id, abstractCardID=oCard.abstractCardID, printingID=oCard.printingID, connection=oTrans)
            oLogger.info('copied PC %s', oCardCopy.id)

    def _copy_old_physical_card(self, oOrigConn, oTrans, oLogger, oVer):
        """Copy PhysicalCards, upgrading if needed."""
        aMessages = []
        if oVer.check_tables_and_versions([PhysicalCard, AbstractCard], [
         PhysicalCard.tableversion,
         AbstractCard.tableversion], oOrigConn):
            self._copy_physical_card(oOrigConn, oTrans, oLogger)
        else:
            return self._upgrade_physical_card(oOrigConn, oTrans, oLogger, oVer)
        return (
         True, aMessages)

    def _upgrade_physical_card(self, _oOrigConn, _oTrans, _oLogger, _oVer):
        """Default fail - subclasses should implement this as
           required"""
        return (
         False, ['Unknown PhysicalCard version'])

    def _copy_physical_card_set_loop(self, aSets, oTrans, oOrigConn, oLogger):
        """Central loop for copying card sets.

           Copy the list of card sets in aSet, ensuring we copy parents before
           children."""
        bDone = False
        dDone = {}
        for oSet in aSets:
            oSet._connection = oOrigConn

        while not bDone:
            aToDo = []
            for oSet in aSets:
                if oSet.parent is None or oSet.parent.id in dDone:
                    if oSet.parent:
                        oParent = dDone[oSet.parent.id]
                    else:
                        oParent = None
                    oCopy = PhysicalCardSet(name=oSet.name, author=oSet.author, comment=oSet.comment, annotations=oSet.annotations, inuse=oSet.inuse, parent=oParent, connection=oTrans)
                    for oCard in oSet.cards:
                        oCopy.addPhysicalCard(oCard.id)

                    oCopy.syncUpdate()
                    oLogger.info('Copied PCS %s', oCopy.name)
                    dDone[oSet.id] = oCopy
                else:
                    aToDo.append(oSet)

            if not aToDo:
                bDone = True
            else:
                aSets = aToDo
            oTrans.commit()

        return

    def _copy_physical_card_set(self, oOrigConn, oTrans, oLogger):
        """Copy PCS, assuming versions match"""
        aSets = list(PhysicalCardSet.select(connection=oOrigConn))
        self._copy_physical_card_set_loop(aSets, oTrans, oOrigConn, oLogger)

    def _copy_old_physical_card_set(self, oOrigConn, oTrans, oLogger, oVer):
        """Copy PCS, upgrading as needed."""
        aMessages = []
        if oVer.check_tables_and_versions([PhysicalCardSet, PhysicalCard], [
         PhysicalCardSet.tableversion,
         PhysicalCard.tableversion], oOrigConn):
            self._copy_physical_card_set(oOrigConn, oTrans, oLogger)
        else:
            return self._upgrade_physical_card_set(oOrigConn, oTrans, oLogger, oVer)
        return (
         True, aMessages)

    def _upgrade_physical_card_set(self, _oOrigConn, _oTrans, _oLogger, _oVer):
        """Default fail - subclasses should implement this as
           required"""
        return (
         False, ['Unknown PhysicalCardSet version'])

    def read_old_database(self, oOrigConn, oDestConnn, oLogHandler=None):
        """Read the old database into new database, filling in
           blanks when needed"""
        try:
            if not self.check_can_read_old_database(oOrigConn):
                return (False, ['Unable to read database'])
        except UnknownVersion as oExp:
            raise oExp

        oLogger = Logger('read Old DB')
        if oLogHandler:
            oLogger.addHandler(oLogHandler)
            if hasattr(oLogHandler, 'set_total'):
                oLogHandler.set_total(self.old_database_count(oOrigConn))
        aMessages = []
        bRes = True
        oTrans = oDestConnn.transaction()
        oVer = DatabaseVersion()
        for sCopyFunc, sName, bPassLogger in self.COPY_OLD_DB:
            fCopy = getattr(self, sCopyFunc)
            try:
                if bPassLogger:
                    bOK, aNewMessages = fCopy(oOrigConn, oTrans, oLogger, oVer)
                else:
                    bOK, aNewMessages = fCopy(oOrigConn, oTrans, oVer)
            except SQLObjectNotFound as oExp:
                bOK = False
                aNewMessages = ['Unable to copy %s: Error %s' % (sName, oExp)]
            else:
                if not bPassLogger:
                    oLogger.info('%s copied', sName)
                bRes = bRes and bOK
                aMessages.extend(aNewMessages)
                oTrans.commit()
                oTrans.cache.clear()

        oTrans.commit(close=True)
        return (bRes, aMessages)

    def drop_old_tables(self, _oConn):
        """Drop tables which are no longer used from the database.
           Needed for postgres and other such things."""
        raise NotImplementedError('implement drop_old_tables')

    def copy_database(self, oOrigConn, oDestConnn, oLogHandler=None):
        """Copy the database, with no attempts to upgrade.

           This is a straight copy, with no provision for funky stuff
           Compatability of database structures is assumed, but not checked.
           """
        flush_cache()
        oVer = DatabaseVersion()
        oVer.expire_cache()
        oLogger = Logger('copy DB')
        if oLogHandler:
            oLogger.addHandler(oLogHandler)
            if hasattr(oLogHandler, 'set_total'):
                oLogHandler.set_total(self.cur_database_count(oOrigConn))
        bRes = True
        aMessages = []
        oTrans = oDestConnn.transaction()
        for sCopyFunc, sName, bPassLogger in self.COPY_DB:
            fCopy = getattr(self, sCopyFunc)
            try:
                if bRes:
                    if bPassLogger:
                        fCopy(oOrigConn, oTrans, oLogger)
                    else:
                        fCopy(oOrigConn, oTrans)
            except SQLObjectNotFound as oExp:
                bRes = False
                aMessages.append('Unable to copy %s: Aborting with error: %s' % (
                 sName, oExp))
            else:
                oTrans.commit()
                oTrans.cache.clear()
                if not bPassLogger:
                    oLogger.info('%s copied', sName)

        flush_cache()
        oTrans.commit(close=True)
        return (
         bRes, aMessages)

    def create_memory_copy(self, oTempConn, oLogHandler=None):
        """Create a temporary copy of the database in memory.

          We create a temporary memory database, and create the updated
          database in it. read_old_database is responsbile for upgrading
          stuff as needed
          """
        if refresh_tables(self._aTableList, oTempConn, False):
            bRes, aMessages = self.read_old_database(sqlhub.processConnection, oTempConn, oLogHandler)
            oVer = DatabaseVersion()
            oVer.expire_cache()
            return (
             bRes, aMessages)
        return (
         False, ['Unable to create tables'])

    def create_final_copy(self, oTempConn, oLogHandler=None):
        """Copy from the memory database to the real thing"""
        if not self.drop_old_tables(sqlhub.processConnection):
            return (False, ['Unable to cleanup database'])
        if refresh_tables(self._aTableList, sqlhub.processConnection):
            return self.copy_database(oTempConn, sqlhub.processConnection, oLogHandler)
        return (
         False, ['Unable to create tables'])

    def attempt_database_upgrade(self, oLogHandler=None):
        """Attempt to upgrade the database,
           going via a temporary memory copy."""
        oTempConn = connectionForURI('sqlite:///:memory:')
        oLogger = Logger('attempt upgrade')
        if oLogHandler:
            oLogger.addHandler(oLogHandler)
        bOK, aMessages = self.create_memory_copy(oTempConn, oLogHandler)
        if bOK:
            oLogger.info('Copied database to memory, performing upgrade.')
            if aMessages:
                oLogger.info('Messages reported: %s', aMessages)
            bOK, aMessages = self.create_final_copy(oTempConn, oLogHandler)
            if bOK:
                oLogger.info('Everything seems to have gone OK')
                if aMessages:
                    oLogger.info('Messages reported %s', aMessages)
                return True
            oLogger.critical('Unable to perform upgrade.')
            if aMessages:
                oLogger.error('Errors reported: %s', aMessages)
            oLogger.critical('!!YOUR DATABASE MAY BE CORRUPTED!!')
        else:
            oLogger.error('Unable to create memory copy. Database not upgraded.')
            if aMessages:
                oLogger.error('Errors reported %s', aMessages)
        return False