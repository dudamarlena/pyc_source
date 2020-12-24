# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/CardSetView.py
# Compiled at: 2019-12-11 16:37:48
"""View object for card sets."""
import gtk
from .CellRendererSutekhButton import CellRendererSutekhButton
from .CellRendererIcons import CellRendererIcons
from .CardListView import CardListView
from .CardSetListModel import CardSetCardListModel
from ..core.BaseTables import PhysicalCardSet
NUM_KEYS = {gtk.gdk.keyval_from_name('1'): 1, 
   gtk.gdk.keyval_from_name('KP_1'): 1, 
   gtk.gdk.keyval_from_name('2'): 2, 
   gtk.gdk.keyval_from_name('KP_2'): 2, 
   gtk.gdk.keyval_from_name('3'): 3, 
   gtk.gdk.keyval_from_name('KP_3'): 3, 
   gtk.gdk.keyval_from_name('4'): 4, 
   gtk.gdk.keyval_from_name('KP_4'): 4, 
   gtk.gdk.keyval_from_name('5'): 5, 
   gtk.gdk.keyval_from_name('KP_5'): 5, 
   gtk.gdk.keyval_from_name('6'): 6, 
   gtk.gdk.keyval_from_name('KP_6'): 6, 
   gtk.gdk.keyval_from_name('7'): 7, 
   gtk.gdk.keyval_from_name('KP_7'): 7, 
   gtk.gdk.keyval_from_name('8'): 8, 
   gtk.gdk.keyval_from_name('KP_8'): 8, 
   gtk.gdk.keyval_from_name('9'): 9, 
   gtk.gdk.keyval_from_name('KP_9'): 9}
PLUS_KEYS = set([
 gtk.gdk.keyval_from_name('plus'),
 gtk.gdk.keyval_from_name('KP_Add')])
MINUS_KEYS = set([
 gtk.gdk.keyval_from_name('minus'),
 gtk.gdk.keyval_from_name('KP_Subtract')])

