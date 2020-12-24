# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/io/BaseZipFileWrapper.py
# Compiled at: 2019-12-11 16:37:52
"""Provide a ZipFile class which wraps the functionlity from zipfile
   Sutekh needs."""
import zipfile, datetime
from StringIO import StringIO
from logging import Logger
from sqlobject import sqlhub
from ..core.BaseTables import PhysicalCardSet, PHYSICAL_SET_LIST
from ..core.BaseAdapters import IPhysicalCardSet
from ..core.CardLookup import DEFAULT_LOOKUP
from ..core.CardSetHolder import CachedCardSetHolder, CardSetWrapper
from ..core.DBUtility import refresh_tables
from ..core.CardSetUtilities import check_cs_exists

def parse_string(oParser, sIn, oHolder):
    """Utility function for reading zip files.

       Allows oParser.parse to be called on a string."""
    oFile = StringIO(sIn)
    oParser.parse(oFile, oHolder)


def write_string(oWriter, oPCSet):
    """Utility function.

       Generate a string from the Writer."""
    oHolder = CardSetWrapper(oPCSet)
    oFile = StringIO()
    oWriter.write(oFile, oHolder)
    oString = oFile.getvalue()
    oFile.close()
    return oString


class ZipEntryProxy(StringIO, object):
    """A proxy that provides a suitable open method so
       these can be passed to the card reading routines."""

    def open(self):
        """Reset to the start of the file."""
        self.seek(0)
        return self


