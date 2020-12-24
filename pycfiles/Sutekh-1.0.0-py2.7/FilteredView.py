# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/FilteredView.py
# Compiled at: 2019-12-11 16:37:48
"""base classes for views."""
import unicodedata, gtk
from .CustomDragIconView import CustomDragIconView

class FilteredView(CustomDragIconView):
    """Base class for all card and card set views in Sutekh"""

    def __init__(self, oController, oMainWindow, oModel, oConfig):
        self._oController = oController
        self._oMainWin = oMainWindow
        self._oConfig = oConfig
        super(FilteredView, self).__init__(oModel)
        self._sDragPrefix = 'None:'
        self._oFilterDialog = None
        self.set_search_equal_func(self.compare, None)
        self.set_name('filtered_view')
        self.set_rules_hint(True)
        return

    mainwindow = property(fget=lambda self: self._oMainWin, doc='The parent window used for dialogs, etc.')
    controller = property(fget=lambda self: self._oController, doc='The controller used by the view.')
    frame = property(fget=lambda self: self._oController.frame, doc='The frame used by the view.')
    filterdialog = property(fget=lambda self: self._oFilterDialog, doc='The filter dialog.')

    def load(self):
        """Called when the model needs to be reloaded."""
        if hasattr(self._oMainWin, 'set_busy_cursor'):
            self._oMainWin.set_busy_cursor()
        self.freeze_child_notify()
        self.set_model(None)
        self._oModel.load()
        self.set_model(self._oModel)
        self.thaw_child_notify()
        if hasattr(self._oMainWin, 'restore_cursor'):
            self._oMainWin.restore_cursor()
        return

    def reload_keep_expanded(self, bRestoreSelection=False):
        """Reload with current expanded state.

           Attempt to reload the card list, keeping the existing structure
           of expanded rows.
           """
        sCurId = None
        aExpandedSet = self._get_expanded_list()
        if bRestoreSelection:
            aSelectedRows = self._get_selected_rows()
        oCurPath, _oCol = self.get_cursor()
        if oCurPath:
            sCurId = self.get_iter_identifier(self._oModel.get_iter(oCurPath))
        self.load()
        self._expand_list(aExpandedSet)
        if bRestoreSelection and aSelectedRows:
            self._reset_selected_rows(aSelectedRows)
        if oCurPath:
            self._oModel.foreach(self._restore_cursor, sCurId)
        return

    def _get_filter_dialog(self, _sDefaultFilter):
        """Create the filter dialog if applicable for this view.

           The default doesn't create a dialog, but some subclasses
           do."""
        return False

    def get_filter(self, oMenu, sDefaultFilter=None):
        """Get the Filter from the FilterDialog.

           oMenu is a menu item to toggle if it exists.
           sDefaultFilterName is the name of the default filter
           to set when the dialog is created. This is intended for
           use by GuiCardLookup."""
        if self._oFilterDialog is None:
            if not self._get_filter_dialog(sDefaultFilter):
                return
            self._oFilterDialog.connect('response', self._dialog_response, oMenu)
        self._oFilterDialog.show()
        return

    def _dialog_response(self, _oWidget, _iId, oMenu):
        """Handle the dialog response."""
        if self._oFilterDialog.was_cancelled():
            return
        oFilter = self._oFilterDialog.get_filter()
        self.set_filter(oFilter, oMenu)

    def run_filter(self, bState):
        """Enable or disable the current filter based on bState"""
        if self._oModel.applyfilter != bState:
            self._oModel.applyfilter = bState
            self.reload_keep_expanded()

    def get_iter_identifier(self, oIter):
        """Get the identifier for the path.

           The identifier is (sTopLevel, sChildren, ...) as required."""
        aKey = []
        while oIter:
            aKey.append(self._oModel.get_value(oIter, 0))
            oIter = self._oModel.iter_parent(oIter)

        return ('').join(aKey)

    def _get_selected_rows(self):
        """Get the currently selected rows"""
        _oModel, aSelection = self._oSelection.get_selected_rows()
        aSelectedRows = set()
        for oPath in aSelection:
            aSelectedRows.add(self.get_iter_identifier(self._oModel.get_iter(oPath)))

        return aSelectedRows

    def _reset_selected_rows(self, aSelectedRows):
        """Reselect the rows"""
        self._oModel.foreach(self._set_row_selected_status, aSelectedRows)

    def _get_expanded_list(self):
        """Create a list of expanded rows"""
        aExpandedSet = set()
        self._oModel.foreach(self._get_row_expanded_status, aExpandedSet)
        return aExpandedSet

    def _expand_list(self, aExpandedSet):
        """Expand the rows listed in aExpandedSet"""
        self._oModel.foreach(self._set_row_expanded_status, aExpandedSet)

    @staticmethod
    def to_ascii(sName):
        """Convert a Name or key to a canonical ASCII form."""
        return unicodedata.normalize('NFKD', sName).encode('ascii', 'ignore')

    def _set_row_selected_status(self, _oModel, oPath, oIter, aSelectedSet):
        """Select the rows listed in aSelectedSet"""
        sKey = self.get_iter_identifier(oIter)
        if sKey in aSelectedSet:
            self._oSelection.select_path(oPath)
        return False

    def _restore_cursor(self, _oModel, oPath, oIter, sCursorId):
        """Select the rows listed in aSelectedSet"""
        sKey = self.get_iter_identifier(oIter)
        if sKey == sCursorId:
            self.set_cursor(oPath)
            self.scroll_to_cell(oPath, None, True, 0.5, 0.0)
        return False

    def _set_row_expanded_status(self, _oModel, oPath, oIter, aExpandedSet):
        """Attempt to expand the rows listed in aExpandedSet."""
        if not self._oModel.iter_has_child(oIter):
            return False
        sKey = self.get_iter_identifier(oIter)
        if sKey in aExpandedSet:
            self.expand_to_path(oPath)
        return False

    def _get_row_expanded_status(self, _oModel, oPath, oIter, aExpandedSet):
        """Create a dictionary of rows and their expanded status."""
        if self.row_expanded(oPath):
            sKey = self.get_iter_identifier(oIter)
            aExpandedSet.add(sKey)
        return False

    def compare(self, oModel, _iColumn, sKey, oIter, _oData):
        """Compare the entered text to the names."""

        def check_children(oModel, oIter, sKey, iLenKey):
            """expand children of this row that match."""
            oChildIter = oModel.iter_children(oIter)
            while oChildIter:
                sChildName = oModel.get_name_from_iter(oChildIter)
                sChildName = sChildName[:iLenKey].lower()
                if self.to_ascii(sChildName).startswith(sKey) or sChildName.startswith(sKey):
                    oPath = oModel.get_path(oChildIter)
                    self.expand_to_path(oPath)
                if oModel.iter_n_children(oChildIter) > 0:
                    check_children(oModel, oChildIter, sKey, iLenKey)
                oChildIter = oModel.iter_next(oChildIter)

        sKey = sKey.lower()
        iLenKey = len(sKey)
        sCardSetName = self._oModel.get_name_from_iter(oIter)[:iLenKey].lower()
        if self.to_ascii(sCardSetName).startswith(sKey) or sCardSetName.startswith(sKey):
            return False
        if oModel.iter_n_children(oIter) > 0:
            check_children(oModel, oIter, sKey, iLenKey)
        return True

    def set_select_none(self):
        """set selection to single mode"""
        self._oSelection.set_mode(gtk.SELECTION_NONE)

    def set_select_single(self):
        """set selection to single mode"""
        self._oSelection.set_mode(gtk.SELECTION_SINGLE)

    def set_select_multiple(self):
        """set selection to multiple mode"""
        self._oSelection.set_mode(gtk.SELECTION_MULTIPLE)

    def set_filter(self, oFilter, oMenu=None):
        """Set the current filter to oFilter & apply it."""
        if oFilter:
            self._oModel.selectfilter = oFilter
            if not self._oModel.applyfilter:
                if oMenu:
                    oMenu.set_apply_filter(True)
                else:
                    self._oModel.applyfilter = True
            else:
                self.reload_keep_expanded()
        elif self._oModel.applyfilter:
            if oMenu:
                oMenu.set_apply_filter(False)
            else:
                self._oModel.applyfilter = False
        else:
            self.reload_keep_expanded()

    def split_selection_data(self, sSelectionData):
        """Helper function to subdivide selection string into bits again"""
        if sSelectionData == '':
            return ('None', [''])
        aLines = sSelectionData.splitlines()
        sSource = aLines[0]
        return (sSource, aLines)