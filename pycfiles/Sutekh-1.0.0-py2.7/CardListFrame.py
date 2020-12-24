# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/CardListFrame.py
# Compiled at: 2019-12-11 16:37:48
"""Basic Card List Frame."""
import gtk
from .AutoScrolledWindow import AutoScrolledWindow
from .BasicFrame import BasicFrame

class CardListFrame(BasicFrame):
    """Base class for all the Card Lists.

       Provide common methods and basic parameters common to all the
       different CardList Frames.
       """

    def __init__(self, oMainWindow):
        super(CardListFrame, self).__init__(oMainWindow)
        self._oConfig = oMainWindow.config_file
        self._oController = None
        self._oMenu = None
        return

    view = property(fget=lambda self: self._oController.view, doc='Associated View Object')
    menu = property(fget=lambda self: self._oMenu, doc='Frame Menu')
    type = property(fget=lambda self: self._cModelType.sqlmeta.table, doc='Frame Type')

    def reload(self):
        """Reload frame contents"""
        self._oController.view.reload_keep_expanded()

    def get_toolbar_plugins(self):
        """Register plugins on the frame toolbar."""
        oBox = gtk.VBox(False, 2)
        bInsertToolbar = False
        for oPlugin in self._aPlugins:
            oWidget = oPlugin.get_toolbar_widget()
            if oWidget is not None:
                oBox.pack_start(oWidget)
                bInsertToolbar = True

        if bInsertToolbar:
            oToolbar = gtk.EventBox()
            oToolbar.add(oBox)
            self.set_drag_handler(oToolbar)
            self.set_drop_handler(oToolbar)
            oToolbar.show_all()
            return oToolbar
        else:
            return

    def do_queued_reload(self):
        """Do a deferred reload if one was set earlier"""
        if self._bNeedReload:
            self.reload()
        self._bNeedReload = False

    def add_parts(self):
        """Add the elements to the Frame."""
        oMbox = gtk.VBox(False, 2)
        oMbox.pack_start(self._oTitle, False, False)
        oMbox.pack_start(self._oMenu, False, False)
        oMbox.pack_end(AutoScrolledWindow(self._oController.view), expand=True)
        self.add(oMbox)
        self.show_all()
        oToolbar = self.get_toolbar_plugins()
        if oToolbar is not None:
            oMbox.pack_start(oToolbar, False, False)
        self._oController.view.load()
        self.set_drag_handler(self._oMenu)
        self.set_drop_handler(self._oMenu)
        return