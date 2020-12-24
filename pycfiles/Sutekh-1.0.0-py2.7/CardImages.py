# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/plugins/CardImages.py
# Compiled at: 2019-12-11 16:37:54
"""Adds a frame which will display card images from ARDB in the GUI"""
import datetime, os, logging, gtk
from sqlobject import SQLObjectNotFound
from sutekh.base.core.BaseAdapters import IExpansion, IPrinting
from sutekh.base.gui.SutekhDialog import do_complaint_error
from sutekh.base.Utility import ensure_dir_exists
from sutekh.base.gui.plugins.BaseImages import BaseImageFrame, BaseImageConfigDialog, BaseImagePlugin, check_file, unaccent, CARD_IMAGE_PATH, DOWNLOAD_IMAGES, DOWNLOAD_EXPANSIONS
from sutekh.gui.PluginManager import SutekhPlugin
from sutekh.SutekhInfo import SutekhInfo
SUTEKH_IMAGE_SITE = 'https://sutekh.vtes.za.net'
IMAGE_DATE_FILE = 'image_dates.txt'
SUTEKH_USER_AGENT = {'User-Agent': 'Sutekh Image Plugin'}

class CardImageFrame(BaseImageFrame):
    """Frame which displays the image.

       Adds the VtES specific handling.
       """
    APP_NAME = SutekhInfo.NAME
    SPECIAL_PROMOS = [
     'Anarchs and Alastors Storyline',
     'Promo-20190408']
    _dReqHeaders = SUTEKH_USER_AGENT

    def _have_expansions(self, sTestPath=''):
        """Test if directory contains expansion/image structure used by ARDB"""
        oConfig = self._config_download_expansions()
        if oConfig is not None:
            return oConfig
        else:
            if sTestPath == '':
                sTestFile = os.path.join(self._sPrefsPath, 'bh', 'acrobatics.jpg')
            else:
                sTestFile = os.path.join(sTestPath, 'bh', 'acrobatics.jpg')
            return check_file(sTestFile)

    def _check_test_file(self, sTestPath=''):
        """Test if acrobatics.jpg exists"""
        if self._config_download_images():
            return True
        if sTestPath == '':
            sTestFile = os.path.join(self._sPrefsPath, 'acrobatics.jpg')
        else:
            sTestFile = os.path.join(sTestPath, 'acrobatics.jpg')
        return check_file(sTestFile)

    def _convert_expansion(self, sExpansionName):
        """Convert the Full Expansion name into the abbreviation needed."""
        if sExpansionName == '':
            return ''
        else:
            bOK = False
            try:
                oExpansion = IExpansion(sExpansionName)
                oPrinting = None
                bOK = True
            except SQLObjectNotFound:
                if '(' in sExpansionName:
                    sSplitExp, sPrintName = [ x.strip() for x in sExpansionName.split('(', 1)
                                            ]
                    sPrintName = sPrintName.replace(')', '')
                    try:
                        oExpansion = IExpansion(sSplitExp)
                        oPrinting = IPrinting((oExpansion, sPrintName))
                        bOK = True
                    except SQLObjectNotFound:
                        pass

            if not bOK:
                logging.warn('Expansion %s no longer found in the database', sExpansionName)
                return ''
            if oExpansion.name in self.SPECIAL_PROMOS:
                sExpName = oExpansion.name.lower()
            else:
                sExpName = oExpansion.shortname.lower()
            if oPrinting:
                sExpName += '_' + oPrinting.name.lower()
            sExpName = sExpName.replace(' ', '_').replace('-', '_')
            sExpName = sExpName.replace("'", '')
            return sExpName

    def _make_card_urls(self, _sFullFilename):
        """Return a url pointing to the scan of the image"""
        sFilename = self._norm_cardname(self._sCardName)[0]
        if sFilename == '':
            return None
        else:
            if self._bShowExpansions:
                aUrlExps = [self._convert_expansion(self._sCurExpPrint)]
            else:
                aUrlExps = [ self._convert_expansion(x) for x in self._aExpPrints ]
            aUrls = []
            for sCurExpansionPath in aUrlExps:
                if sCurExpansionPath == '':
                    return None
                sUrl = '%s/cardimages/%s/%s' % (SUTEKH_IMAGE_SITE,
                 sCurExpansionPath,
                 sFilename)
                aUrls.append(sUrl)

            return aUrls

    def _make_date_url(self):
        """Date info file lives with the images"""
        return '%s/cardimages/%s' % (SUTEKH_IMAGE_SITE, IMAGE_DATE_FILE)

    def _parse_date_data(self, sDateData):
        """Parse date file into entries"""
        try:
            self._dDateCache = {}
            for sLine in sDateData.splitlines():
                sLine = sLine.strip()
                if not sLine:
                    continue
                _sSize, sDay, sTime, sName = sLine.split()
                oCacheDate = datetime.datetime.strptime('%s %s' % (sDay, sTime), '%Y-%m-%d %H:%M:%S')
                sExpansion, sCardName = sName.replace('./', '').split('/')
                sKey = os.path.join(self._sPrefsPath, sExpansion, sCardName)
                self._dDateCache[sKey] = oCacheDate

            if len(self._dDateCache) > 100:
                return True
        except Exception as oErr:
            logging.warn('Error parsing date cache file %s', oErr)

        return False

    def _norm_cardname(self, sCardName):
        """Normalise the card name"""
        sCardName = sCardName.replace('™', 'tm')
        sFilename = unaccent(sCardName)
        if sFilename.startswith('the '):
            sFilename = sFilename[4:] + 'the'
        else:
            if sFilename.startswith('an '):
                sFilename = sFilename[3:] + 'an'
            sFilename = sFilename.replace('(advanced)', 'adv')
            for sChar in (' ', '.', ',', "'", '(', ')', '-', ':', '!', '"', '/'):
                sFilename = sFilename.replace(sChar, '')

        sFilename = sFilename + '.jpg'
        return [sFilename]


