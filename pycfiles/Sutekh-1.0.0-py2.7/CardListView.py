# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/CardListView.py
# Compiled at: 2019-12-11 16:37:48
"""gtk.TreeView classes for displaying the card list."""
import gtk
from .FilteredView import FilteredView
from .FilterDialog import FilterDialog
from ..core.BaseTables import PhysicalCard, AbstractCard
from ..core.BaseAdapters import IPhysicalCard

class CardListView(FilteredView):
    """Base class for all the card list views in Sutekh."""

    def __init__(self, oController, oMainWindow, oModel, oConfig):
        super(CardListView, self).__init__(oController, oMainWindow, oModel, oConfig)
        self.set_select_multiple()
        self._oSelection.connect('changed', self.card_selected)
        if hasattr(oMainWindow, 'icon_manager') and hasattr(oModel, 'oIconManager'):
            oModel.oIconManager = oMainWindow.icon_manager
        self._oSelection.set_select_function(self.can_select)
        tGtkVersion = gtk.gtk_version
        if tGtkVersion[0] == 2 and (tGtkVersion[1] > 6 and tGtkVersion[1] < 12 or tGtkVersion[1] == 12 and tGtkVersion[2] == 0):
            self.connect('move-cursor', self.force_cursor_move)
        self.connect('row-activated', self.card_activated)
        self.connect('select-all', self.select_all)
        aTargets = [
         (
          'STRING', gtk.TARGET_SAME_APP, 0),
         (
          'text/plain', gtk.TARGET_SAME_APP, 0)]
        self.drag_source_set(gtk.gdk.BUTTON1_MASK | gtk.gdk.BUTTON3_MASK, aTargets, gtk.gdk.ACTION_COPY | gtk.gdk.ACTION_MOVE)
        self.drag_dest_set(gtk.DEST_DEFAULT_ALL, aTargets, gtk.gdk.ACTION_COPY | gtk.gdk.ACTION_MOVE)
        self.connect('drag_data_get', self.drag_card)
        self.connect('drag_data_delete', self.drag_delete)
        self.connect('drag_data_received', self.card_drop)
        self.bSelectTop = 0

    def can_select(self, oPath):
        """disable selecting top level rows"""
        if self.bSelectTop > 0:
            self.bSelectTop -= 1
            return True
        else:
            return self._oModel.iter_parent(self._oModel.get_iter(oPath)) is not None

    def card_selected(self, oSelection):
        """Change the selection behaviour.

           If we have multiple rows selected, and the user selects
           a single row that is in the selection, we DON'T change
           the selection, but we do update the card text and so on.
           """
        oPath = self.row_selected(oSelection)
        if not oPath:
            return
        oPhysCard = self._oModel.get_physical_card_from_path(oPath)
        if oPhysCard:
            self._oController.set_card_text(oPhysCard)

    def process_selection(self):
        """Create a dictionary from the selection.

           Entries are of the form oAbsId : {oPhysId: iCount1, ... }
           for use in drag-'n drop and elsewhere.

           We use ids to avoid various encoding issues
           """
        oModel, aPathList = self._oSelection.get_selected_rows()
        dSelectedData = {}
        for oPath in aPathList:
            oIter = oModel.get_iter(oPath)
            iDepth = oModel.iter_depth(oIter)
            if iDepth == 0:
                continue
            oAbsCard = oModel.get_abstract_card_from_iter(oIter)
            oPhysCard = oModel.get_physical_card_from_iter(oIter)
            iCount = oModel.get_card_count_from_iter(oIter)
            dSelectedData.setdefault(oAbsCard.id, {})
            if iDepth == 1:
                dSelectedData[oAbsCard.id].clear()
                aChildren = oModel.get_child_entries_from_iter(oIter)
                if len(aChildren) != 1:
                    dSelectedData[oAbsCard.id][-1] = iCount
                else:
                    oChildCard, iCount = aChildren[0]
                    dSelectedData[oAbsCard.id][oChildCard.id] = iCount
            else:
                if -1 in dSelectedData[oAbsCard.id]:
                    continue
                dSelectedData[oAbsCard.id][oPhysCard.id] = iCount

        return dSelectedData

    def get_selection_as_string(self):
        """Get a string representing the current selection.

           Because of how pygtk handles drag-n-drop data, we need to
           create a string representating the card data."""
        if self._oSelection.count_selected_rows() < 1:
            return ''
        dSelectedData = self.process_selection()
        sSelectData = self.sDragPrefix
        for oAbsCardID in dSelectedData:
            for oPhysCardId, iCount in dSelectedData[oAbsCardID].iteritems():
                sSelectData += '\n%(count)d x  %(abscard)d x %(physcard)d' % {'count': iCount, 
                   'abscard': oAbsCardID, 
                   'physcard': oPhysCardId}

        return sSelectData

    def split_selection_data(self, sSelectionData):
        """Helper function to subdivide selection string into bits again"""

        def true_card(iPhysCardID, oAbsCard):
            """Convert back from the 'None' placeholder in the string"""
            if iPhysCardID == -1:
                return IPhysicalCard((oAbsCard, None))
            else:
                return PhysicalCard.get(iPhysCardID)

        sSource, aLines = super(CardListView, self).split_selection_data(sSelectionData)
        if sSource in ('None', 'Basic Pane:', 'Card Set:'):
            return (
             sSource, aLines)
        aCardInfo = []
        for sLine in aLines[1:]:
            iCount, iAbsID, iPhysID = [ int(x) for x in sLine.split(' x ') ]
            oAbsCard = AbstractCard.get(iAbsID)
            oPhysCard = true_card(iPhysID, oAbsCard)
            aCardInfo.append((iCount, oPhysCard))

        return (
         sSource, aCardInfo)

    def drag_card(self, oBtn, oContext, oSelectionData, oInfo, oTime):
        """Create string representation of the selection for drag-n-drop"""
        sSelectData = self.get_selection_as_string()
        if sSelectData == '':
            self._oController.frame.create_drag_data(oBtn, oContext, oSelectionData, oInfo, oTime)
            return
        oSelectionData.set(oSelectionData.target, 8, sSelectData)

    def drag_delete(self, oBtn, oContext):
        """Default drag-delete handler"""
        pass

    def card_drop(self, oWdgt, oContext, iXPos, iYPos, oData, oInfo, oTime):
        """Default drag-n-drop handler."""
        self._oController.frame.drag_drop_handler(oWdgt, oContext, iXPos, iYPos, oData, oInfo, oTime)

    def copy_selection(self):
        """Copy the current selection to the application clipboard"""
        sSelection = self.get_selection_as_string()
        self._oMainWin.set_selection_text(sSelection)

    def compare(self, oModel, _iColumn, sKey, oIter, _oData):
        """Compare the entered text to the card names."""
        if oModel.iter_depth(oIter) == 2:
            return True
        oPath = oModel.get_path(oIter)
        sKey = sKey.lower()
        iLenKey = len(sKey)
        if oModel.iter_depth(oIter) == 0:
            if self.row_expanded(oPath):
                return True
            oChildIter = self._oModel.iter_children(oIter)
            while oChildIter:
                sChildName = self._oModel.get_name_from_iter(oChildIter)
                sChildName = sChildName[:iLenKey].lower()
                if self.to_ascii(sChildName).startswith(sKey) or sChildName.startswith(sKey):
                    self.expand_to_path(oPath)
                    return True
                oChildIter = self._oModel.iter_next(oChildIter)

            return True
        sCardName = self._oModel.get_name_from_iter(oIter)[:iLenKey].lower()
        if self.to_ascii(sCardName).startswith(sKey) or sCardName.startswith(sKey):
            return False
        return True

    def card_activated(self, _oTree, oPath, _oColumn):
        """Update card text and notify listeners when a card is selected."""
        oPhysCard = self._oModel.get_physical_card_from_path(oPath)
        if oPhysCard:
            self._oController.set_card_text(oPhysCard)

    def force_cursor_move(self, _oTreeView, _iStep, _iCount):
        """Special handling for move events for buggy gtk events.

           We need to allow the selection of top level items when
           moving the cursor over them
           """
        oCurPath, _oColumn = self.get_cursor()
        if self._oModel.iter_parent(self._oModel.get_iter(oCurPath)) is None:
            self.bSelectTop = 2
            self._oSelection.select_path(oCurPath)
        return False

    def _get_filter_dialog(self, sDefaultFilter):
        """Create the filter dialog for this view."""
        self._oFilterDialog = FilterDialog(self._oMainWin, self._oConfig, self._oController.filtertype, sDefaultFilter)
        return True

    def make_drag_icon(self, _oWidget, oDragContext):
        """Custom drag icon for dragging cards"""
        iNumSelected = self._oSelection.count_selected_rows()
        if iNumSelected > 1:
            self.drag_source_set_icon_stock(gtk.STOCK_DND_MULTIPLE)
        elif iNumSelected == 1:
            self.drag_source_set_icon_stock(gtk.STOCK_DND)
        else:
            self.frame.make_drag_icon(self, oDragContext)

    def select_all(self, _oWidget):
        """Expand the tree and select all the nodes"""
        self.expand_all()
        self._oSelection.select_all()