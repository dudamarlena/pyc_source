# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/GuiCardSetFunctions.py
# Compiled at: 2019-12-11 16:37:48
"""Useful utilities for managing card sets that need to access the gui"""
import datetime, logging, gtk
from sqlobject import sqlhub
from ..core.CardSetHolder import CardSetHolder, CardSetWrapper
from ..core.BaseTables import PhysicalCardSet
from ..core.BaseAdapters import IPhysicalCardSet
from ..core.CardLookup import LookupFailed
from ..core.CardSetUtilities import delete_physical_card_set, find_children, has_children, detect_loop, get_loop_names, break_loop, get_current_card_sets, clean_empty, check_cs_exists
from ..Utility import safe_filename
from .CreateCardSetDialog import CreateCardSetDialog
from .SutekhFileWidget import ExportDialog
from .RenameDialog import RenameDialog, PROMPT, RENAME, REPLACE
from .ProgressDialog import ProgressDialog, SutekhCountLogHandler
from .SutekhDialog import do_complaint_warning, do_complaint, do_complaint_error, do_exception_complaint

def reparent_card_set(oCardSet, oNewParent):
    """Helper function to ensure that reparenting a card set doesn't
       cause loops"""
    if oNewParent:
        oOldParent = oCardSet.parent
        oCardSet.parent = oNewParent
        oCardSet.syncUpdate()
        if detect_loop(oCardSet):
            oCardSet.parent = oOldParent
            oCardSet.syncUpdate()
            do_complaint('Changing parent of %s to %s introduces a loop. Leaving the parent unchanged.' % (
             oCardSet.name, oNewParent.name), gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE)
        else:
            return True
    else:
        oCardSet.parent = oNewParent
        oCardSet.syncUpdate()
        return True
    return False


def reparent_all_children(sCardSetName, aChildren):
    """Handle reparenting a list of children gracefully"""
    if aChildren:
        oCardSet = IPhysicalCardSet(sCardSetName)
        for oChildCS in aChildren:
            reparent_card_set(oChildCS, oCardSet)


def check_ok_to_delete(oCardSet):
    """Check if the user is OK with deleting the card set."""
    bChildren = has_children(oCardSet)
    iResponse = gtk.RESPONSE_OK
    if oCardSet.cards:
        if bChildren:
            iResponse = do_complaint_warning('Card Set %s Not Empty and Has Children. Really Delete?' % oCardSet.name)
        else:
            iResponse = do_complaint_warning('Card Set %s Not Empty. Really Delete?' % oCardSet.name)
    elif bChildren:
        iResponse = do_complaint_warning('Card Set %s Has Children. Really Delete?' % oCardSet.name)
    return iResponse == gtk.RESPONSE_OK


def create_card_set(oMainWindow):
    """Create a new card set from the edit dialog"""
    oDialog = CreateCardSetDialog(oMainWindow)
    oDialog.run()
    sName = oDialog.get_name()
    if sName:
        if check_cs_exists(sName):
            do_complaint_error('Card Set %s already exists.' % sName)
            return (None, None)
        sAuthor = oDialog.get_author()
        sComment = oDialog.get_comment()
        oParent = oDialog.get_parent()
        bInUse = oDialog.get_in_use()
        _oCS = PhysicalCardSet(name=sName, author=sAuthor, comment=sComment, parent=oParent, inuse=bInUse)
    return sName


def get_import_name(oHolder, iClashMode=PROMPT):
    """Helper for importing a card set holder.

       Deals with prompting the user for a new name if required, and properly
       dealing with child card sets if the user decides to replace an
       existing card set."""

    def setup_for_replace():
        """Little helper function to handle getting children and deleting
           the card set consistently"""
        oCS = IPhysicalCardSet(oHolder.name)
        aChildren = find_children(oCS)
        delete_physical_card_set(oHolder.name)
        return aChildren

    bRename = False
    if oHolder.name:
        if check_cs_exists(oHolder.name):
            bRename = True
    else:
        bRename = True
    aChildren = []
    if bRename:
        if iClashMode == PROMPT:
            oDlg = RenameDialog(oHolder.name)
            iResponse = oDlg.run()
            if iResponse == RENAME:
                oHolder.name = oDlg.sNewName
            elif iResponse == REPLACE:
                aChildren = setup_for_replace()
            else:
                oHolder.name = None
            oDlg.destroy()
        elif iClashMode == REPLACE:
            aChildren = setup_for_replace()
        elif iClashMode == RENAME:
            sTime = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
            sBaseName = '%s (imported %s)' % (oHolder.name, sTime)
            sNewName = sBaseName
            iCount = 0
            while check_cs_exists(sNewName):
                iCount += 1
                sNewName = '%s (%d)' % (sBaseName, iCount)

            oHolder.name = sNewName
    return (
     oHolder, aChildren)


def update_open_card_sets(sSetName, oMainWindow):
    """Update open copies of the card set sSetName to database changes
       (from imports, etc.)"""
    for oFrame in oMainWindow.find_cs_pane_by_set_name(sSetName):
        oFrame.update_to_new_db()

    oMainWindow.reload_pcs_list()


