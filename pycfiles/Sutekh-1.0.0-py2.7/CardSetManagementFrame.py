# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/CardSetManagementFrame.py
# Compiled at: 2019-12-11 16:37:48
"""Pane for a list of card sets"""
import gtk
from ..core.BaseTables import PhysicalCardSet
from .BasicFrame import BasicFrame
from .CardSetManagementController import CardSetManagementController
from .CardSetManagementMenu import CardSetManagementMenu
from .AutoScrolledWindow import AutoScrolledWindow

class CardSetManagementFrame(BasicFrame):
    """Pane for the List of card sets.

       Provides the actions associated with this Pane - creating new
       card sets, filtering, etc.
       """
    _sName = 'Card Set List'
    _oSetClass = PhysicalCardSet
    _cModelType = 'Card Set List'

    def __init__(self, oMainWindow):
        super(CardSetManagementFrame, self).__init__(oMainWindow)
        self._oMenu = None
        self._oScrolledWindow = None
        self._oController = CardSetManagementController(oMainWindow, self)
        self.set_name('card sets list')
        self.init_plugins()
        self._oMenu = CardSetManagementMenu(self, self._oMainWindow, self._oController)
        self.add_parts()
        return

    type = property(fget=lambda self: self._sName, doc='Frame Type')
    menu = property(fget=lambda self: self._oMenu, doc='Frame Menu')
    view = property(fget=lambda self: self._oController.view, doc='Associated View Object')

    def add_parts(self):
        """Add a list object to the frame"""
        oMbox = gtk.VBox(False, 2)
        self.set_title(self._sName)
        oMbox.pack_start(self._oTitle, False, False)
        oMbox.pack_start(self._oMenu, False, False)
        self._oScrolledWindow = AutoScrolledWindow(self._oController.view)
        oMbox.pack_start(self._oScrolledWindow, expand=True)
        self.add(oMbox)
        self.show_all()
        self.set_drag_handler(self._oMenu)
        self.set_drop_handler(self._oMenu)

    def reload(self):
        """Reload the frame contents"""
        oVertAdj = self._oScrolledWindow.get_vadjustment()
        oHorzAdj = self._oScrolledWindow.get_hadjustment()
        tVertVals = (oVertAdj.value, oVertAdj.page_size)
        tHorzVals = (oHorzAdj.value, oHorzAdj.page_size)
        self.view.reload_keep_expanded(True)
        oVertAdj.value, oVertAdj.page_size = tVertVals
        oHorzAdj.value, oHorzAdj.page_size = tHorzVals
        oVertAdj.changed()
        oHorzAdj.changed()
        oVertAdj.value_changed()
        oHorzAdj.value_changed()

    def get_menu_name(self):
        """Get the menu key"""
        return self._sName