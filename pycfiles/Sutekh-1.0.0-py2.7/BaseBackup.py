# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/plugins/BaseBackup.py
# Compiled at: 2019-12-11 16:37:39
"""Plugin to wrap zipfile backup and restore methods"""
import os, gtk
from ..BasePluginManager import BasePlugin
from ..SutekhDialog import do_complaint_warning, do_exception_complaint
from ..SutekhFileWidget import ZipFileDialog
from ..ProgressDialog import ProgressDialog, SutekhCountLogHandler
from ...core.DBUtility import get_cs_id_name_table

class BaseBackup(BasePlugin):
    """Provide access to ZipFileWrapper's backup and restore methods.

       Handle GUI aspects associated with restoring (ensuring everything
       reloads, etc.)
       """
    dTableVersions = {}
    aModelsSupported = ('MainWindow', )
    cZipWrapper = None
    sMenuName = 'Backup'
    sHelpCategory = 'card_list:file'
    sHelpText = 'This allows you either to save or to restore a full backup\n                   of the current database. The backup is saved as a zip file,\n                   and is independent of the database back-end used.\n                   Consequently, the backup can also be used to transfer\n                   the complete state between different databases.\n\n                   There are two options offered:\n\n                   * _Save a Full Backup_: Save the current state (card sets                    and their contents) to the specified zip file.\n                   * _Restore a Full Backup_: Import all the card sets from                    the specified zip file. Note that restoring a backup will                    replace anything currently in the database with the                    contents of the backup.\n\n                   You can save a backup at any time. You will be asked\n                   whether you would like to save a backup when you\n                   initiate certain actions, such as updating the full\n                   card list.'

    @classmethod
    def get_help_list_text(cls):
        return 'Save or restore backups of the database, discussed                   further in the **Backup** section'

    def get_menu_item(self):
        """Register on the Plugins menu"""
        oBackup = gtk.MenuItem('Save a Full Backup')
        oBackup.connect('activate', self.activate_backup)
        oRestore = gtk.MenuItem('Restore a Full Backup')
        oRestore.connect('activate', self.activate_restore)
        return [
         (
          'Backup', oBackup), ('Backup', oRestore)]

    def activate_backup(self, _oWidget):
        """Handle backup request"""
        oDlg = self.make_backup_dialog()
        oDlg.run()
        sFilename = oDlg.get_name()
        if sFilename:
            self.handle_backup_response(sFilename)

    def activate_restore(self, _oWidget):
        """Handle restore request"""
        oDlg = self.make_restore_dialog()
        oDlg.run()
        sFilename = oDlg.get_name()
        if sFilename:
            self.handle_restore_response(sFilename)

    def make_backup_dialog(self):
        """Create file dialog for backup"""
        sName = 'Choose a file to save the full backup to ...'
        oDlg = ZipFileDialog(self.parent, sName, gtk.FILE_CHOOSER_ACTION_SAVE)
        oDlg.set_do_overwrite_confirmation(True)
        oDlg.show_all()
        return oDlg

    def handle_backup_response(self, sFilename):
        """Handle response from backup dialog"""
        try:
            oLogHandler = SutekhCountLogHandler()
            oProgressDialog = ProgressDialog()
            oProgressDialog.set_description('Saving backup')
            oLogHandler.set_dialog(oProgressDialog)
            oProgressDialog.show()
            oFile = self.cZipWrapper(sFilename)
            oFile.do_dump_all_to_zip(oLogHandler)
            oProgressDialog.destroy()
        except Exception as oException:
            oProgressDialog.destroy()
            sMsg = 'Failed to write backup.\n\n%s' % oException
            do_exception_complaint(sMsg)

    def make_restore_dialog(self):
        """Create file chooser dialog for restore"""
        sName = 'Restore a Full Backup ....'
        oDlg = ZipFileDialog(self.parent, sName, gtk.FILE_CHOOSER_ACTION_OPEN)
        oWarning = gtk.Label()
        oWarning.set_markup('<b>This will delete all existing Card Sets</b>')
        oDlg.vbox.pack_start(oWarning, expand=False)
        oDlg.vbox.reorder_child(oWarning, 0)
        oDlg.show_all()
        return oDlg

    def handle_restore_response(self, sFilename):
        """Handle response from the restore dialog"""
        bContinue = True
        if not os.path.exists(sFilename):
            bContinue = do_complaint_warning('Backup file %s does not seem to exist.' % sFilename) != gtk.RESPONSE_CANCEL
        if bContinue:
            dOldMap = get_cs_id_name_table()
            self.parent.prepare_for_db_update()
            try:
                aEditable = self.parent.get_editable_panes()
                oLogHandler = SutekhCountLogHandler()
                oProgressDialog = ProgressDialog()
                oProgressDialog.set_description('Restoring backup')
                oLogHandler.set_dialog(oProgressDialog)
                oProgressDialog.show()
                oFile = self.cZipWrapper(sFilename)
                oFile.do_restore_from_zip(self.cardlookup, oLogHandler)
                aMessages = oFile.get_warnings()
                if aMessages:
                    sMsg = 'The following warnings were reported:\n%s' % ('\n').join(aMessages)
                    do_complaint_warning(sMsg)
                dNewMap = get_cs_id_name_table()
                self.parent.config_file.fix_profile_mapping(dOldMap, dNewMap)
                self.parent.update_to_new_db()
                oProgressDialog.destroy()
                self.parent.restore_editable_panes(aEditable)
            except Exception as oException:
                self.parent.update_to_new_db()
                oProgressDialog.destroy()
                sMsg = 'Failed to restore backup.\n\n%s' % oException
                do_exception_complaint(sMsg)