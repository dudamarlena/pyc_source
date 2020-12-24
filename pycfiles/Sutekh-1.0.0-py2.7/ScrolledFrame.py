# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/ScrolledFrame.py
# Compiled at: 2019-12-11 16:37:48
"""Simple frame that holds a widget in a scrolled window."""
import gtk
from .AutoScrolledWindow import AutoScrolledWindow
from .BasicFrame import BasicFrame

class ScrolledFrame(BasicFrame):
    """Frame which holds a view in a scrolled window.

       Provides basic frame actions (drag-n-drop, focus behaviour), and
       sets names and such correctly.
       """
    _sName = 'scrolled'

    def __init__(self, oView, oMainWindow):
        super(ScrolledFrame, self).__init__(oMainWindow)
        self._oView = oView
        self.add_parts()
        self.set_name(self._sName.lower())

    type = property(fget=lambda self: self._sName, doc='Frame Type')

    def add_parts(self):
        """Add Widget + title widgets to the Frame."""
        oBox = gtk.VBox(False, 2)
        self.set_title(self._sName)
        oBox.pack_start(self._oTitle, False, False)
        oBox.pack_start(AutoScrolledWindow(self._oView), True, True)
        self.set_drop_handler(self._oView)
        self.add(oBox)
        self.show_all()

    def update_to_new_db(self):
        """Ensure we update cached results so DB changes don't cause odd
           results"""
        self._oView.update_to_new_db()

    def get_menu_name(self):
        """Get the menu key"""
        return self._sName