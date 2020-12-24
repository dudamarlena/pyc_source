# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/plugins/PrintProxyDeck.py
# Compiled at: 2019-12-11 16:37:54
"""Print the deck using the image plugin to get images for the cards."""
import gtk
from sutekh.base.core.BaseTables import PhysicalCardSet
from sutekh.base.core.BaseAdapters import IAbstractCard, IPhysicalCard, IPrinting
from sutekh.base.gui.SutekhDialog import do_complaint_error
from sutekh.base.gui.plugins.BaseImages import get_printing_info, check_file
from sutekh.gui.PluginManager import SutekhPlugin
PRINT_LATEST, PRINT_EXACT = range(2)
TEXT_LATEST = 'Use Latest Card Image'
TEXT_EXACT = 'Use Exact Image'
IMG_WIDTH = 720
IMG_HEIGHT = 1008

class PrintProxyPlugin(SutekhPlugin):
    """Plugin for printing a deck using proxy images"""
    dTableVersions = {PhysicalCardSet: (7, )}
    aModelsSupported = (
     PhysicalCardSet,)
    dOptions = {TEXT_LATEST: PRINT_LATEST, 
       TEXT_EXACT: PRINT_EXACT}
    sMenuName = 'Print Card Set as Proxies'
    sHelpCategory = 'card_sets:actions'
    sHelpText = 'If you have downloaded the card images, this allows\n                   you to print the card set using the card images for\n                   use as proxies.\n\n                   If images are available for all the expansions, you can\n                   choose to either print the exact expansion specified\n                   for the card, or use the latest image for the given card.\n                   By default, the most recent card image will be used.\n\n                   Cards without an expansion ("Unspecified Expansion") will\n                   always be printed using the latest available image.\n\n                   If the exact image cannot be found, another image of the\n                   card from a different expansion will be used if possible.\n                   The plugin will throw an error only if no suitable image\n                   can be found.\n\n                   This will only print the current filtered view of the\n                   card set, which can be used to restict the card printed\n                   to only those required.'

    @classmethod
    def get_help_list_text(cls):
        return 'Print the card set using the images of the cards, for use                   as proxies.'

    def __init__(self, *args, **kwargs):
        super(PrintProxyPlugin, self).__init__(*args, **kwargs)
        self._oSettings = None
        self._oImageFrame = None
        for oPlugin in self.parent.plugins:
            if hasattr(oPlugin, 'image_frame'):
                self._oImageFrame = oPlugin.image_frame
                break

        self._aFiles = []
        self._iPrintExpansion = PRINT_LATEST
        self._aMissing = set()
        return

    def get_menu_item(self):
        """Register on the 'Actions' Menu"""
        if not self._oImageFrame:
            return None
        else:
            oPrint = gtk.MenuItem('Print Card Set as Proxies')
            oPrint.connect('activate', self.activate)
            return ('Actions', oPrint)

    def activate(self, _oWidget):
        """Generate the PDF file"""
        oPrintOp = gtk.PrintOperation()
        if self._oSettings:
            oPrintOp.set_print_settings(self._oSettings)
        oPrintOp.connect('begin-print', self.begin_print)
        oPrintOp.connect('end-print', self.end_print)
        oPrintOp.connect('draw-page', self.draw_page)
        oPrintOp.set_custom_tab_label('Proxy Set Print Settings')
        dCustomData = {}
        oPrintOp.connect('create-custom-widget', self._add_print_widgets, dCustomData)
        oPrintOp.connect('custom-widget-apply', self._get_print_widgets, dCustomData)
        oRes = oPrintOp.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, self.parent)
        if self._aMissing:
            aErrors = ['Error printing card set.',
             'Unable to load images for the following cards:']
            aErrors.extend(sorted(self._aMissing))
            sErr = ('\n').join(aErrors)
            do_complaint_error(sErr)
        elif oRes == gtk.PRINT_OPERATION_RESULT_ERROR:
            do_complaint_error('Error printing card set:\n' + oPrintOp.get_error())
        elif oRes == gtk.PRINT_OPERATION_RESULT_APPLY:
            self._oSettings = oPrintOp.get_print_settings()

    def begin_print(self, oPrintOp, _oContext):
        """Set up printing context.

           This includes determining pagination and the number of pages.
           """
        self._aMissing = set()
        oPrintOp.set_unit(gtk.UNIT_POINTS)
        oPrintOp.set_n_pages(1)
        oIter = self.model.get_card_iterator(self.model.get_current_filter())
        aCards = sorted([ IPhysicalCard(x) for x in oIter ], key=lambda y: IAbstractCard(y).name)
        for oTheCard in aCards:
            oCard = oTheCard
            if self._iPrintExpansion == PRINT_LATEST:
                sLatestPrinting = get_printing_info(oTheCard.abstractCard)[0]
                oExp = IPrinting(sLatestPrinting)
                oCard = IPhysicalCard((oTheCard.abstractCard, oExp))
            sFilename = self._oImageFrame.lookup_filename(oCard)[0]
            if not check_file(sFilename):
                bOk = False
                for sExpName in get_printing_info(oTheCard.abstractCard):
                    oPrinting = IPrinting(sExpName)
                    oCard = IPhysicalCard((oTheCard.abstractCard, oPrinting))
                    sFilename = self._oImageFrame.lookup_filename(oCard)[0]
                    if check_file(sFilename):
                        bOk = True
                        self._aFiles.append(sFilename)
                        break

                if not bOk:
                    self._aMissing.add(oTheCard.abstractCard.name)
                    continue
            else:
                self._aFiles.append(sFilename)

        if self._aMissing:
            oPrintOp.cancel()
            return
        iNumCards = len(aCards)
        iNumPages = iNumCards // 9
        if iNumPages * 9 < iNumCards:
            iNumPages += 1
        oPrintOp.set_n_pages(iNumPages)

    def end_print(self, _oPrintOp, _oContext):
        """Clean up resources allocated in begin_print."""
        self._aFiles = []
        self._iPrintExpansion = PRINT_LATEST

    def draw_page(self, _oPrintOp, oContext, iPageNum):
        """Page drawing callback."""
        aTheseFiles = self._aFiles[iPageNum * 9:(iPageNum + 1) * 9]
        oCairoContext = oContext.get_cairo_context()
        iOffsetX = 0
        iOffsetY = 0
        fContextWidth = oContext.get_width()
        fContextHeight = oContext.get_height()
        oCairoContext.scale(fContextWidth / (3 * IMG_WIDTH + 10), fContextHeight / (3 * IMG_HEIGHT + 10))
        for sFilename in aTheseFiles:
            oPixbuf = gtk.gdk.pixbuf_new_from_file(sFilename)
            oPixbuf = oPixbuf.scale_simple(IMG_WIDTH, IMG_HEIGHT, gtk.gdk.INTERP_HYPER)
            oCairoContext.set_source_pixbuf(oPixbuf, iOffsetX, iOffsetY)
            oCairoContext.rectangle(iOffsetX, iOffsetY, IMG_WIDTH, IMG_HEIGHT)
            oCairoContext.fill()
            iOffsetX += IMG_WIDTH + 5
            if iOffsetX > 3 * IMG_WIDTH:
                iOffsetX = 0
                iOffsetY += IMG_HEIGHT + 5

    def _add_print_widgets(self, _oOp, dCustomData):
        """Add widgets to the custom options tab"""
        oVBox = gtk.VBox(False, 2)
        oLabel = gtk.Label()
        oLabel.set_markup('<b>Proxy printing Options:</b>')
        oLabel.set_alignment(0.0, 0.5)
        oVBox.pack_start(oLabel, expand=False, padding=10)
        aExpButtons = []
        oFirstBut = gtk.RadioButton(None, TEXT_LATEST, False)
        oFirstBut.set_active(True)
        oVBox.pack_start(oFirstBut, expand=False)
        aExpButtons.append(oFirstBut)
        for sText in self.dOptions:
            if sText == oFirstBut.get_label():
                continue
            oBut = gtk.RadioButton(oFirstBut, sText, False)
            oBut.set_active(False)
            oVBox.pack_start(oBut, expand=False)
            aExpButtons.append(oBut)

        dCustomData['aExpButtons'] = aExpButtons
        oVBox.show_all()
        return oVBox

    def _get_print_widgets(self, _oOp, _oBox, dCustomData):
        """Get the selection from the custom area"""
        for oButton in dCustomData['aExpButtons']:
            if oButton.get_active():
                sLabel = oButton.get_label()
                self._iPrintExpansion = self.dOptions[sLabel]


plugin = PrintProxyPlugin