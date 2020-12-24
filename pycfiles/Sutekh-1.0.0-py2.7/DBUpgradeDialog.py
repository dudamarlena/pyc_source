# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/DBUpgradeDialog.py
# Compiled at: 2019-12-11 16:37:48
"""Database to prompt for database upgrades"""
import gtk
from .SutekhDialog import SutekhDialog

class DBUpgradeDialog(SutekhDialog):
    """Dialog which prompts the user at the end of a database upgrade.

       Display any messages from the upgrade process, and ask the user
       whether to cancel, commit the changes, or test using the memory copy.
       """

    def __init__(self, aMessages):
        super(DBUpgradeDialog, self).__init__('Memory Copy Created', None, gtk.DIALOG_MODAL, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
         gtk.STOCK_OK, gtk.RESPONSE_OK))
        oHBox = gtk.HBox(False, 0)
        oIcon = gtk.Image()
        oIcon.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_DIALOG)
        oHBox.pack_start(oIcon)
        sLabel = 'Memory Copy successfully created. Commit Changes?'
        oLabel = gtk.Label(sLabel)
        oHBox.pack_start(oLabel)
        if aMessages:
            sLabelInfo = 'The following messages were reported in creating the copy:\n'
            for sStr in aMessages:
                sLabelInfo += '<b>' + sStr + '</b>\n'

            oInfolabel = gtk.Label()
            oInfolabel.set_markup(sLabelInfo)
            self.vbox.pack_start(oInfolabel)
        self.add_button('Test upgraded database?\n(No changes are committed)', 1)
        self.set_default_response(gtk.RESPONSE_OK)
        self.vbox.pack_start(oHBox)
        self.show_all()
        return