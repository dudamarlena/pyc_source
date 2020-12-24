# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/CustomDragIconView.py
# Compiled at: 2019-12-11 16:37:48
"""gtk.TreeView class implementing a custom drag icon."""
import gtk

class CustomDragIconView(gtk.TreeView):
    """Base class for tree views that fiddle with the drag icon"""

    def __init__(self, oModel):
        self._oModel = oModel
        super(CustomDragIconView, self).__init__(self._oModel)
        self._oSelection = self.get_selection()
        self._aOldSelection = []
        self.bReentrant = False
        self.connect_after('drag_begin', self.make_drag_icon)
        self.connect_after('drag_motion', self.drag_motion)

    def make_drag_icon(self, _oWidget, _oDragContext):
        """Drag begin signal handler to set custom icon"""
        iNumSelected = self._oSelection.count_selected_rows()
        if iNumSelected > 1:
            self.drag_source_set_icon_stock(gtk.STOCK_DND_MULTIPLE)
        elif iNumSelected == 1:
            _oModel, aSelectedRows = self._oSelection.get_selected_rows()
            oDrawable = self.create_row_drag_icon(aSelectedRows[0])
            self.drag_source_set_icon(oDrawable.get_colormap(), oDrawable)

    def drag_motion(self, _oWidget, oDrag_context, _iXPos, _iYPos, _oTimestamp):
        """Set appropriate context during drag + drop."""
        if 'STRING' in oDrag_context.targets:
            oDrag_context.drag_status(gtk.gdk.ACTION_COPY)
            return True
        return False

    def row_selected(self, oSelection):
        """Change the selection behaviour.

           If we have multiple rows selected, and the user selects
           a single row that is in the selection, we DON'T change
           the selection, but we do update the card text and so on.
           """
        if self.bReentrant:
            return
        else:
            if oSelection.count_selected_rows() <= 0:
                self._aOldSelection = []
                return
            _oModel, aList = oSelection.get_selected_rows()
            tCursorPos = self.get_cursor()
            if len(aList) == 1 and len(self._aOldSelection) > 1 and tCursorPos[0] == aList[0] and aList[0] in self._aOldSelection:
                try:
                    self.bReentrant = True
                    for oPath in self._aOldSelection:
                        oSelection.select_path(oPath)

                finally:
                    self.bReentrant = False

                oPath = aList[0]
            else:
                _oModel, aList = oSelection.get_selected_rows()
                if not aList:
                    self._aOldSelection = []
                    return
                if len(aList) <= len(self._aOldSelection):
                    oPath = aList[(-1)]
                else:
                    oPath = [ x for x in aList if x not in self._aOldSelection ][(-1)]
                self._aOldSelection = aList
            return oPath