def update_card_set(oCardSet, oMainWindow):
    """Update the details of the card set when the user edits them."""
    sOldName = oCardSet.name
    oEditDialog = CreateCardSetDialog(oMainWindow, oCardSet=oCardSet)
    oEditDialog.run()
    sName = oEditDialog.get_name()
    if not sName:
        return
    if sName != oCardSet.name:
        oCardSet.name = sName
    sAuthor = oEditDialog.get_author()
    if sAuthor != oCardSet.author:
        oCardSet.author = sAuthor
    sComment = oEditDialog.get_comment()
    if sComment != oCardSet.comment:
        oCardSet.comment = sComment
    sAnnotations = oEditDialog.get_annotations()
    if sAnnotations != oCardSet.annotations:
        oCardSet.annotations = sAnnotations
    bInUse = oEditDialog.get_in_use()
    if bInUse != oCardSet.inuse:
        oCardSet.inuse = bInUse
    oParent = oEditDialog.get_parent()
    if oParent != oCardSet.parent:
        reparent_card_set(oCardSet, oParent)
    oCardSet.syncUpdate()
    for oFrame in oMainWindow.find_cs_pane_by_set_name(sOldName):
        oFrame.menu.update_card_set_menu(oCardSet)

    oMainWindow.reload_pcs_list()


def write_cs_to_file(oCardSet, oWriter, sFileName):
    """Core of the writing logic.

       Split out as a separate function so the plugins which tweak the
       Export Dialog can still use the same logic."""
    fOut = None
    try:
        try:
            fOut = open(sFileName, 'w')
            oWriter.write(fOut, CardSetWrapper(oCardSet))
        except Exception as oExp:
            sMsg = 'Writing the card set failed with the following error:\n%s\nAborting' % oExp
            do_exception_complaint(sMsg)

    finally:
        if fOut:
            fOut.close()

    return


def export_cs(oCardSet, cWriter, oParWin, sExt, aPatterns=None):
    """Query the user for a file name and
       export the card using the given writer."""
    sSuggestedFileName = '%s.%s' % (safe_filename(oCardSet.name), sExt)
    oDlg = ExportDialog('Save CardSet As ', oParWin, sSuggestedFileName)
    if aPatterns:
        for sName, aFiltPat in aPatterns:
            oDlg.add_filter_with_pattern(sName, aFiltPat)

    else:
        oDlg.add_filter_with_pattern('Text Files', ['*.txt'])
    oDlg.run()
    sFileName = oDlg.get_name()
    if sFileName is None:
        return
    else:
        oWriter = cWriter()
        write_cs_to_file(oCardSet, oWriter, sFileName)
        return


def import_cs(fIn, oParser, oMainWindow, sSetName=None):
    """Create a card set from the given file object."""
    oHolder = CardSetHolder()
    try:
        oParser.parse(fIn, oHolder)
    except Exception as oExp:
        sMsg = 'Reading the card set failed with the following error:\n%s\n The file is probably not in the format the Parser expects.\nAborting' % oExp
        do_exception_complaint(sMsg)
        return

    if oHolder.num_entries < 1:
        do_complaint_error('No cards found in the card set.\nThe file may not be in the format the Parser expects.\nAborting')
        return
    aWarnings = oHolder.get_warnings()
    if aWarnings:
        sMsg = 'The following warnings were reported:\n%s' % ('\n').join(aWarnings)
        logging.warn(sMsg)
        iResponse = do_complaint_warning('%s\nContinue with the import?' % sMsg)
        if iResponse != gtk.RESPONSE_OK:
            return
        oHolder.clear_warnings()
    if sSetName and not oHolder.name:
        oHolder.name = sSetName
    oHolder, aChildren = get_import_name(oHolder)
    if not oHolder.name:
        return
    try:
        oHolder.create_pcs(oCardLookup=oMainWindow.cardLookup)
        reparent_all_children(oHolder.name, aChildren)
        aWarnings = oHolder.get_warnings()
        if aWarnings:
            sMsg = 'Card Set Created.\nThe following warnings were reported during the final import:\n%s' % ('\n').join(aWarnings)
            logging.warn(sMsg)
            do_complaint(sMsg, gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE)
    except RuntimeError as oExp:
        sMsg = 'Creating the card set failed with the following error:\n%s\nAborting' % oExp
        do_exception_complaint(sMsg)
        return
    except LookupFailed as oExp:
        return

    if oMainWindow.find_cs_pane_by_set_name(oHolder.name):
        update_open_card_sets(oHolder.name, oMainWindow)
    else:
        oMainWindow.add_new_physical_card_set(oHolder.name)


def break_existing_loops():
    """Ensure there are no loops in the database"""
    for oCS in PhysicalCardSet.select():
        if detect_loop(oCS):
            sLoop = ('->').join(get_loop_names(oCS))
            sBreakName = break_loop(oCS)
            do_complaint('Loop %s in the card sets relationships.\nBreaking at %s' % (
             sLoop, sBreakName), gtk.MESSAGE_WARNING, gtk.BUTTONS_CLOSE)


