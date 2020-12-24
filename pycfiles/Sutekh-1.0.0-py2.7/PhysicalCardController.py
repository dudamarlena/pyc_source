# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/PhysicalCardController.py
# Compiled at: 2019-12-11 16:37:48
"""Controller for the Physical Card Collection"""
from .PhysicalCardView import PhysicalCardView
from .MessageBus import MessageBus, CARD_TEXT_MSG

class PhysicalCardController(object):
    """Controller for the Physical Card Collection.

       Provide settings needed for the Physical Card List,
       and suitable card manipulation methods.
       """

    def __init__(self, oFrame, oMainWindow):
        self.__oMainWin = oMainWindow
        self.__oFrame = oFrame
        self.__oView = PhysicalCardView(self, oMainWindow, oMainWindow.config_file)
        self.__oModel = self.__oView.get_model()
        self._sFilterType = 'PhysicalCard'
        self.model.set_controller(self)

    view = property(fget=lambda self: self.__oView, doc='Associated View')
    model = property(fget=lambda self: self.__oModel, doc="View's Model")
    frame = property(fget=lambda self: self.__oFrame, doc='Associated Frame')
    filtertype = property(fget=lambda self: self._sFilterType, doc='Associated Type')

    def cleanup(self):
        """Remove the signal handlers."""
        self.model.cleanup()

    def set_card_text(self, oCard):
        """Set the card text to reflect the selected card."""
        MessageBus.publish(CARD_TEXT_MSG, 'set_card_text', oCard)

    def toggle_expansion(self, oWidget):
        """Toggle whether the expansion information is shown."""
        self.__oModel.bExpansions = oWidget.active
        self.__oView.reload_keep_expanded()

    def toggle_icons(self, oWidget):
        """Toggle the icons display"""
        self.__oModel.bUseIcons = oWidget.active
        self.__oView.reload_keep_expanded()