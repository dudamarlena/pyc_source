# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/BaseCardTextFrame.py
# Compiled at: 2019-12-11 16:37:48
"""Frame to hold the CardTextView."""
from .ScrolledFrame import ScrolledFrame
from .MessageBus import MessageBus, CARD_TEXT_MSG

class BaseCardTextFrame(ScrolledFrame):
    """ScrolledFrame which adds listeners for the 'set_card_text' signal."""
    _sName = 'Card Text'

    def __init__(self, oView, oMainWindow):
        super(BaseCardTextFrame, self).__init__(oView, oMainWindow)
        self._oView.clear_text()

    def frame_setup(self):
        """Subscribe to the set_card_text signal"""
        self._oView.clear_text()
        MessageBus.subscribe(CARD_TEXT_MSG, 'set_card_text', self.set_card_text)
        super(BaseCardTextFrame, self).frame_setup()

    def cleanup(self, bQuit=False):
        """Cleanup the listeners"""
        MessageBus.unsubscribe(CARD_TEXT_MSG, 'set_card_text', self.set_card_text)
        super(BaseCardTextFrame, self).cleanup(bQuit)

    def set_card_text(self, oCard):
        """Hand off card text update to the view"""
        if oCard:
            self._oView.set_card_text(oCard)