def _unzip_helper(oZipFile, dList, oLogger, dRemaining, oMainWindow, aExcluded):
    """Helper function for unzip_list that handles a step of the unzip
       process inside an SQL transaction."""
    oOldConn = sqlhub.processConnection
    oTrans = oOldConn.transaction()
    sqlhub.processConnection = oTrans
    for sName, tInfo in dList.items():
        sFilename, _bIgnore, sParentName = tInfo
        if aExcluded:
            if sName in aExcluded or sParentName in aExcluded:
                oLogger.info('Read %s' % sName)
                continue
        if sParentName is not None and sParentName in dList:
            dRemaining[sName] = tInfo
            continue
        else:
            if sParentName is not None:
                if not check_cs_exists(sParentName):
                    return False
            try:
                oHolder = oZipFile.read_single_card_set(sFilename)
                oLogger.info('Read %s' % sName)
                if not oHolder.name:
                    continue
                aChildren = []
                if check_cs_exists(oHolder.name):
                    oCS = IPhysicalCardSet(oHolder.name)
                    aChildren = find_children(oCS)
                    if oCS.parent:
                        oHolder.parent = oCS.parent.name
                    delete_physical_card_set(oHolder.name)
                oHolder.create_pcs(oMainWindow.cardLookup)
                reparent_all_children(oHolder.name, aChildren)
                if oMainWindow.find_cs_pane_by_set_name(oHolder.name):
                    update_open_card_sets(oHolder.name, oMainWindow)
            except Exception as oException:
                sMsg = 'Failed to import card set %s.\n\n%s' % (
                 sName, oException)
                do_exception_complaint(sMsg)
                oTrans.commit(close=True)
                sqlhub.processConnection = oOldConn
                return False

    oTrans.commit(close=True)
    sqlhub.processConnection = oOldConn
    return True


def remove_decks_in_transaction(aToDelete, oMainWindow):
    """Remove an list of decks in a single transaction."""
    if not aToDelete:
        return []
    aOpenSets = []
    oOldConn = sqlhub.processConnection
    oTrans = oOldConn.transaction()
    sqlhub.processConnection = oTrans
    oCntLogHandler = SutekhCountLogHandler()
    oProgressDialog = ProgressDialog()
    oProgressDialog.set_description('Deleting obselete card sets')
    oCntLogHandler.set_total(len(aToDelete))
    oLogger = logging.Logger('Deleting decks')
    oLogger.addHandler(oCntLogHandler)
    oCntLogHandler.set_dialog(oProgressDialog)
    oProgressDialog.show()
    for sName in aToDelete:
        if not check_cs_exists(sName):
            continue
        for oFrame in oMainWindow.find_cs_pane_by_set_name(sName):
            oFrame.close_frame()
            aOpenSets.append(sName)

        delete_physical_card_set(sName)
        oLogger.info('deleted %s', sName)

    oTrans.commit(close=True)
    sqlhub.processConnection = oOldConn
    oMainWindow.reload_pcs_list()
    oProgressDialog.destroy()
    return aOpenSets


def reopen_card_sets(aOpenSets, oMainWindow):
    """Reopen card sets we closed earlier if they exist in the
       updated database."""
    for sName in aOpenSets:
        if check_cs_exists(sName):
            oMainWindow.add_new_physical_card_set(sName, False)

    oMainWindow.reload_pcs_list()


def unzip_files_into_db(aZipFiles, sProgDesc, oMainWindow, aToDelete, aExcluded=None):
    """Unzip cardsets from the zip files into an existing database, ensuring
       we unzip parents before their children."""
    aExistingList = get_current_card_sets()
    aOpenSets = remove_decks_in_transaction(aToDelete, oMainWindow)
    iZipTotal = 0
    for oZipFile in aZipFiles:
        iZipTotal += len(oZipFile.get_all_entries())

    oProgressDialog = ProgressDialog()
    oProgressDialog.set_description(sProgDesc)
    oCntLogHandler = SutekhCountLogHandler()
    oLogger = logging.Logger('Read zip file')
    oLogger.addHandler(oCntLogHandler)
    oCntLogHandler.set_dialog(oProgressDialog)
    oCntLogHandler.set_total(iZipTotal)
    oProgressDialog.show()
    aCSList = []
    for oZipFile in aZipFiles:
        dList = oZipFile.get_all_entries()
        while dList:
            dRemaining = {}
            if _unzip_helper(oZipFile, dList, oLogger, dRemaining, oMainWindow, aExcluded):
                dList = dRemaining
            else:
                oMainWindow.reload_pcs_list()
                oProgressDialog.destroy()
                return False

        aCSList.extend(oZipFile.get_all_entries().keys())

    clean_empty(aCSList, aExistingList)
    oProgressDialog.destroy()
    reopen_card_sets(aOpenSets, oMainWindow)
    return True