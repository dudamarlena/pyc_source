# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/UpdateDialog.py
# Compiled at: 2019-12-11 16:37:48
"""Database to prompt for datapack updates and so forth."""
import gtk
from .SutekhDialog import SutekhDialog

class UpdateDialog(SutekhDialog):
    """Dialog which prompts the user if datapack or other updates
       are available."""

    def __init__(self, aMessages):
        super(UpdateDialog, self).__init__('Updates available', None, gtk.DIALOG_MODAL, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
         gtk.STOCK_OK, gtk.RESPONSE_OK))
        oHBox = gtk.HBox(False, 0)
        oIcon = gtk.Image()
        oIcon.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_DIALOG)
        oHBox.pack_start(oIcon)
        self.vbox.pack_start(oHBox)
        sLabel = 'Updates are available. Download now?'
        oLabel = gtk.Label(sLabel)
        oHBox.pack_start(oLabel)
        sLabelInfo = 'The following updates are available:\n\n'
        sLabelInfo += ('\n').join(aMessages)
        oInfolabel = gtk.Label()
        oInfolabel.set_markup(sLabelInfo)
        self.vbox.pack_start(oInfolabel)
        self.set_default_response(gtk.RESPONSE_OK)
        self.show_all()
        return