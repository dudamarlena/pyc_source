# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/PhysicalCardFrame.py
# Compiled at: 2019-12-11 16:37:48
"""Frame which holds the PhysicalCardView"""
from ..core.BaseTables import PhysicalCard
from .CardListFrame import CardListFrame
from .PhysicalCardController import PhysicalCardController
from .PhysicalCardMenu import PhysicalCardMenu

class PhysicalCardFrame(CardListFrame):
    """Frame which holds the Physical Card Collection View.

       Set the title, and menus as needed for the card collection.
       """
    _cModelType = PhysicalCard
    _sName = 'Full Card List'

    def __init__(self, oMainWindow):
        super(PhysicalCardFrame, self).__init__(oMainWindow)
        self.set_title(self._sName)
        self.set_name('physical card list')
        self._oController = PhysicalCardController(self, oMainWindow)
        self.init_plugins()
        self._oMenu = PhysicalCardMenu(self, self._oController, oMainWindow)
        self.add_parts()

    def get_menu_name(self):
        """Get the menu key"""
        return self._sName

    def cleanup(self, bQuit=False):
        """Cleanup function called before pane is removed by the Main Window"""
        super(PhysicalCardFrame, self).cleanup(bQuit)
        self._oController.cleanup()