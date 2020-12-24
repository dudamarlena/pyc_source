# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/MainToolbar.py
# Compiled at: 2019-12-11 16:37:48
"""Toolbar for the Main Application Window"""
import gtk

class MainToolbar(gtk.Toolbar):
    """The Main application toolbar.

       This provides a place to minimize panes.
       """

    def __init__(self, oWindow):
        super(MainToolbar, self).__init__()
        self.set_no_show_all(True)
        self.set_style(gtk.TOOLBAR_BOTH)
        self._oMainWindow = oWindow

    def create_tool_button(self, sLabel, oIcon=None, fAction=None):
        """Create a Toolbar button with the given action."""
        oToolButton = gtk.ToolButton(oIcon, sLabel)
        if fAction is not None:
            oToolButton.connect('clicked', fAction)
        return oToolButton

    def remove_frame_button(self, sTitle):
        """Remove the button associated with the given frame title."""
        aItems = self.get_children()
        for oItem in aItems:
            if oItem.get_label() == sTitle:
                self.remove(oItem)
                break

    def refresh(self):
        """Refresh the toolbars hide/show state (needed because show all
           is turned off)."""
        aItems = self.get_children()
        if aItems:
            for oItem in aItems:
                oItem.show()

            self.show()
        else:
            self.hide()

    def frame_to_toolbar(self, oFrame, sTitle):
        """Minimize the given frame to the toolbar."""

        def unminimize(oToolbarWidget):
            """Unminimize this frame"""
            self.remove(oToolbarWidget)
            self.refresh()
            self.frame_from_toolbar(oFrame)

        oToolButton = self.create_tool_button(sTitle, oIcon=None, fAction=unminimize)
        self.add(oToolButton)
        self.refresh()
        return

    def frame_from_toolbar(self, oFrame):
        """Restore the given frame from the toolbar."""
        self._oMainWindow.restore_from_toolbar(oFrame)