class BaseZipFileWrapper(object):
    """The zip file wrapper.

       This provides useful functions for dumping + extracting the
       database to / form a zipfile"""

    def __init__(self, sZipFileName):
        self.sZipFileName = sZipFileName
        self.oZip = None
        self._aWarnings = []
        self._bForceReparent = False
        self._cWriter = None
        self._cIdentifyFile = None
        return

    def _open_zip_for_write(self):
        """Open zip file to be written"""
        self.oZip = zipfile.ZipFile(self.sZipFileName, 'w')

    def _open_zip_for_read(self):
        """Open zip file to be read"""
        self.oZip = zipfile.ZipFile(self.sZipFileName, 'r')

    def _close_zip(self):
        """Close the zip file and clean up"""
        self.oZip.close()
        self.oZip = None
        return

    def _write_pcs_list_to_zip(self, aPCSList, oLogger):
        """Write the given list of card sets to the zip file"""
        bClose = False
        tTime = datetime.datetime.now().timetuple()
        if self.oZip is None:
            self._open_zip_for_write()
            bClose = True
        aList = []
        for oPCSet in aPCSList:
            sZName = oPCSet.name
            oWriter = self._cWriter()
            oString = write_string(oWriter, oPCSet)
            sZName = sZName.replace(' ', '_')
            sZName = sZName.replace('/', '_')
            sZipName = '%s.xml' % sZName
            sZipName = sZipName.encode('ascii', 'xmlcharrefreplace')
            aList.append(sZipName)
            oInfoObj = zipfile.ZipInfo(sZipName, tTime)
            oInfoObj.external_attr = 25165824
            oInfoObj.compress_type = zipfile.ZIP_DEFLATED
            self.oZip.writestr(oInfoObj, oString)
            oLogger.info('PCS: %s written', oPCSet.name)

        if bClose:
            self._close_zip()
        return aList

    def do_restore_from_zip(self, oCardLookup=DEFAULT_LOOKUP, oLogHandler=None):
        """Recover data from the zip file"""
        self._aWarnings = []
        bTablesRefreshed = False
        self._bForceReparent = False
        self._open_zip_for_read()
        oLogger = Logger('Restore zip file')
        if oLogHandler is not None:
            oLogger.addHandler(oLogHandler)
            if hasattr(oLogHandler, 'set_total'):
                oLogHandler.set_total(len(self.oZip.infolist()))
        oIdParser = self._cIdentifyFile()
        for oItem in self.oZip.infolist():
            oData = self.oZip.read(oItem.filename)
            oIdParser.parse_string(oData)
            if not bTablesRefreshed and self._check_refresh(oIdParser):
                refresh_tables(PHYSICAL_SET_LIST, sqlhub.processConnection)
                bTablesRefreshed = True
            if self._should_force_reparent(oIdParser):
                self._bForceReparent = True

        if not bTablesRefreshed:
            raise IOError('No valid card sets found in the zip file.')
        dLookupCache = {}
        aToRead = self.oZip.infolist()
        while aToRead:
            aToRead = self.read_items(aToRead, oCardLookup, oLogger, dLookupCache)

        self._close_zip()
        return

    def read_items(self, aList, oCardLookup, oLogger, dLookupCache):
        """Read a list of CardSet items from the card list, reaturning
           a list of those that couldn't be read because their parents
           weren't read first"""
        aToRead = []
        oIdParser = self._cIdentifyFile()
        oOldConn = sqlhub.processConnection
        oTrans = oOldConn.transaction()
        sqlhub.processConnection = oTrans
        for oItem in aList:
            bReparent = False
            oData = self.oZip.read(oItem.filename)
            oIdParser.parse_string(oData)
            if not oIdParser.can_parse():
                continue
            if not oIdParser.parent_exists:
                aToRead.append(oItem)
                continue
            if self._check_forced_reparent(oIdParser):
                if check_cs_exists('My Collection'):
                    bReparent = True
                else:
                    aToRead.append(oItem)
                    continue
            oParser = oIdParser.get_parser()
            oHolder = CachedCardSetHolder()
            parse_string(oParser, oData, oHolder)
            if bReparent:
                oHolder.parent = 'My Collection'
            oHolder.create_pcs(oCardLookup, dLookupCache)
            self._aWarnings.extend(oHolder.get_warnings())
            oLogger.info('%s %s read', oIdParser.type, oItem.filename)

        oTrans.commit(close=True)
        sqlhub.processConnection = oOldConn
        if len(aToRead) == len(aList):
            raise IOError('Card sets with unstatisfiable parents %s' % (',').join([ x.filename for x in aToRead ]))
        return aToRead

    def _check_forced_reparent(self, oIdParser):
        """Do we need to force the parent of this to be 'My Collection'?"""
        raise NotImplementedError('implement _check_forced_reparent')

    def _should_force_reparent(self, oIdParser):
        """Check if we may need to force reparenting of card sets to
           'My Collection'"""
        raise NotImplementedError('implement _should_force_reparent')

    def _check_refresh(self, oIdParser):
        """Does this require we refresh the card set list?"""
        raise NotImplementedError('implement _check_refresh')

    def do_dump_all_to_zip(self, oLogHandler=None):
        """Dump all the database contents to the zip file"""
        aPhysicalCardSets = PhysicalCardSet.select()
        return self.do_dump_list_to_zip(aPhysicalCardSets, oLogHandler)

    def do_dump_list_to_zip(self, aCSList, oLogHandler=None):
        """Handle dumping a list of cards to the zip file with log fiddling"""
        self._open_zip_for_write()
        oLogger = Logger('Write zip file')
        if oLogHandler is not None:
            oLogger.addHandler(oLogHandler)
            if hasattr(oLogHandler, 'set_total'):
                if hasattr(aCSList, 'count'):
                    iTotal = aCSList.count()
                    oLogHandler.set_total(iTotal)
                else:
                    oLogHandler.set_total(len(aCSList))
        aPCSList = self._write_pcs_list_to_zip(aCSList, oLogger)
        self._close_zip()
        return aPCSList

    def dump_cs_names_to_zip(self, aCSNames, oLogHandler=None):
        """Utility function to dump a list of CS names to a zip"""
        aCSList = []
        for sName in aCSNames:
            aCSList.append(IPhysicalCardSet(sName))

        return self.do_dump_list_to_zip(aCSList, oLogHandler)

    def get_all_entries(self):
        """Return the list of card sets in the zip file"""
        self._open_zip_for_read()
        dCardSets = {}
        oIdParser = self._cIdentifyFile()
        for oItem in self.oZip.infolist():
            oData = self.oZip.read(oItem.filename)
            oIdParser.parse_string(oData)
            if oIdParser.can_parse():
                dCardSets[oIdParser.name] = (
                 oItem.filename,
                 oIdParser.parent_exists,
                 oIdParser.parent)

        self._close_zip()
        return dCardSets

    def read_single_card_set(self, sFilename):
        """Read a single card set into a card set holder."""
        self._open_zip_for_read()
        oIdParser = self._cIdentifyFile()
        oData = self.oZip.read(sFilename)
        oIdParser.parse_string(oData)
        oHolder = None
        if oIdParser.can_parse():
            oHolder = CachedCardSetHolder()
            oParser = oIdParser.get_parser()
            parse_string(oParser, oData, oHolder)
        self._close_zip()
        return oHolder

    def get_info_file(self, sFileName):
        """Try to find a non-deck file in the zipfile.

           Return None if it's not present, otherwise return
           the contents."""
        self._open_zip_for_read()
        sData = None
        for oItem in self.oZip.infolist():
            if oItem.filename == sFileName:
                sData = self.oZip.read(oItem.filename)
                break

        self._close_zip()
        return sData

    def get_warnings(self):
        """Get any warnings from the process"""
        return self._aWarnings