class CardSetView(CardListView):
    """Subclass of CardListView specific to the Card Sets

       Adds editing support, and other specific to the card sets.
       The database interactions are handled by the controller,
       this just manages the GUI side of things, passing info to
       the controller when needed.
       """

    def __init__(self, oMainWindow, oController, sName, bStartEditable):
        oModel = CardSetCardListModel(sName, oMainWindow.config_file)
        oModel.enable_sorting()
        if bStartEditable:
            oModel.bEditable = True
        super(CardSetView, self).__init__(oController, oMainWindow, oModel, oMainWindow.config_file)
        self.sSetName = sName
        self.sDragPrefix = PhysicalCardSet.sqlmeta.table + ':' + self.sSetName
        self.oNumCell = gtk.CellRendererText()
        self.oNameCell = CellRendererIcons(5)
        oColumn1 = gtk.TreeViewColumn('#', self.oNumCell, text=1)
        oColumn1.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        oColumn1.set_fixed_width(60)
        oColumn1.set_sort_column_id(1)
        oColumn1.set_resizable(True)
        self.append_column(oColumn1)
        oParentCell = gtk.CellRendererText()
        self.oParentCol = gtk.TreeViewColumn('Par #', oParentCell, text=2, foreground_gdk=7)
        self.oParentCol.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.oParentCol.set_fixed_width(60)
        self.oParentCol.set_sort_column_id(2)
        self.append_column(self.oParentCol)
        self.oParentCol.set_visible(False)
        self.oParentCol.set_resizable(True)
        oColumn2 = gtk.TreeViewColumn('Cards', self.oNameCell, text=0, textlist=5, icons=6)
        oColumn2.set_min_width(100)
        oColumn2.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        oColumn2.set_sort_column_id(0)
        oColumn2.set_expand(True)
        oColumn2.set_resizable(True)
        self.append_column(oColumn2)
        self.set_expander_column(oColumn2)
        oIncCell = CellRendererSutekhButton()
        oIncCell.load_icon(gtk.STOCK_ADD, self)
        oDecCell = CellRendererSutekhButton()
        oDecCell.load_icon(gtk.STOCK_REMOVE, self)
        self.oIncCol = gtk.TreeViewColumn('', oIncCell, showicon=3)
        self.oIncCol.set_fixed_width(19)
        self.oIncCol.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.oIncCol.set_resizable(False)
        self.oIncCol.set_visible(False)
        self.append_column(self.oIncCol)
        self.oDecCol = gtk.TreeViewColumn('', oDecCell, showicon=4)
        self.oDecCol.set_fixed_width(19)
        self.oDecCol.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.oDecCol.set_resizable(False)
        self.oDecCol.set_visible(False)
        self.append_column(self.oDecCol)
        oIncCell.connect('clicked', self.inc_card)
        oDecCell.connect('clicked', self.dec_card)
        self.__iMapID = self.connect('map', self.mapped)
        self.connect('key-press-event', self.key_press)
        self._oMenu = None
        self.oCellColor = None
        self.set_fixed_height_mode(True)
        return

    def process_selection(self):
        """Create a dictionary from the selection.

           Entries are of the form sCardName : {sExpansion1 : iCount1, ... }
           for use in drag-'n drop and elsewhere.
           """
        oModel, oPathList = self._oSelection.get_selected_rows()
        dSelectedData = {}
        for oPath in oPathList:
            iAbsID, iPhysID, iCount, iDepth = oModel.get_drag_info_from_path(oPath)
            if not iAbsID:
                continue
            dSelectedData.setdefault(iAbsID, {})
            if iDepth == 1:
                dSelectedData[iAbsID].clear()
                for iPhysID, iCnt in oModel.get_drag_child_info(oPath).iteritems():
                    dSelectedData[iAbsID][iPhysID] = iCnt

            elif not iPhysID:
                dChildInfo = oModel.get_drag_child_info(oPath)
                if dChildInfo:
                    for iPhysID, iCnt in dChildInfo.iteritems():
                        dSelectedData[iAbsID][iPhysID] = iCnt

                else:
                    if -1 in dSelectedData[iAbsID]:
                        continue
                    dSelectedData[iAbsID][-1] = iCount
            else:
                if iPhysID in dSelectedData[iAbsID]:
                    continue
                dSelectedData[iAbsID][iPhysID] = iCount

        return dSelectedData

    def _process_edit_selection(self, iSetNewCount=None, iChg=None):
        """Create a dictionary from the selection, suitable for the quick
           key based edits.

           Entries are of the form
               oPhysCard : { sCardSetName : [iCount1, iNewCnt1] ... }
           In addition to adding information about card sets, this
           differs from process_selection in the way card level items
           are handled. Here, these are treated as selecting the expansion
           None, and ignoring other expansions.

           Since this isn't going through the drag-n-drop code, we don't
           need to create a string representation, so we can work with the
           card objects directly.

           """
        oModel, oPathList = self._oSelection.get_selected_rows()
        dSelectedData = {}
        aSkip = set()
        iNewCount = 0
        for oPath in oPathList:
            sCardSet = None
            oIter = oModel.get_iter(oPath)
            oPhysCard = oModel.get_physical_card_from_iter(oIter)
            oAbsCard = oModel.get_abstract_card_from_iter(oIter)
            iCount = oModel.get_card_count_from_iter(oIter)
            if iChg:
                iNewCount = max(0, iCount + iChg)
            elif iSetNewCount:
                iNewCount = iSetNewCount
            _sCardName, _sExpansion, sCardSet = oModel.get_all_names_from_iter(oIter)
            dSelectedData.setdefault(oPhysCard, {})
            iDepth = oModel.iter_depth(oIter)
            if iDepth == 1:
                dSelectedData[oPhysCard].clear()
                dSelectedData[oPhysCard][None] = [iCount, iNewCount]
                aSkip.add(oAbsCard)
            else:
                if oAbsCard in aSkip:
                    continue
                if sCardSet in dSelectedData[oPhysCard]:
                    continue
                dSelectedData[oPhysCard][sCardSet] = [iCount, iNewCount]

        return dSelectedData

    def card_drop(self, oWidget, oContext, iXPos, iYPos, oData, oInfo, oTime):
        """Handle drag-n-drop events."""
        bDragRes = True
        if not oData or oData.format != 8:
            bDragRes = False
        else:
            sSource, aCardInfo = self.split_selection_data(oData.data)
            bSkip = False
            if sSource == 'Basic Pane:' or sSource == 'Card Set:':
                self._oController.frame.drag_drop_handler(oWidget, oContext, iXPos, iYPos, oData, oInfo, oTime)
                return
        if not self._oModel.bEditable:
            bSkip = True
        elif sSource == self.sDragPrefix:
            bSkip = True
        if bSkip or not self._oController.add_paste_data(sSource, aCardInfo):
            bDragRes = False
        oContext.finish(bDragRes, False, oTime)

    def inc_card(self, _oCell, oPath):
        """Called to increment the count for a card."""
        if self._oModel.bEditable:
            bInc, _bDec = self._oModel.get_inc_dec_flags_from_path(oPath)
            if bInc:
                oPhysCard = self._oModel.get_physical_card_from_path(oPath)
                _sCardName, _sExpansion, sCardSetName = self._oModel.get_all_names_from_path(oPath)
                self._oController.inc_card(oPhysCard, sCardSetName)

    def dec_card(self, _oCell, oPath):
        """Called to decrement the count for a card"""
        if self._oModel.bEditable:
            _bInc, bDec = self._oModel.get_inc_dec_flags_from_path(oPath)
            if bDec:
                oPhysCard = self._oModel.get_physical_card_from_path(oPath)
                _sCardName, _sExpansion, sCardSetName = self._oModel.get_all_names_from_path(oPath)
                self._oController.dec_card(oPhysCard, sCardSetName)

    def key_press(self, _oWidget, oEvent):
        """Change the number if 1-9 is pressed and we're editable or if + or
           - is pressed. We use the lists defined above to handle the keypad
           as well."""
        if oEvent.keyval in NUM_KEYS:
            if self._oModel.bEditable:
                iCnt = NUM_KEYS[oEvent.keyval]
                dSelectedData = self._process_edit_selection(iSetNewCount=iCnt)
                self._oController.change_selected_card_count(dSelectedData)
            return True
        if oEvent.keyval in PLUS_KEYS and self._oModel.bEditable:
            dSelectedData = self._process_edit_selection(iChg=+1)
            self._oController.change_selected_card_count(dSelectedData)
            return True
        if oEvent.keyval in MINUS_KEYS and self._oModel.bEditable:
            dSelectedData = self._process_edit_selection(iChg=-1)
            self._oController.change_selected_card_count(dSelectedData)
            return True
        return False

    def mapped(self, _oWidget):
        """Called when the view has been mapped, so we can twiddle the
           display

           In the case when a card set is opened editable, we need to
           load after the pane is mapped, so that the colours are setup
           correctly. We also use the opportunity to ensure the menu
           is in sync."""
        if self._oModel.bEditable:
            self._set_editable(True)
        self.disconnect(self.__iMapID)
        self.__iMapID = None
        self.reload_keep_expanded()
        return True

    def del_selection(self):
        """try to delete all the cards in the current selection"""
        if self._oModel.bEditable:
            dSelectedData = self._process_edit_selection(iSetNewCount=0)
            self._oController.change_selected_card_count(dSelectedData)

    def do_paste(self):
        """Try and paste the current selection from the application
           clipboard"""
        if self._oModel.bEditable:
            sSelection = self._oMainWin.get_selection_text()
            sSource, aCards = self.split_selection_data(sSelection)
            if sSource != self.sDragPrefix:
                self._oController.add_paste_data(sSource, aCards)

    def load(self):
        """Called when the model needs to be reloaded."""
        if self.__iMapID is not None:
            return
        else:
            if hasattr(self._oMainWin, 'set_busy_cursor'):
                self._oMainWin.set_busy_cursor()
            self.freeze_child_notify()
            self.set_model(None)
            self._oModel.load()
            self.set_model(self._oModel)
            self.oNumCell.set_property('foreground-gdk', self._oModel.get_count_colour())
            self.thaw_child_notify()
            if hasattr(self._oMainWin, 'restore_cursor'):
                self._oMainWin.restore_cursor()
            return

    def set_color_edit_cue(self):
        """Set a visual cue that the card set is editable."""
        if not self._oModel.oEditColour:
            self._determine_edit_colour()
        self.set_name('editable_view')

    def _determine_edit_colour(self):
        """Determine which colour to use for the editable hint"""

        def _compare_colors(oColor1, oColor2):
            """Compare the RGB values for 2 gtk.gdk.Colors. Return True if
               they're the same, false otherwise."""
            return oColor1.to_string() == oColor2.to_string()

        oCurStyle = self.rc_get_style()
        self.oCellColor = gtk.gdk.color_parse('black')
        oCurBackColor = oCurStyle.base[gtk.STATE_NORMAL]
        self.set_name('editable_view')
        oDefaultSutekhStyle = gtk.rc_get_style_by_paths(self.get_settings(), '', self.class_path(), self)
        oSpecificStyle = self.rc_get_style()
        if oSpecificStyle == oDefaultSutekhStyle or oDefaultSutekhStyle is None:
            sColour = 'red'
            if _compare_colors(gtk.gdk.color_parse(sColour), oCurStyle.fg[gtk.STATE_NORMAL]):
                sColour = 'green'
            sStyleInfo = '\n            style "internal_sutekh_editstyle" {\n                fg[NORMAL] = "%(colour)s"\n                }\n            widget "%(path)s" style "internal_sutekh_editstyle"\n            ' % {'colour': sColour, 'path': self.path()}
            gtk.rc_parse_string(sStyleInfo)
            self.set_name('editable_view')
        oCurStyle = self.rc_get_style()
        oEditColor = oCurStyle.fg[gtk.STATE_NORMAL]
        oEditBackColor = oCurStyle.base[gtk.STATE_NORMAL]
        if not _compare_colors(oEditColor, self.oCellColor) or not _compare_colors(oEditBackColor, oCurBackColor):
            self._oModel.oEditColour = oEditColor
        else:
            self._oModel.oEditColour = gtk.gdk.color_parse('red')
        return

    def set_color_normal(self):
        """Unset the editable visual cue"""
        self.set_name('normal_view')

    def _set_editable(self, bValue):
        """Update the view and menu when the editable status changes"""
        self._oModel.bEditable = bValue
        if self._oMenu is not None:
            self._oMenu.force_editable_mode(bValue)
        if bValue:
            self.set_color_edit_cue()
            self.oIncCol.set_visible(True)
            self.oDecCol.set_visible(True)
        else:
            self.set_color_normal()
            self.oIncCol.set_visible(False)
            self.oDecCol.set_visible(False)
        return

    def toggle_editable(self, bValue):
        """Reload the view and update status when editable status changes"""
        self._set_editable(bValue)
        self.reload_keep_expanded()

    def set_menu(self, oMenu):
        """Keep track of the menu item, so we can update it's toggled
           status."""
        self._oMenu = oMenu

    def set_parent_count_col_vis(self, bVisible):
        """Make the parent count column visible or invisible"""
        self.oParentCol.set_visible(bVisible)

    def update_name(self, sNewName):
        """Handle the renaming of a card set - set the correct new drag prefix,
           etc."""
        self.sSetName = sNewName
        self.sDragPrefix = PhysicalCardSet.sqlmeta.table + ':' + self.sSetName

    def save_iter_state(self, aIters, dStates):
        """Save the expanded state of the list of iters in aIters and their
           children."""
        dStates.setdefault('expanded', set())
        dStates.setdefault('selected', set())
        for oIter in aIters:
            oParIter = self._oModel.iter_parent(oIter)
            sParKey = self.get_iter_identifier(oParIter)
            sKey = self.get_iter_identifier(oIter)
            if self._oSelection.iter_is_selected(oIter):
                dStates['selected'].add(sKey)
            oPath = self._oModel.get_path(oParIter)
            if self.row_expanded(oPath):
                dStates['expanded'].add(sParKey)
            aChildIters = self._oModel.get_all_iter_children(oIter)
            self.save_iter_state(aChildIters, dStates)

    def restore_iter_state(self, aIters, dStates):
        """Restore expanded state of the iters."""
        if not dStates or 'selected' not in dStates:
            return
        for oIter in aIters:
            oParIter = self._oModel.iter_parent(oIter)
            sParKey = self.get_iter_identifier(oParIter)
            sKey = self.get_iter_identifier(oIter)
            if sParKey in dStates['expanded']:
                self.expand_to_path(self._oModel.get_path(oParIter))
            aChildIters = self._oModel.get_all_iter_children(oIter)
            self.restore_iter_state(aChildIters, dStates)
            if sKey in dStates['selected']:
                self._oSelection.select_iter(oIter)