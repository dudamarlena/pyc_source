# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/plugins/TWDADeckInfo.py
# Compiled at: 2019-12-11 16:37:54
"""Adds info about the TWDA decks cards are found in"""
import re, datetime
from logging import Logger
from StringIO import StringIO
import gtk
from sqlobject import SQLObjectNotFound
from sutekh.base.core.BaseTables import PhysicalCardSet, PhysicalCard, MapPhysicalCardToPhysicalCardSet
from sutekh.base.core.BaseAdapters import IAbstractCard, IPhysicalCardSet
from sutekh.base.core.BaseFilters import FilterOrBox, FilterAndBox, SpecificCardFilter, MultiPhysicalCardSetMapFilter
from sutekh.base.io.UrlOps import urlopen_with_timeout, fetch_data, HashError
from sutekh.base.gui.SutekhDialog import SutekhDialog, NotebookDialog, do_complaint_error
from sutekh.base.gui.ProgressDialog import ProgressDialog, SutekhCountLogHandler
from sutekh.base.gui.GuiCardSetFunctions import unzip_files_into_db
from sutekh.base.gui.FileOrUrlWidget import FileOrUrlWidget
from sutekh.base.gui.SutekhFileWidget import add_filter
from sutekh.base.gui.AutoScrolledWindow import AutoScrolledWindow
from sutekh.base.gui.GuiDataPack import gui_error_handler
from sutekh.io.DataPack import find_all_data_packs, DOC_URL
from sutekh.io.ZipFileWrapper import ZipFileWrapper
from sutekh.gui.PluginManager import SutekhPlugin

class BinnedCountLogHandler(SutekhCountLogHandler):
    """Wrapped around SutekhCountLogHandler to handle downloading
       multiple files with a single progess dialog"""

    def __init__(self):
        super(BinnedCountLogHandler, self).__init__()
        self.fTotBins = 0.0
        self.fBinFrac = 0.0

    def set_tot_bins(self, iBins):
        """Set the total bins for the update steps"""
        self.fTotBins = float(iBins)

    def inc_cur_bin(self):
        """Move to the next bin"""
        self.fBinFrac += 1 / self.fTotBins
        self.iCount = 0
        self.fTot = 0.0

    def emit(self, _oRecord):
        """Scale the progress bar to just be a fraction of the current bin"""
        if self.oDialog is None:
            return
        else:
            self.iCount += 1
            fBinPos = self.iCount / (self.fTot * self.fTotBins)
            fBarPos = self.fBinFrac + fBinPos
            self.oDialog.update_bar(fBarPos)
            return


