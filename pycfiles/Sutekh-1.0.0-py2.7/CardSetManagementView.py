# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/CardSetManagementView.py
# Compiled at: 2019-12-11 16:37:48
"""gtk.TreeView class for the card set list."""
import gtk
from sqlobject import SQLObjectNotFound
from ..core.BaseAdapters import IPhysicalCardSet
from .GuiCardSetFunctions import reparent_card_set
from .CardSetsListView import CardSetsListView
from .FilterDialog import FilterDialog

class CardSetManagementView(CardSetsListView):
    """Tree View for the management of card set list."""

    def __init__(self, oController, oMainWindow):
        super(CardSetManagementView, self).__init__(oController, oMainWindow)
        self.set_select_single()
        aTargets = [
         ('STRING', 0, 0),
         ('text/plain', 0, 0)]
        self.drag_source_set(gtk.gdk.BUTTON1_MASK | gtk.gdk.BUTTON3_MASK, aTargets, gtk.gdk.ACTION_COPY | gtk.gdk.ACTION_MOVE)
        self.enable_model_drag_dest(aTargets, gtk.gdk.ACTION_COPY | gtk.gdk.ACTION_MOVE)
        self.connect('drag_data_get', self.drag_card_set)
        self.connect('row_activated', self.row_clicked)
        self.connect('drag_data_received', self.card_set_drop)
        self.set_name('card set management view')

    def make_drag_icon(self, oWidget, oDragContext):
        """Drag begin signal handler to set custom icon"""
        sSetName = self.get_selected_card_set()
        if sSetName:
            super(CardSetManagementView, self).make_drag_icon(oWidget, oDragContext)
        else:
            self.frame.make_drag_icon(self, oDragContext)

    def drag_card_set(self, oBtn, oDragContext, oSelectionData, oInfo, oTime):
        """Allow card sets to be dragged to a frame."""
        sSetName = self.get_selected_card_set()
        if not sSetName:
            self._oController.frame.create_drag_data(oBtn, oDragContext, oSelectionData, oInfo, oTime)
            return
        sData = ('\n').join(['Card Set:', sSetName])
        oSelectionData.set(oSelectionData.target, 8, sData)

    def card_set_drop(self, oWidget, oContext, iXPos, iYPos, oData, oInfo, oTime):
        """Default drag-n-drop handler."""
        sSource, aData = self.split_selection_data(oData.data)
        bDragRes = False
        if sSource == 'Basic Pane:':
            self._oController.frame.drag_drop_handler(oWidget, oContext, iXPos, iYPos, oData, oInfo, oTime)
            return
        if sSource == 'Card Set:':
            oPath = self.get_path_at_pointer()
            if oPath:
                sThisName = aData[1]
                try:
                    oDraggedCS = IPhysicalCardSet(sThisName)
                    oParentCS = IPhysicalCardSet(self._oModel.get_name_from_path(oPath))
                    if reparent_card_set(oDraggedCS, oParentCS):
                        self.frame.reload()
                        oPath = self._oModel.get_path_from_name(sThisName)
                        if oPath:
                            self.expand_to_path(oPath)
                        bDragRes = True
                except SQLObjectNotFound:
                    pass

        oContext.finish(bDragRes, False, oTime)

    def row_clicked(self, _oTreeView, oPath, _oColumn):
        """Handle row clicked events.

           allow double clicks to open a card set.
           """
        sName = self._oModel.get_name_from_path(oPath)
        self._oMainWin.add_new_physical_card_set(sName)

    def get_path_at_pointer(self):
        """Get the path at the current pointer position"""
        iXPos, iYPos, _oIgnore = self.get_bin_window().get_pointer()
        tRes = self.get_path_at_pos(iXPos, iYPos)
        if tRes:
            return tRes[0]
        else:
            return

    def _get_filter_dialog(self, sDefaultFilter):
        """Create the filter dialog for this view."""
        self._oFilterDialog = FilterDialog(self._oMainWin, self._oConfig, self._oController.filtertype, sDefaultFilter)
        return True