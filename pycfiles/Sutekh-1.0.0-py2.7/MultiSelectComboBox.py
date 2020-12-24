# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/MultiSelectComboBox.py
# Compiled at: 2019-12-11 16:37:48
"""Generic multiselect combobox for use in FilterEditor (and elsewhere)"""
import sys, gtk
from .AutoScrolledWindow import AutoScrolledWindow
from .ScrolledList import ScrolledListView

def mouse_in_button(oButton):
    """Check if mouse pointer is inside the button"""
    iXPos, iYPos = oButton.get_pointer()
    oButtonGeom = oButton.allocation
    return iXPos >= 0 and iYPos >= 0 and iXPos < oButtonGeom.width and iYPos < oButtonGeom.height


class MultiSelectComboBox(gtk.HBox):
    """Implementation of a multiselect combo box widget."""

    def __init__(self, oParentWin):
        super(MultiSelectComboBox, self).__init__()
        self._oButton = gtk.Button(' - ')
        self._oButton.connect('clicked', self.__show_list)
        self.pack_start(self._oButton)
        self._oTreeView = ScrolledListView(' ... ')
        self._oTreeView.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        oScrolled = AutoScrolledWindow(self._oTreeView)
        self._aOldSelection = []
        self._oDialog = gtk.Dialog('Select ...', None, gtk.DIALOG_MODAL | gtk.DIALOG_NO_SEPARATOR | gtk.DIALOG_DESTROY_WITH_PARENT)
        self._oDialog.set_decorated(False)
        self._oDialog.action_area.set_size_request(-1, 0)
        self._oDialog.vbox.pack_start(oScrolled)
        self._oDialog.connect('key-press-event', self.__hide_on_return)
        self._oDialog.connect('event-after', self.__grab_event)
        self._bInButton = False
        self._oParentWin = oParentWin
        return

    def __grab_event(self, _oWidget, oEvent):
        """Hook into the event-after chain, so we can check if any uncaught
           events refer to the original button."""
        if oEvent.type == gtk.gdk.BUTTON_PRESS or sys.platform.startswith('win') and oEvent.type == gtk.gdk.BUTTON_RELEASE:
            if oEvent.button == 1:
                if mouse_in_button(self._oButton):
                    self.__hide_list()
        elif oEvent.type == gtk.gdk.ENTER_NOTIFY:
            if mouse_in_button(self._oButton):
                self._bInButton = True
                self._oButton.set_state(gtk.STATE_PRELIGHT)
        elif oEvent.type == gtk.gdk.LEAVE_NOTIFY and self._bInButton:
            self._bInButton = False
            self._oButton.set_state(gtk.STATE_NORMAL)
        return False

    def __show_list(self, _oButton):
        """Drop down the list of possible selections."""
        self._aOldSelection = self.get_selection()
        oParent = self.get_parent_window()
        tWinPos = oParent.get_origin()
        tButtonPos = (
         self._oButton.allocation.x, self._oButton.allocation.y)
        tShift = (5, self._oButton.allocation.height)
        tDialogPos = (
         tWinPos[0] + tButtonPos[0] + tShift[0],
         tWinPos[1] + tButtonPos[1] + tShift[1])
        self._oDialog.set_keep_above(True)
        self._oDialog.set_transient_for(self._oParentWin)
        self._oDialog.show_all()
        self._oDialog.move(tDialogPos[0], tDialogPos[1])
        self._bInButton = False

    def __hide_on_return(self, _oWidget, oEvent):
        """Hide the list when return or escape is pressed."""
        if oEvent.type is gtk.gdk.KEY_PRESS:
            sKeyName = gtk.gdk.keyval_name(oEvent.keyval)
            if sKeyName in ('Return', 'Escape'):
                if sKeyName == 'Escape':
                    self.set_selected_rows(self._aOldSelection)
                self.__hide_list()
                return True
        return False

    def __hide_list(self):
        """Hide the list of options"""
        self._oDialog.hide_all()
        self.__update_button_text()

    def __update_button_text(self):
        """Update the text to reflect the selected items."""
        aSelection = self.get_selection()
        if aSelection:
            self._oButton.set_label((', ').join(aSelection))
        else:
            self._oButton.set_label(' - ')

    def fill_list(self, aVals):
        """Fill the list store with the given values"""
        self._oTreeView.store.fill_list(aVals)

    def set_list_size(self, iWidth, iHeight):
        """Set size of the drop-down list"""
        self._oDialog.set_size_request(iWidth, iHeight)

    def set_sensitive(self, bValue):
        """Control the sensitivity of the button"""
        self._oButton.set_sensitive(bValue)

    def get_selection(self):
        """Return a list of the selected elements of the list"""
        return self._oTreeView.get_selected_data()

    def set_selected_rows(self, aRowsToSelect):
        """Set the selected rows in the drop-down to aRowsToSelect"""
        self._oTreeView.set_selected_rows(aRowsToSelect)