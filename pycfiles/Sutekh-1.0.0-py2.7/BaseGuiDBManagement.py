# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/BaseGuiDBManagement.py
# Compiled at: 2019-12-11 16:37:48
"""This handles the gui aspects of upgrading the database."""
import logging, datetime, zipfile
from collections import namedtuple
from StringIO import StringIO
import gtk
from sqlobject import sqlhub, connectionForURI
from ..core.BaseDBManagement import UnknownVersion, copy_to_new_abstract_card_db
from ..core.BaseTables import AbstractCard, PhysicalCardSet
from ..core.DBUtility import flush_cache, get_cs_id_name_table, refresh_tables, set_metadata_date, CARDLIST_UPDATE_DATE
from ..io.EncodedFile import EncodedFile
from ..io.UrlOps import urlopen_with_timeout, HashError
from ..io.BaseZipFileWrapper import ZipEntryProxy
from .DBUpgradeDialog import DBUpgradeDialog
from .ProgressDialog import ProgressDialog, SutekhCountLogHandler, SutekhHTMLLogHandler
from .SutekhDialog import do_complaint_buttons, do_complaint, do_complaint_warning, do_exception_complaint, do_complaint_error, do_complaint_error_details
from .GuiUtils import save_config
from .GuiDataPack import gui_error_handler, progress_fetch_data
from .DataFilesDialog import DataFilesDialog, COMBINED_ZIP

def wrapped_read(oFile, fDoRead, sDesc, oProgressDialog, oLogHandler):
    """Wrap the reading of a file in a ProgressDialog."""
    oProgressDialog.set_description(sDesc)
    oProgressDialog.show()
    fDoRead(oFile, oLogHandler)
    oProgressDialog.set_complete()


DataFileReader = namedtuple('DataFileReader', ['sName', 'sUrl',
 'sDescription',
 'tPattern', 'bRequired',
 'bCountLogger', 'fReader'])

