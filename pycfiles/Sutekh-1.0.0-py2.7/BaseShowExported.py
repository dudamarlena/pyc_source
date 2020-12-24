# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/plugins/BaseShowExported.py
# Compiled at: 2019-12-11 16:37:39
"""Plugin for displaying the exported version of a card set in a gtk.TextView.
   Intended to make cutting and pasting easier."""
import StringIO, gtk
from ...core.BaseTables import PhysicalCardSet
from ...core.CardSetHolder import CardSetWrapper
from ...io.WriteCSV import WriteCSV
from ..BasePluginManager import BasePlugin
from ..AutoScrolledWindow import AutoScrolledWindow
from ..SutekhDialog import SutekhDialog

class BaseShowExported(BasePlugin):
    """Display the various exported versions of a card set.

       The card set is shown in a textview, and the user can toggle between
       the different formats. This is designed to make it trivial to
       cut-n-paste the card set into something else (such as a web-browser).
       """
    dTableVersions = {}
    aModelsSupported = (
     PhysicalCardSet,)
    EXPORTERS = {'CSV Export (with headers)': WriteCSV}

    def get_menu_item(self):
        """Register on the 'Analyze' menu"""
        oShowExported = gtk.MenuItem('Display card set in alternative format')
        oShowExported.connect('activate', self.activate)
        return ('Actions', oShowExported)

    def activate(self, _oWidget):
        """Handle response from menu"""
        oCardSet = self._get_card_set()
        if not oCardSet:
            return
        else:
            oDlg = SutekhDialog('Exported CardSet: %s' % self.view.sSetName, self.parent, gtk.DIALOG_DESTROY_WITH_PARENT)
            oDlg.set_default_size(700, 600)
            oTextBuffer = ExportBuffer()
            oTextView = gtk.TextView()
            oTextView.set_buffer(oTextBuffer)
            oTextView.set_editable(False)
            oTextView.set_wrap_mode(gtk.WRAP_NONE)
            oTextView.set_border_width(5)
            oTextView.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
            oDlg.vbox.pack_start(AutoScrolledWindow(oTextView))
            oTable = gtk.Table(len(self.EXPORTERS) // 2, 2)
            iXPos, iYPos = (0, 0)
            oFirstBut = None
            for sName in sorted(self.EXPORTERS):
                if not oFirstBut:
                    oBut = gtk.RadioButton(None, sName)
                    oFirstBut = oBut
                    oFirstBut.set_active(True)
                    self._set_text(sName, oCardSet, oTextBuffer)
                else:
                    oBut = gtk.RadioButton(oFirstBut, sName)
                oBut.connect('toggled', self._button_toggled, sName, oCardSet, oTextBuffer)
                oTable.attach(oBut, iXPos, iXPos + 1, iYPos, iYPos + 1)
                iXPos += 1
                if iXPos > 1:
                    iXPos = 0
                    iYPos += 1

            oDlg.vbox.pack_start(oTable, False)
            oDlg.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
            oDlg.connect('response', lambda oW, oR: oDlg.destroy())
            oDlg.show_all()
            oDlg.run()
            return

    def _button_toggled(self, oBut, sName, oCardSet, oTextBuffer):
        """Handle user changing the toggle button state"""
        if not oBut.get_active():
            return
        self._set_text(sName, oCardSet, oTextBuffer)

    def _set_text(self, sName, oCardSet, oTextBuffer):
        """Internals of setting the buffer to the correct text"""
        cWriter = self.EXPORTERS[sName]
        oWriter = cWriter()
        fOut = StringIO.StringIO()
        oWriter.write(fOut, CardSetWrapper(oCardSet))
        oTextBuffer.set_text(fOut.getvalue())
        fOut.close()


class ExportBuffer(gtk.TextBuffer):
    """Buffer object for showing the exported card set text"""

    def __init__(self):
        super(ExportBuffer, self).__init__(None)
        self.create_tag('text', left_margin=0)
        return

    def set_text(self, sCardSetText):
        """Set the buffer contents to the card set text"""
        oStart, oEnd = self.get_bounds()
        self.delete(oStart, oEnd)
        oIter = self.get_iter_at_offset(0)
        self.insert_with_tags_by_name(oIter, sCardSetText, 'text')