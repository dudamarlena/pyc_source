# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/plugins/BaseExport.py
# Compiled at: 2019-12-11 16:37:39
"""Plugin for exporting to standard writers"""
import gtk
from ...core.BaseTables import PhysicalCardSet
from ..BasePluginManager import BasePlugin
from ..GuiCardSetFunctions import export_cs

class BaseCardSetExport(BasePlugin):
    """Provides a dialog for selecting a filename, then calls on
       the appropriate writer to produce the required output."""
    dTableVersions = {PhysicalCardSet: (4, 5, 6, 7)}
    aModelsSupported = (
     PhysicalCardSet,)
    EXPORTERS = {}

    def get_menu_item(self):
        """Register with the 'Export Card Set' Menu"""
        aMenuItems = []
        for sKey, tInfo in self.EXPORTERS.iteritems():
            sMenuText = tInfo[1]
            oExport = gtk.MenuItem(sMenuText)
            oExport.connect('activate', self.make_dialog, sKey)
            aMenuItems.append(('Export Card Set', oExport))

        return aMenuItems

    def make_dialog(self, _oWidget, sKey):
        """Create the dialog"""
        oCardSet = self._get_card_set()
        if not oCardSet:
            return
        else:
            tInfo = self.EXPORTERS[sKey]
            aPatterns = None
            if len(tInfo) > 3:
                aPatterns = zip(tInfo[3::2], tInfo[4::2])
            export_cs(oCardSet, tInfo[0], self.parent, tInfo[2], aPatterns)
            return