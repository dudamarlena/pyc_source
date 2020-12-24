# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/CardTextFrame.py
# Compiled at: 2019-12-11 16:37:54
"""Frame to hold the CardTextView."""
from sutekh.gui.CardTextView import CardTextView
from sutekh.base.gui.BaseCardTextFrame import BaseCardTextFrame

class CardTextFrame(BaseCardTextFrame):
    """Frame which holds the CardTextView."""

    def __init__(self, oMainWindow, oIconManager):
        oView = CardTextView(oIconManager, oMainWindow)
        super(CardTextFrame, self).__init__(oView, oMainWindow)