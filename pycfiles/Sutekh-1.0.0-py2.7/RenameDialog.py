# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/RenameDialog.py
# Compiled at: 2019-12-11 16:37:47
"""Dialog to handle the Rename / Replace / Cancel options when importing
   a card set with a name that's already in use."""
import gtk
from .SutekhDialog import SutekhDialog, do_complaint_error
from ..core.CardSetUtilities import check_cs_exists
from ..core.BaseTables import MAX_ID_LENGTH
RENAME, REPLACE, PROMPT = (1, 2, 3)

class RenameDialog(SutekhDialog):
    """Class to handle the card set renaming"""

    def __init__(self, sOldName):
        self.oEntry = gtk.Entry(MAX_ID_LENGTH)
        if sOldName:
            sMsg = 'Card Set %s already exists.\nPlease choose a new name or choose to replace the card set.\nChoose cancel to abort this import.' % sOldName
            tButtons = ('Rename card set', RENAME, 'Replace Existing Card Set',
             REPLACE, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
            self.oEntry.set_text(sOldName)
        else:
            sMsg = 'No name given for the card set\nPlease specify a name.\nChoose cancel to abort this import.'
            tButtons = (
             'Name card set', RENAME, gtk.STOCK_CANCEL,
             gtk.RESPONSE_CANCEL)
        super(RenameDialog, self).__init__('Choose New Card Set Name', None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, tButtons)
        oLabel = gtk.Label(sMsg)
        self.sNewName = ''
        self.oEntry.connect('activate', self.handle_response, RENAME)
        self.connect('response', self.handle_response)
        self.vbox.pack_start(oLabel)
        self.vbox.pack_start(self.oEntry)
        self.show_all()
        return

    def handle_response(self, _oWidget, oResponse):
        """Handle the user's clicking on OK or CANCEL in the dialog."""
        if oResponse == RENAME:
            sNewName = self.oEntry.get_text().strip()
            if not sNewName:
                do_complaint_error('No name specified.\nPlease choose a suitable name')
                self.run()
            elif check_cs_exists(sNewName):
                do_complaint_error('The name %s is in use.\nPlease choose a different name' % sNewName)
                self.run()
            else:
                self.sNewName = sNewName