class TWDAConfigDialog(SutekhDialog):
    """Dialog for configuring the TWDA plugin."""
    sDocUrl = DOC_URL

    def __init__(self, oParent, bFirstTime=False):
        super(TWDAConfigDialog, self).__init__('Configure TWDA Info Plugin', oParent, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (
         gtk.STOCK_OK, gtk.RESPONSE_OK,
         gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        oDescLabel = gtk.Label()
        if not bFirstTime:
            oDescLabel.set_markup('<b>Choose how to configure the Tournament Winning Deck Archive (TWDA) info plugin</b>')
        else:
            oDescLabel.set_markup('<b>Choose how to configure the Tournament Winning Deck Archive (TWDA) info plugin</b>\nChoose cancel to skip configuring the plugin\nYou will not be prompted again')
        self.oFileWidget = FileOrUrlWidget(oParent, 'Choose location for TWDA decks', {'Sutekh Datapack': self.sDocUrl})
        add_filter(self.oFileWidget, 'Zip Files', ['*.zip', '*.ZIP'])
        self.vbox.pack_start(oDescLabel, False, False)
        self.vbox.pack_start(gtk.HSeparator(), False, False)
        self.vbox.pack_start(self.oFileWidget, False, False)
        self.set_size_request(350, 300)
        self.show_all()

    def is_url(self):
        """Check if the user has chosen an url"""
        _sFile, bUrl = self.oFileWidget.get_file_or_url()
        return bUrl

    def get_file_data(self):
        """Get data from a physical file"""
        _sFile, bUrl = self.oFileWidget.get_file_or_url()
        if bUrl:
            return None
        else:
            return self.oFileWidget.get_binary_data()

    def get_url_data(self):
        """Return the relevant data from the url given.

           Returns a tuple of arrays (urls, dates, hashes)"""
        _sFile, bUrl = self.oFileWidget.get_file_or_url()
        if not bUrl:
            return (None, None, None)
        else:
            return find_all_data_packs('twd', fErrorHandler=gui_error_handler)


class TWDAInfoPlugin(SutekhPlugin):
    """Plugin providing access to TWDA decks."""
    dTableVersions = {PhysicalCardSet: (5, 6, 7)}
    aModelsSupported = (
     PhysicalCardSet, PhysicalCard, 'MainWindow')
    oTWDARegex = re.compile('^TWDA ([0-9]{4})$')
    dGlobalConfig = {'twda configured': 'option("Yes", "No", "Unasked", default="Unasked")'}
    sMenuName = 'Find TWDA decks containing'
    sHelpCategory = 'card_sets:analysis'
    sHelpText = 'If you have downloaded the database of tournament winning\n                   decks, this allows you to search the tournament winning\n                   deck archive for decks containing specific combinations of\n                   cards.\n\n                   You can either search for all the selected cards or for\n                   those that contain at least 1 of the selected cards.\n\n                   The results are grouped by year, and list the number of\n                   matching card found in each listed deck. The matching\n                   decks can be opened as new panes by choosing the\n                   "Open cardset" option.\n\n                   The results dialog in not modal, so it\'s possible to\n                   examine the opened card sets closely without closing\n                   the search results.'

    def __init__(self, *args, **kwargs):
        super(TWDAInfoPlugin, self).__init__(*args, **kwargs)
        self.oAllTWDA = None
        self.oAnyTWDA = None
        return

    def get_menu_item(self):
        """Overrides method from base class.

           Adds the menu item to the analyze menu.
           """
        if self.model is None:
            oDownload = gtk.MenuItem('Download TWDA decks')
            oDownload.connect('activate', self.do_download)
            return (
             'Data Downloads', oDownload)
        else:
            oTWDMenu = gtk.MenuItem(self.sMenuName + ' ... ')
            oSubMenu = gtk.Menu()
            oTWDMenu.set_submenu(oSubMenu)
            self.oAllTWDA = gtk.MenuItem('ALL selected cards')
            oSubMenu.add(self.oAllTWDA)
            self.oAllTWDA.connect('activate', self.find_twda, 'all')
            self.oAnyTWDA = gtk.MenuItem('ANY selected cards')
            oSubMenu.add(self.oAnyTWDA)
            self.oAnyTWDA.connect('activate', self.find_twda, 'any')
            if self.check_enabled():
                self.oAnyTWDA.set_sensitive(True)
                self.oAllTWDA.set_sensitive(True)
            else:
                self.oAnyTWDA.set_sensitive(False)
                self.oAllTWDA.set_sensitive(False)
            return (
             'Analyze', oTWDMenu)

    def find_twda(self, _oWidget, sMode):
        """Find decks which match the given search"""
        aAbsCards = set(self._get_selected_abs_cards())
        if not aAbsCards:
            do_complaint_error('Need to select some cards for this plugin')
            return
        if len(aAbsCards) > 20:
            do_complaint_error('Too many cards selected (%d). Please select no more than 20 cards' % len(aAbsCards))
            return
        aCardFilters = []
        iTotCards = len(aAbsCards)
        for oCard in aAbsCards:
            aCardFilters.append(SpecificCardFilter(oCard))

        oCardFilter = FilterOrBox(aCardFilters)
        aNames = self._get_twda_names()
        oMapFilter = MultiPhysicalCardSetMapFilter(aNames)
        oFullFilter = FilterAndBox([oCardFilter, oMapFilter])
        dCardSets = {}
        for oMapCard in oFullFilter.select(MapPhysicalCardToPhysicalCardSet):
            oCS = oMapCard.physicalCardSet
            sCardName = IAbstractCard(oMapCard).name
            dCardSets.setdefault(oCS, {})
            dCardSets[oCS].setdefault(sCardName, 0)
            dCardSets[oCS][sCardName] += 1

        if sMode == 'all' and iTotCards > 1:
            for oCS in list(dCardSets):
                if len(dCardSets[oCS]) != iTotCards:
                    del dCardSets[oCS]

        sCards = ('",  "').join(sorted([ x.name for x in aAbsCards ]))
        if sMode == 'any':
            sMatchText = 'Matching ANY of "%s"' % sCards
        else:
            sMatchText = 'Matching ALL of "%s"' % sCards
        if dCardSets:
            oDlg = self._fill_dlg(dCardSets, sMatchText)
        else:
            oDlg = self._empty_dlg(sMatchText)
        oDlg.set_default_size(700, 600)
        oDlg.show_all()
        oDlg.show()

    def _fill_dlg(self, dCardSets, sMatchText):
        """Add info about the card sets to the dialog"""
        oDlg = NotebookDialog('TWDA matches', self.parent, gtk.DIALOG_DESTROY_WITH_PARENT, (
         gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
        aParents = set([ oCS.parent.name for oCS in dCardSets ])
        dPages = {}
        oDlg.connect('response', lambda dlg, but: dlg.destroy())
        for sName in sorted(aParents):
            oInfo = gtk.VBox(False, 2)
            oDlg.add_widget_page(AutoScrolledWindow(oInfo, True), sName.replace('TWDA ', ''))
            oInfo.pack_start(gtk.Label(sMatchText), expand=False, padding=6)
            iCardSets = len([ x for x in dCardSets if x.parent.name == sName ])
            oInfo.pack_start(gtk.Label('%d Card Sets' % iCardSets), expand=False, padding=4)
            dPages[sName] = oInfo

        for oCS in sorted(dCardSets, key=lambda x: x.name):
            oInfo = dPages[oCS.parent.name]
            oName = gtk.Label(oCS.name)
            aCardInfo = []
            for sName in sorted(dCardSets[oCS]):
                aCardInfo.append('  - %s × %d' % (sName, dCardSets[oCS][sName]))

            oCards = gtk.Label(('\n').join(aCardInfo))
            oButton = gtk.Button('Open cardset')
            oButton.connect('clicked', self._open_card_set, oCS)
            oInfo.pack_start(oName, expand=False)
            oInfo.pack_start(oCards, expand=False)
            oInfo.pack_start(oButton, expand=False)
            oInfo.pack_start(gtk.HSeparator(), expand=False)

        return oDlg

    def _empty_dlg(self, sMatchText):
        """Add an nothing found notice to dialog"""
        oDlg = SutekhDialog('No TWDA matches', self.parent, gtk.DIALOG_DESTROY_WITH_PARENT, (
         gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
        oDlg.connect('response', lambda dlg, but: dlg.destroy())
        oLabel = gtk.Label('No decks found statisfying %s' % sMatchText)
        oDlg.vbox.pack_start(oLabel)
        return oDlg

    def _open_card_set(self, _oButton, oCS):
        """Wrapper around open_cs to handle being called directly from a
           gtk widget"""
        self._open_cs(oCS.name)

    def check_enabled(self):
        """check for TWD decks in the database and disable menu if not"""
        bEnabled = False
        for oCS in PhysicalCardSet.select():
            oMatch = self.oTWDARegex.match(oCS.name)
            if oMatch:
                bEnabled = True
                break

        return bEnabled

    def _get_twda_names(self):
        """Get names of all the TWDA entries in the current database"""
        aNames = []
        for oCS in PhysicalCardSet.select():
            if not oCS.parent or not oCS.inuse:
                continue
            oMatch = self.oTWDARegex.match(oCS.parent.name)
            if oMatch:
                aNames.append(oCS.name)

        return aNames

    def _get_twda_holders(self):
        """Return all the TWDA holders in the current database"""
        aHolders = []
        for oCS in PhysicalCardSet.select():
            oMatch = self.oTWDARegex.match(oCS.name)
            if oMatch:
                aHolders.append(oCS)

        return aHolders

    def setup(self):
        """1st time setup tasks"""
        sPrefsValue = self.get_config_item('twda configured')
        if sPrefsValue == 'Unasked':
            self.set_config_item('twda configured', 'No')
            oDialog = TWDAConfigDialog(self.parent, True)
            self.handle_response(oDialog)

    def do_download(self, _oMenuWidget):
        """Prompt the user to download/setup decks"""
        oDialog = TWDAConfigDialog(self.parent)
        self.handle_response(oDialog)

    def handle_response(self, oDialog):
        """Handle running and responding to the download dialog"""
        iResponse = oDialog.run()
        if iResponse == gtk.RESPONSE_OK:
            if oDialog.is_url():
                aUrls, aDates, aHashes = oDialog.get_url_data()
                if not aUrls:
                    do_complaint_error('Unable to access TWD data')
                elif not self._get_decks(aUrls, aDates, aHashes):
                    do_complaint_error("Didn't find any TWD data to download")
                else:
                    self.set_config_item('twda configured', 'Yes')
            elif self._unzip_twda_file(oDialog.get_file_data()):
                self.set_config_item('twda configured', 'Yes')
        oDialog.destroy()

    def check_for_updates(self):
        """Check for any updates at startup."""
        sPrefsValue = self.get_config_item('twda configured')
        if sPrefsValue.lower() != 'yes':
            return
        else:
            aUrls, aDates, aHashes = find_all_data_packs('twd', fErrorHandler=gui_error_handler)
            if not aUrls:
                return
            aToUnzip, _aToReplace = self._get_decks_to_download(aUrls, aDates, aHashes)
            if aToUnzip:
                aMessages = [
                 'The following TWDA updates are available: ']
                for _sUrl, sTWDA, _sHash in aToUnzip:
                    aMessages.append('<b>%s</b>' % sTWDA)

                return ('\n').join(aMessages)
            return

    def do_update(self):
        """Handle the 'download stuff' respone from the startup check"""
        sPrefsValue = self.get_config_item('twda configured')
        if sPrefsValue.lower() != 'yes':
            return
        aUrls, aDates, aHashes = find_all_data_packs('twd', fErrorHandler=gui_error_handler)
        if not self._get_decks(aUrls, aDates, aHashes):
            do_complaint_error("Didn't find any TWD data to download")

    def _get_decks_to_download(self, aUrls, aDates, aHashes):
        """Check for any decks we need to download."""
        aToUnzip = []
        aToReplace = []
        for sUrl, sDate, sHash in zip(aUrls, aDates, aHashes):
            if not sUrl:
                return (False, False)
            sZipName = sUrl.split('/')[(-1)]
            sTWDA = sZipName.replace('Sutekh_', '').replace('.zip', '')
            sTWDA = sTWDA[:9].replace('_', ' ')
            try:
                oHolder = IPhysicalCardSet(sTWDA)
            except SQLObjectNotFound:
                aToUnzip.append((sUrl, sTWDA, sHash))
                continue

            try:
                oUrlDate = datetime.datetime.strptime(sDate, '%Y-%m-%d')
            except ValueError:
                oUrlDate = None

            sTWDUpdated = 'Date Updated:'
            oTWDDate = None
            for sLine in oHolder.annotations.splitlines():
                if sLine.startswith(sTWDUpdated):
                    sTWDDate = sLine.split(sTWDUpdated)[1][1:11]
                    try:
                        oTWDDate = datetime.datetime.strptime(sTWDDate, '%Y-%m-%d')
                    except ValueError:
                        pass

            if oTWDDate is None or oUrlDate is None:
                aToUnzip.append((sUrl, sTWDA, sHash))
                aToReplace.append(sTWDA)
            elif oTWDDate < oUrlDate:
                aToUnzip.append((sUrl, sTWDA, sHash))
                aToReplace.append(sTWDA)

        return (
         aToUnzip, aToReplace)

    def _get_decks(self, aUrls, aDates, aHashes):
        """Unzip a file containing the decks."""
        aZipHolders = []
        aToUnzip, aToReplace = self._get_decks_to_download(aUrls, aDates, aHashes)
        if not aToUnzip:
            return False
        oBinLogHandler = BinnedCountLogHandler()
        oProgressDialog = ProgressDialog()
        oProgressDialog.set_description('Downloading TWDA data')
        oLogger = Logger('Download zip files')
        oLogger.addHandler(oBinLogHandler)
        oBinLogHandler.set_dialog(oProgressDialog)
        oBinLogHandler.set_tot_bins(len(aToUnzip))
        oProgressDialog.show()
        for sUrl, sTWDA, sHash in sorted(aToUnzip, key=lambda x: x[1]):
            oFile = urlopen_with_timeout(sUrl, fErrorHandler=gui_error_handler)
            oProgressDialog.set_description('Downloading %s' % sTWDA)
            try:
                sData = fetch_data(oFile, sHash=sHash, oLogHandler=oBinLogHandler, fErrorHandler=gui_error_handler)
            except HashError:
                do_complaint_error('Checksum failed for %s\nSkipping' % sTWDA)
                aToReplace.remove(sTWDA)
                continue

            oZipFile = ZipFileWrapper(StringIO(sData))
            aZipHolders.append(oZipFile)
            oBinLogHandler.inc_cur_bin()

        oProgressDialog.destroy()
        if not aZipHolders:
            return False
        aToDelete = []
        for oCS in list(PhysicalCardSet.select()):
            if not oCS.parent:
                continue
            if oCS.parent.name in aToReplace:
                aToDelete.append(oCS.name)

        return unzip_files_into_db(aZipHolders, 'Adding TWDA Data', self.parent, aToDelete)

    def _unzip_twda_file(self, oFile):
        """Unzip a single zip file containing all the TWDA entries"""
        dList = oFile.get_all_entries()
        bOK = False
        for sName in dList:
            oMatch = self.oTWDARegex.match(sName)
            if oMatch:
                bOK = True
                break

        if not bOK:
            return False
        aToDelete = self._get_twda_names()
        return unzip_files_into_db([oFile], 'Adding TWDA Data', self.parent, aToDelete)


plugin = TWDAInfoPlugin