class BaseGuiDBManager(object):
    """Base class for handling gui DB Upgrades."""
    tReaders = ()
    bDisplayZip = False
    sZippedUrl = None
    sHash = None
    aTables = []
    cZipFileWrapper = None

    def __init__(self, oWin, cDatabaseUpgrade):
        self._oWin = oWin
        self._oDatabaseUpgrade = cDatabaseUpgrade()

    def _get_names(self, bDisableBackup):
        """Query the user for the files / urls to import.

           Returns a list of file names and a backup file name if required.
           return dFiles, sBackupFile
           dFiles should be None to skip the import / initialisation."""
        sBackupFile = None
        oFilesDialog = DataFilesDialog(self._oWin, self.tReaders, self.bDisplayZip, self.sZippedUrl, bDisableBackup)
        oFilesDialog.run()
        dChoices, sBackupFile = oFilesDialog.get_names()
        oFilesDialog.destroy()
        dFiles = {}
        if COMBINED_ZIP in dChoices:
            dFiles = self.read_zip_file(dChoices[COMBINED_ZIP], self.sHash)
        else:
            for sName, oResult in dChoices.items():
                if oResult.sName is not None:
                    dFiles[sName] = EncodedFile(oResult.sName, bUrl=oResult.bIsUrl)

        return (
         dFiles, sBackupFile)

    def _do_import_checks(self, _oAbsCard):
        """Do the actual import checks.
           Returns a list of errors. An empty list is considered a success.

           Subclasses must implement the correct logic here."""
        raise NotImplementedError('Implement _do_import_checks')

    def _check_import(self):
        """Check the database for any import issues and display
           any errors to the user."""
        aMessages = []
        for oAbsCard in AbstractCard.select():
            aMessages.extend(self._do_import_checks(oAbsCard))

        if not aMessages:
            return True
        aFullMessages = ['<b>The database import has failed consistency checks</b>']
        for sDetails in aMessages:
            aFullMessages.append('<i>%s</i>' % sDetails)

        iRes = do_complaint_buttons(('\n').join(aFullMessages), gtk.MESSAGE_ERROR, ('Abort import?',
                                                                                    1,
                                                                                    'Accept import despite errors',
                                                                                    2), True)
        return iRes == 2

    def read_zip_file(self, oZipDetails, sHash):
        """open (Downlaoding it if required) a zip file and split it into
           the required bits.

           We provide a parameter for hashes, so it can be used when a
           hash is available."""
        aReaderNames = [ x.sName for x in self.tReaders ]
        if oZipDetails.bIsUrl:
            oFile = urlopen_with_timeout(oZipDetails.sName, fErrorHandler=gui_error_handler)
            try:
                sData = progress_fetch_data(oFile, sHash=sHash, sDesc='Downloading zipfile')
            except HashError:
                do_complaint_error('Checksum failed for zipfile.\nAborting')
                return

        else:
            if not oZipDetails.sName:
                do_complaint_error('No filename or url given to update from.\nAborting')
                return
            fIn = file(oZipDetails.sName, 'rb')
            sData = fIn.read()
            fIn.close()
        oZipFile = zipfile.ZipFile(StringIO(sData), 'r')
        aNames = oZipFile.namelist()
        dFiles = {}
        for sName in aNames:
            if sName in aReaderNames:
                oFile = ZipEntryProxy(oZipFile.read(sName))
                dFiles[sName] = oFile

        if not dFiles:
            do_complaint_error('Aborting the import.No useable files found in the zipfile')
        return dFiles

    def _read_data(self, dFiles, oProgressDialog):
        """Read the data from the give files / urls."""
        aMissing = []
        for oReader in self.tReaders:
            if oReader.bRequired and oReader.sName not in dFiles:
                aMissing.append('Missing %s' % oReader.sDescription)

        if aMissing:
            do_complaint_error_details('Aborting the import - Missing required data files', ('\n').join(aMissing))
            return False
        refresh_tables(self.aTables, sqlhub.processConnection)
        oProgressDialog.reset()
        for oReader in self.tReaders:
            if oReader.sName not in dFiles:
                continue
            if oReader.bCountLogger:
                oLogHandler = SutekhCountLogHandler()
            else:
                oLogHandler = SutekhHTMLLogHandler()
            oLogHandler.set_dialog(oProgressDialog)
            wrapped_read(dFiles[oReader.sName], oReader.fReader, oReader.sDescription, oProgressDialog, oLogHandler)

        return True

    def copy_to_new_db(self, oOldConn, oTempConn, oProgressDialog, oLogHandler):
        """Copy card collection and card sets to a new abstract card db."""
        oProgressDialog.set_description('Reloading card collection and card sets')
        oProgressDialog.reset()
        bOK, aErrors = copy_to_new_abstract_card_db(oOldConn, oTempConn, self._oWin.cardLookup, oLogHandler)
        oProgressDialog.set_complete()
        if not bOK:
            sMesg = ('\n').join([
             'There was a problem copying your collection to the new database'] + aErrors + [
             'Attempt to Continue Anyway (This is most probably very dangerous)?'])
            iResponse = do_complaint_warning(sMesg)
            return iResponse == gtk.RESPONSE_OK
        return True

    def initialize_db(self, oConfig):
        """Initialise the database if it doesn't exist."""
        iRes = do_complaint_buttons("The database doesn't seem to be properly initialised", gtk.MESSAGE_ERROR, (
         gtk.STOCK_QUIT, gtk.RESPONSE_CLOSE,
         'Initialise database with cardlist and rulings?', 1))
        if iRes != 1:
            return False
        else:
            dFiles, _sBackup = self._get_names(True)
            if dFiles is not None:
                oProgressDialog = ProgressDialog()
                try:
                    bRet = self._read_data(dFiles, oProgressDialog)
                    oProgressDialog.destroy()
                except IOError as oErr:
                    do_exception_complaint('Failed to read cardlists.\n\n%s\nAborting import.' % oErr)
                    oProgressDialog.destroy()
                    return False

            else:
                return False
            if bRet:
                PhysicalCardSet(name='My Collection', parent=None)
            return bRet

    def save_backup(self, sBackupFile, oProgressDialog):
        """Save a backup file, showing a progress dialog"""
        oLogHandler = SutekhCountLogHandler()
        oProgressDialog.set_description('Saving backup')
        oLogHandler.set_dialog(oProgressDialog)
        oProgressDialog.show()
        oFile = self.cZipFileWrapper(sBackupFile)
        oFile.do_dump_all_to_zip(oLogHandler)
        oProgressDialog.set_complete()

    def refresh_card_list(self, oUpdateDate=None, dFiles=None):
        """Handle grunt work of refreshing the card lists"""
        aEditable = self._oWin.get_editable_panes()
        dOldMap = get_cs_id_name_table()
        if not dFiles:
            dFiles, sBackupFile = self._get_names(False)
        else:
            sBackupFile = None
        if not dFiles:
            return False
        else:
            oProgressDialog = ProgressDialog()
            if sBackupFile is not None:
                try:
                    self.save_backup(sBackupFile, oProgressDialog)
                except Exception as oErr:
                    do_exception_complaint('Failed to write backup.\n\n%s\nNot touching the database further.' % oErr)
                    return False

            self._oWin.prepare_for_db_update()
            oOldConn = sqlhub.processConnection
            oTempConn = connectionForURI('sqlite:///:memory:')
            sqlhub.processConnection = oTempConn
            try:
                bRet = self._read_data(dFiles, oProgressDialog)
            except IOError as oErr:
                do_exception_complaint('Failed to read cardlists.\n\n%s\nAborting import.' % oErr)
                oProgressDialog.destroy()
                sqlhub.processConnection = oOldConn
                self._oWin.update_to_new_db()
                return False

            if not bRet:
                oProgressDialog.destroy()
                sqlhub.processConnection = oOldConn
                self._oWin.update_to_new_db()
                return False
            if not self._check_import():
                oProgressDialog.destroy()
                sqlhub.processConnection = oOldConn
                self._oWin.update_to_new_db()
                return False
            oLogHandler = SutekhCountLogHandler()
            oLogHandler.set_dialog(oProgressDialog)
            sqlhub.processConnection = oOldConn
            if not self.copy_to_new_db(oOldConn, oTempConn, oProgressDialog, oLogHandler):
                oProgressDialog.destroy()
                self._oWin.update_to_new_db()
                return True
            sqlhub.processConnection = oOldConn
            self._oWin.clear_cache()
            oProgressDialog.set_description('Finalizing import')
            oProgressDialog.reset()
            oProgressDialog.show()
            bOK, aErrors = self._oDatabaseUpgrade.create_final_copy(oTempConn, oLogHandler)
            if not bOK:
                sMesg = 'There was a problem updating the database\nYour database may be in an inconsistent state - sorry'
                logging.warn(('\n').join([sMesg] + aErrors))
                do_complaint_error_details(sMesg, ('\n').join(aErrors))
            else:
                sMesg = 'Import Completed\n'
                sMesg += 'Everything seems to have gone OK'
                do_complaint(sMesg, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, True)
            oProgressDialog.destroy()
            dNewMap = get_cs_id_name_table()
            self._oWin.config_file.fix_profile_mapping(dOldMap, dNewMap)
            self._oWin.update_to_new_db()
            self._oWin.restore_editable_panes(aEditable)
            if oUpdateDate:
                set_metadata_date(CARDLIST_UPDATE_DATE, oUpdateDate)
            save_config(self._oWin.config_file)
            return True

    def do_db_upgrade(self, aLowerTables, aHigherTables):
        """Attempt to upgrade the database"""
        if aHigherTables:
            sMesg = 'Database version error. Cannot continue\nThe following tables have a higher version than expected:\n'
            sMesg += ('\n').join(aHigherTables)
            sMesg += '\n\n<b>Unable to continue</b>'
            do_complaint_buttons(sMesg, gtk.MESSAGE_ERROR, (
             gtk.STOCK_QUIT, gtk.RESPONSE_CLOSE), True)
            return False
        sMesg = 'Database version error. Cannot continue\nThe following tables need to be upgraded:\n'
        sMesg += ('\n').join(aLowerTables)
        iRes = do_complaint_buttons(sMesg, gtk.MESSAGE_ERROR, (
         gtk.STOCK_QUIT, gtk.RESPONSE_CLOSE,
         'Attempt Automatic Database Upgrade', 1))
        if iRes != 1:
            return False
        oTempConn = connectionForURI('sqlite:///:memory:')
        oLogHandler = SutekhCountLogHandler()
        oProgressDialog = ProgressDialog()
        oLogHandler.set_dialog(oProgressDialog)
        try:
            oProgressDialog.set_description('Creating temporary copy')
            bOK, aMessages = self._oDatabaseUpgrade.create_memory_copy(oTempConn, oLogHandler)
            oProgressDialog.destroy()
            if bOK:
                oDialog = DBUpgradeDialog(aMessages)
                iRes = oDialog.run()
                oDialog.destroy()
                if iRes == gtk.RESPONSE_OK:
                    return self._do_commit_db(oLogHandler, oTempConn, aMessages)
                if iRes == 1:
                    sqlhub.processConnection = oTempConn
                    flush_cache()
                    return True
            else:
                sMesg = 'Unable to create memory copy!\nUpgrade Failed.'
                logging.warn(('\n').join([sMesg] + aMessages))
                do_complaint_error_details(sMesg, ('\n').join(aMessages))
        except UnknownVersion as oErr:
            oProgressDialog.destroy()
            do_exception_complaint('Upgrade Failed. %s' % oErr)

        return False

    def _do_commit_db(self, oLogHandler, oTempConn, aOldMessages):
        """Handle committing the memory copy to the actual DB"""
        oProgressDialog = ProgressDialog()
        oProgressDialog.set_description('Commiting changes')
        oLogHandler.set_dialog(oProgressDialog)
        bOK, aMessages = self._oDatabaseUpgrade.create_final_copy(oTempConn, oLogHandler)
        oProgressDialog.destroy()
        if bOK:
            if aOldMessages:
                sMesg = 'Messages from Database Upgrade are:\n'
                for sStr in aOldMessages:
                    sMesg += '<b>%s</b>\n' % sStr

                sMesg += '\nChanges Commited\n'
            else:
                sMesg = 'Changes Commited\n'
            if aMessages:
                sMesg += 'Messages from commiting changes are:'
                for sStr in aMessages:
                    sMesg += '<b>%s</b>\n' % sStr

            else:
                sMesg += 'Everything seems to have gone smoothly.'
            do_complaint(sMesg, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, True)
            return True
        sMesg = 'Unable to commit updated database!\nUpgrade Failed.\nYour database may be in an inconsistent state.'
        logging.warn(('\n').join([sMesg] + aMessages))
        do_complaint_error_details(sMesg, ('\n').join(aMessages))
        return False