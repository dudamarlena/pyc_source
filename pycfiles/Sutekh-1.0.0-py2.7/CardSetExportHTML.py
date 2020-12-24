# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/plugins/CardSetExportHTML.py
# Compiled at: 2019-12-11 16:37:54
"""Export a card set to HTML."""
import gtk
from sutekh.base.core.BaseTables import PhysicalCardSet
from sutekh.io.WriteArdbHTML import WriteArdbHTML
from sutekh.gui.PluginManager import SutekhPlugin
from sutekh.base.gui.SutekhDialog import do_complaint_error
from sutekh.base.gui.SutekhFileWidget import ExportDialog
from sutekh.base.Utility import safe_filename
from sutekh.base.gui.GuiCardSetFunctions import write_cs_to_file

class CardSetExportHTML(SutekhPlugin):
    """Export a Card set to a 'nice' HTML file.

       We create a ElementTree that represents the XHTML file,
       and then dump that to file.
       This tries to match the HTML file produced by ARDB.
       """
    dTableVersions = {PhysicalCardSet: (4, 5, 6, 7)}
    aModelsSupported = (
     PhysicalCardSet, 'MainWindow')
    dGlobalConfig = {'HTML export mode': 'string(default=None)'}

    def get_menu_item(self):
        """Register on the Plugins Menu"""
        if self._cModelType == 'MainWindow':
            oPrefs = gtk.MenuItem('Export to HTML preferences')
            oSubMenu = gtk.Menu()
            oPrefs.set_submenu(oSubMenu)
            oGroup = None
            sDefault = self.get_config_item('HTML export mode')
            if sDefault is None:
                sDefault = 'Secret Library'
                self.set_config_item('HTML export mode', sDefault)
            for sString, sVal in (('Add links to The Secret Library', 'Secret Library'),
             ('Add links to VTES Monger', 'Monger'),
             ("Don't add links in the HTML file", 'None')):
                oItem = gtk.RadioMenuItem(oGroup, sString)
                if not oGroup:
                    oGroup = oItem
                oSubMenu.add(oItem)
                oItem.set_active(False)
                if sVal == sDefault:
                    oItem.set_active(True)
                oItem.connect('toggled', self.change_prefs, sVal)

            return ('File Preferences', oPrefs)
        else:
            oExport = gtk.MenuItem('Export to HTML')
            oExport.connect('activate', self.activate)
            return ('Export Card Set', oExport)

    def activate(self, _oWidget):
        """In response to the menu, create the dialog and run it."""
        oDlg = self.make_dialog()
        oDlg.run()
        self.handle_response(oDlg.get_name())

    def change_prefs(self, _oWidget, sChoice):
        """Manage the preferences (library to link to, etc.)"""
        sCur = self.get_config_item('HTML export mode')
        if sChoice != sCur:
            self.set_config_item('HTML export mode', sChoice)

    def make_dialog(self):
        """Create the dialog prompted for the filename."""
        oDlg = ExportDialog('Filename to save as', self.parent, '%s.html' % safe_filename(self.view.sSetName))
        oDlg.add_filter_with_pattern('HTML Files', ['*.html'])
        self.oTextButton = gtk.CheckButton('Include Card _Texts?')
        self.oTextButton.set_active(False)
        oDlg.vbox.pack_start(self.oTextButton, False, False)
        oDlg.show_all()
        return oDlg

    def handle_response(self, sFileName):
        """Handle the response to the dialog"""
        if sFileName is not None:
            oCardSet = self._get_card_set()
            if not oCardSet:
                do_complaint_error('Unsupported Card Set Type')
                return
            bDoText = False
            if self.oTextButton.get_active():
                bDoText = True
            sLinkMode = self.get_config_item('HTML export mode')
            oWriter = WriteArdbHTML(sLinkMode, bDoText)
            write_cs_to_file(oCardSet, oWriter, sFileName)
        return


plugin = CardSetExportHTML