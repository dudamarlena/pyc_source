# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/plugins/BaseSnapshot.py
# Compiled at: 2019-12-11 16:37:39
"""Create a snapshot of the current card set."""
import datetime, gtk
from ...core.BaseTables import PhysicalCardSet
from ...core.CardSetHolder import CardSetHolder
from ..BasePluginManager import BasePlugin
from ..SutekhDialog import do_complaint
from ..GuiCardSetFunctions import get_import_name

class BaseSnapshot(BasePlugin):
    """Creates a snapshot of the card set.

       The snapshot is a copy of the current state of the card set, with the
       date and time appended to the name, and it is a child of the card set.
       """
    dTableVersions = {PhysicalCardSet: (6, 7)}
    aModelsSupported = (
     PhysicalCardSet,)

    def get_menu_item(self):
        """Return a gtk.MenuItem to activate this plugin."""
        oMenuItem = gtk.MenuItem('Take a snapshot of this card set')
        oMenuItem.connect('activate', self.activate)
        return ('Actions', oMenuItem)

    def activate(self, _oWidget):
        """Create the snapshot."""
        oMyCS = self._get_card_set()
        sTime = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
        oTempHolder = CardSetHolder()
        oTempHolder.name = '%s (%s)' % (oMyCS.name, sTime)
        get_import_name(oTempHolder)
        if not oTempHolder.name:
            return
        oNewPCS = PhysicalCardSet(name=oTempHolder.name, parent=oMyCS)
        oNewPCS.author = oMyCS.author
        oNewPCS.comment = oMyCS.comment
        oNewPCS.annotations = oMyCS.annotations
        oNewPCS.syncUpdate()
        self._commit_cards(oNewPCS, oMyCS.cards)
        self._reload_pcs_list()
        sMesg = 'Snapshot <b>%s</b> created' % self._escape(oTempHolder.name)
        do_complaint(sMesg, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, True)