class ImageConfigDialog(BaseImageConfigDialog):
    """Dialog for configuring the Image plugin."""
    sDefUrlId = 'sutekh.vtes.za.net'
    sImgDownloadSite = 'sutekh.vtes.za.net'
    sDefaultUrl = '%s/zipped/%s' % (SUTEKH_IMAGE_SITE, 'cardimages.zip')

    def __init__(self, oImagePlugin, bFirstTime=False, bDownloadUpgrade=False):
        super(ImageConfigDialog, self).__init__(oImagePlugin, bFirstTime)
        self.oChoice.set_request_headers(SUTEKH_USER_AGENT)
        if bDownloadUpgrade:
            self.vbox.remove(self.oDescLabel)
            self.vbox.remove(self.oChoice)
            self.vbox.remove(self.oDownload)
            self.vbox.remove(self.oDownloadExpansions)
            self.oDescLabel.set_markup('<b>Choose how to configure the cardimages plugin</b>\nThe card images plugin can now download missing images from sutekh.vtes.za.net.\nDo you wish to enable this (you will not be prompted again)?')
            self.vbox.pack_start(self.oDescLabel, False, False)
            self.vbox.pack_start(self.oDownload, False, False)
            self.vbox.pack_start(self.oDownloadExpansions, False, False)
            self.set_size_request(400, 200)
            self.show_all()


class CardImagePlugin(SutekhPlugin, BaseImagePlugin):
    """Plugin providing access to CardImageFrame."""
    DOWNLOAD_SUPPORTED = True
    _cImageFrame = CardImageFrame

    @classmethod
    def update_config(cls):
        super(CardImagePlugin, cls).update_config()
        cls.dGlobalConfig[DOWNLOAD_EXPANSIONS] = 'boolean(default=True)'

    def setup(self):
        """Prompt the user to download/setup images the first time"""
        sPrefsPath = self.get_config_item(CARD_IMAGE_PATH)
        if not os.path.exists(sPrefsPath):
            oDialog = ImageConfigDialog(self, True, False)
            self.handle_response(oDialog)
            sPrefsPath = self.get_config_item(CARD_IMAGE_PATH)
            ensure_dir_exists(sPrefsPath)
        else:
            oDownloadImages = self.get_config_item(DOWNLOAD_IMAGES)
            if oDownloadImages is None:
                oDialog = ImageConfigDialog(self, False, True)
                self.set_config_item(DOWNLOAD_IMAGES, False)
                self.handle_response(oDialog)
        return

    def config_activate(self, _oMenuWidget):
        """Configure the plugin dialog."""
        oDialog = ImageConfigDialog(self, False, False)
        self.handle_response(oDialog)

    def handle_response(self, oDialog):
        """Handle the response from the config dialog"""
        iResponse = oDialog.run()
        if iResponse == gtk.RESPONSE_OK:
            oFile, bDir, bDownload, bDownloadExpansions = oDialog.get_data()
            if bDir:
                if self._accept_path(oFile):
                    self.image_frame.update_config_path(oFile)
                    self._activate_menu()
            elif oFile:
                if self._unzip_file(oFile):
                    self._activate_menu()
                else:
                    do_complaint_error('Unable to successfully unzip data')
                oFile.close()
            else:
                do_complaint_error('Unable to configure card images plugin')
            self.set_config_item(DOWNLOAD_IMAGES, bDownload)
            self.set_config_item(DOWNLOAD_EXPANSIONS, bDownloadExpansions)
            self.image_frame.check_images()
        oDialog.destroy()


plugin = CardImagePlugin