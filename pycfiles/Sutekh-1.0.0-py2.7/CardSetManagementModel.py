# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/CardSetManagementModel.py
# Compiled at: 2019-12-11 16:37:48
"""gtk.TreeModel class the card set list."""
import gtk, gobject
from ..core.BaseTables import PhysicalCardSet
from ..core.BaseAdapters import IPhysicalCardSet
from ..core.BaseFilters import NullFilter
from .BaseConfigFile import CARDSET_LIST

class CardSetManagementModel(gtk.TreeStore):
    """TreeModel for the card set list"""

    def __init__(self, oMainWindow):
        super(CardSetManagementModel, self).__init__(str, str)
        self._dName2Iter = {}
        self._oMainWin = oMainWindow
        self._bApplyFilter = False
        self._oSelectFilter = None
        self.oEmptyIter = None
        self._aExcludedSet = set()
        return

    applyfilter = property(fget=lambda self: self._bApplyFilter, fset=lambda self, x: setattr(self, '_bApplyFilter', x))
    selectfilter = property(fget=lambda self: self._oSelectFilter, fset=lambda self, x: setattr(self, '_oSelectFilter', x))
    frame_id = property(fget=lambda self: CARDSET_LIST, doc='Frame ID of the card set list (for selecting profiles)')
    cardset_id = property(fget=lambda self: CARDSET_LIST, doc='Cardset ID of card set list (for selecting profiles)')

    def get_card_set_iterator(self, oFilter):
        """Return an interator over the card set model.

           None may be used to retrieve the entire card set list
           """
        if not oFilter:
            oFilter = NullFilter()
        return oFilter.select(PhysicalCardSet).distinct()

    def _format_set(self, oSet):
        """Format the card set name for display"""
        sMarkup = gobject.markup_escape_text(oSet.name)
        if oSet.name in self._aExcludedSet:
            sMarkup = '<span foreground="grey">%s</span>' % sMarkup
        elif hasattr(self._oMainWin, 'find_cs_pane_by_set_name') and self._oMainWin.find_cs_pane_by_set_name(oSet.name):
            sMarkup = '<span foreground="blue">%s</span>' % sMarkup
        if oSet.inuse:
            sMarkup = '<b>%s</b>' % sMarkup
        return sMarkup

    def exclude_set(self, sSetName):
        """Mark the given set as excluded"""
        self._aExcludedSet.add(sSetName)
        oPath = self.get_path_from_name(sSetName)
        if oPath:
            oIter = self.get_iter(oPath)
            sMarkup = self._format_set(IPhysicalCardSet(sSetName))
            self.set(oIter, 0, sMarkup)

    def unexclude_set(self, sSetName):
        """Unmark the given set as excluded"""
        self._aExcludedSet.discard(sSetName)

    def is_excluded(self, sSetName):
        """Check if this set is excluded"""
        return sSetName in self._aExcludedSet

    def enable_sorting(self):
        """Enable the default sorting behaviour"""
        self.set_sort_func(0, self.sort_column)
        self.set_sort_column_id(0, gtk.SORT_ASCENDING)

    def sort_equal_iters(self, oIter1, oIter2):
        """Default sort on names (card names, expansion names, etc.)"""
        oVal1 = self.get_value(oIter1, 0)
        oVal2 = self.get_value(oIter2, 0)
        return cmp(oVal1, oVal2)

    def load(self):
        """Load the card sets into the card view"""
        self.clear()
        oCardSetIter = self.get_card_set_iterator(self.get_current_filter())
        self._dName2Iter = {}
        iSortColumn, iSortOrder = self.get_sort_column_id()
        if iSortColumn is not None:
            self.set_sort_column_id(-2, 0)
        for oCardSet in oCardSetIter:
            if oCardSet.name in self._dName2Iter:
                continue
            if oCardSet.parent:
                oParent = oCardSet
                aToAdd = []
                oIter = None
                while oParent and oParent.name not in self._dName2Iter:
                    aToAdd.insert(0, oParent)
                    oParent = oParent.parent

                if oParent and oParent.name in self._dName2Iter:
                    oIter = self._dName2Iter[oParent.name]
            else:
                oIter = None
                aToAdd = [oCardSet]
            for oSet in aToAdd:
                oIter = self.append(oIter)
                sMarkup = self._format_set(oSet)
                self.set(oIter, 0, sMarkup, 1, oSet.name)
                self._dName2Iter[oSet.name] = oIter

        if not self._dName2Iter:
            self.oEmptyIter = self.append(None)
            sText = self._get_empty_text()
            self.set(self.oEmptyIter, 0, sText)
        if iSortColumn is not None:
            self.set_sort_column_id(iSortColumn, iSortOrder)
        return

    def get_current_filter(self):
        """Get the current applied filter."""
        if self.applyfilter:
            return self.selectfilter
        else:
            return

    def get_name_from_iter(self, oIter):
        """Extract the value at oIter from the model, correcting for encoding
           issues."""
        sCardSetName = self.get_value(oIter, 1)
        if sCardSetName:
            sCardSetName = sCardSetName.decode('utf-8')
        return sCardSetName

    def get_path_from_name(self, sName):
        """Get the tree path corresponding to the name"""

        def check_iter(oIter, sName):
            """Recursively descend the children of the given gtk.TreeIter,
               looking for a path matching sName."""
            oPath = None
            if sName == self.get_name_from_iter(oIter):
                return self.get_path(oIter)
            else:
                oChildIter = self.iter_children(oIter)
                while oChildIter:
                    oPath = check_iter(oChildIter, sName)
                    if oPath:
                        return oPath
                    oChildIter = self.iter_next(oChildIter)

                return oPath

        oIter = self.get_iter_root()
        while oIter:
            oPath = check_iter(oIter, sName)
            if oPath:
                return oPath
            oIter = self.iter_next(oIter)

        return

    def get_name_from_path(self, oPath):
        """Get the card set name at oPath."""
        oIter = self.get_iter(oPath)
        return self.get_name_from_iter(oIter)

    def sort_column(self, _oModel, oIter1, oIter2):
        """Custom sort function - ensure that markup doesn't affect sort
           order"""
        oCardSet1 = self.get_name_from_iter(oIter1)
        oCardSet2 = self.get_name_from_iter(oIter2)
        return cmp(oCardSet1, oCardSet2)

    def _get_empty_text(self):
        """Get the correct text for an empty model."""
        if self.get_card_set_iterator(None).count() == 0:
            sText = 'Empty'
        else:
            sText = 'No Card Sets found'
        return sText