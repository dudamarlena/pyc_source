# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/CardListModel.py
# Compiled at: 2019-12-11 16:37:48
"""The gtk.TreeModel for the card lists."""
import logging, gtk, gobject
from ..core.BaseFilters import FilterAndBox, NullFilter, PhysicalCardFilter, CachedFilter, make_illegal_filter
from ..core.BaseGroupings import CardTypeGrouping
from ..core.BaseTables import PhysicalCard
from ..core.BaseAdapters import IAbstractCard, IPhysicalCard, IPrintingName, PrintingNameAdapter
from ..core.FilterParser import FilterParser
from ..Utility import move_articles_to_back
from .BaseConfigFile import FULL_CARDLIST
from .SutekhDialog import do_exception_complaint
from .MessageBus import MessageBus, CONFIG_MSG
EXTRA_LEVEL_OPTION = 'extra levels'
EXTRA_LEVEL_LOOKUP = {'none': False, 
   'expansions': True}
USE_ICONS = 'show icons for grouping'
HIDE_ILLEGAL = 'hide cards not legal for tournament play'

class CardListModel(gtk.TreeStore):
    """Provides a card list specific API for accessing a gtk.TreeStore."""
    sUnknownExpansion = PrintingNameAdapter.sUnknownExpansion

    def __init__(self, oConfig):
        super(CardListModel, self).__init__(str, int, int, bool, bool, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT, gtk.gdk.Color, gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT)
        self._cGroupBy = CardTypeGrouping
        self._oBaseFilter = PhysicalCardFilter()
        self._cCardClass = PhysicalCard
        self.oLegalFilter = CachedFilter(make_illegal_filter())
        self._bApplyFilter = False
        self._oSelectFilter = None
        self._oConfigFilter = None
        self._sCurConfigFilter = None
        self._oConfig = oConfig
        self.bExpansions = True
        self.oEmptyIter = None
        self.oIconManager = None
        self.bUseIcons = True
        self._bHideIllegal = True
        self._oController = None
        self._oFilterParser = FilterParser()
        MessageBus.subscribe(CONFIG_MSG, 'replace_filter', self.replace_filter)
        MessageBus.subscribe(CONFIG_MSG, 'profile_option_changed', self.profile_option_changed)
        MessageBus.subscribe(CONFIG_MSG, 'profile_changed', self.profile_changed)
        MessageBus.subscribe(CONFIG_MSG, 'set_postfix_the_display', self.set_postfix_the_display)
        return

    cardclass = property(fget=lambda self: self._cCardClass, fset=lambda self, x: setattr(self, '_cCardClass', x))
    groupby = property(fget=lambda self: self._cGroupBy, fset=lambda self, x: setattr(self, '_cGroupBy', x))
    basefilter = property(fget=lambda self: self._oBaseFilter, fset=lambda self, x: setattr(self, '_oBaseFilter', x))
    hideillegal = property(fget=lambda self: self._bHideIllegal, fset=lambda self, x: setattr(self, '_bHideIllegal', x))
    applyfilter = property(fget=lambda self: self._bApplyFilter, fset=lambda self, x: setattr(self, '_bApplyFilter', x))
    selectfilter = property(fget=lambda self: self._oSelectFilter, fset=lambda self, x: setattr(self, '_oSelectFilter', x))
    configfilter = property(fget=lambda self: self._oConfigFilter, doc='Filter from the current profile.')
    frame_id = property(fget=lambda self: FULL_CARDLIST, doc='Frame ID of the card list (for selecting profiles)')
    cardset_id = property(fget=lambda self: FULL_CARDLIST, doc='Cardset ID of card list (for selecting profiles)')

    def cleanup(self):
        """Remove the config file listener if needed"""
        self._oController = None
        MessageBus.unsubscribe(CONFIG_MSG, 'replace_filter', self.replace_filter)
        MessageBus.unsubscribe(CONFIG_MSG, 'profile_option_changed', self.profile_option_changed)
        MessageBus.unsubscribe(CONFIG_MSG, 'profile_changed', self.profile_changed)
        MessageBus.clear(self)
        return

    def _sort_col(self, _oModel, oIter1, oIter2, iCol):
        """Default sort function for model"""
        oVal1 = self.get_value(oIter1, iCol)
        oVal2 = self.get_value(oIter2, iCol)
        iRes = cmp(oVal1, oVal2)
        if iRes == 0:
            iRes = self.sort_equal_iters(oIter1, oIter2)
        return iRes

    def sort_equal_iters(self, oIter1, oIter2):
        """Default sort on names (card names, expansion names, etc.)"""
        oVal1 = self.get_value(oIter1, 0)
        oVal2 = self.get_value(oIter2, 0)
        return cmp(oVal1, oVal2)

    def enable_sorting(self):
        """Enable default sorting setup"""
        self.set_sort_func(0, self._sort_col, 0)
        self.set_sort_func(1, self._sort_col, 1)
        self.set_sort_func(2, self._sort_col, 2)
        self.set_sort_column_id(0, gtk.SORT_ASCENDING)

    def set_controller(self, oController):
        """Set the controller"""
        self._oController = oController
        self.update_options(True)

    def get_expansion_info(self, _oCard, dExpanInfo):
        """Get information about expansions"""
        aExpansions = []
        if not self.bExpansions:
            return aExpansions
        for oPhysCard in dExpanInfo:
            aExpansions.append((oPhysCard, IPrintingName(oPhysCard)))

        return aExpansions

    def lookup_icons(self, sGroup):
        """Lookup the icons for the group. Method since it's repeated in
           several places in CardSetListModel"""
        if self.oIconManager and self.bUseIcons:
            aTexts, aIcons = self.oIconManager.get_info(sGroup, self.groupby)
        else:
            aTexts = aIcons = []
        return (
         aTexts, aIcons)

    def _fix_group_name(self, sGroup):
        """Fix the None group name"""
        if sGroup is None:
            return '<< None >>'
        else:
            return sGroup

    def _set_display_name(self, bPostfix):
        """Set the correct display name for the cards.

           We walk all the 1st level entries, and set the name from the
           card, based on bPostfix."""
        oIter = self.get_iter_first()
        while oIter:
            oChildIter = self.iter_children(oIter)
            while oChildIter:
                sName = self.get_card_name_from_iter(oChildIter)
                if bPostfix:
                    sName = move_articles_to_back(sName)
                self.set(oChildIter, 0, sName)
                self.row_changed(self.get_path(oChildIter), oChildIter)
                oChildIter = self.iter_next(oChildIter)

            oIter = self.iter_next(oIter)

    def set_postfix_the_display(self, bPostfix):
        """Respond to config file changes. Passes straight through to
           _set_display_name so we don't need another load."""
        iSortColumn, iSortOrder = self.get_sort_column_id()
        if iSortColumn is not None:
            self.set_sort_column_id(-2, 0)
        self._set_display_name(bPostfix)
        if iSortColumn is not None:
            self.set_sort_column_id(iSortColumn, iSortOrder)
        return

    def load(self):
        """Clear and reload the underlying store. For use after initialisation
           or when the filter or grouping changes."""
        self.clear()
        oCardIter = self.get_card_iterator(self.get_current_filter())
        fGetCard, _fGetCount, fGetExpanInfo, oGroupedIter, aCards = self.grouped_card_iter(oCardIter)
        self.oEmptyIter = None
        iSortColumn, iSortOrder = self.get_sort_column_id()
        if iSortColumn is not None:
            self.set_sort_column_id(-2, 0)
        bEmpty = True
        bPostfix = self._oConfig.get_postfix_the_display()
        for sGroup, oGroupIter in oGroupedIter:
            sGroup = self._fix_group_name(sGroup)
            oSectionIter = self.append(None)
            for oItem in oGroupIter:
                oCard = fGetCard(oItem)
                oChildIter = self.prepend(oSectionIter)
                sName = oCard.name
                if bPostfix:
                    sName = move_articles_to_back(sName)
                self.set(oChildIter, 0, sName, 8, oCard, 9, IPhysicalCard((oCard, None)))
                aExpansionInfo = self.get_expansion_info(oCard, fGetExpanInfo(oItem))
                for oPhysCard, sExpansion in aExpansionInfo:
                    oExpansionIter = self.append(oChildIter)
                    self.set(oExpansionIter, 0, sExpansion, 9, oPhysCard)

                bEmpty = False

            aTexts, aIcons = self.lookup_icons(sGroup)
            if aTexts:
                self.set(oSectionIter, 0, sGroup, 5, aTexts, 6, aIcons)
            else:
                self.set(oSectionIter, 0, sGroup)

        if bEmpty:
            self.oEmptyIter = self.append(None)
            sText = self._get_empty_text()
            self.set(self.oEmptyIter, 0, sText)
        MessageBus.publish(self, 'load', aCards)
        if iSortColumn is not None:
            self.set_sort_column_id(iSortColumn, iSortOrder)
        return

    def get_card_iterator(self, oFilter):
        """Return an interator over the card model.

           The filter is combined with self.basefilter. None may be used to
           retrieve the entire card list (with only the base filter
           restriciting which cards appear).
           """
        oFilter = self.combine_filter_with_base(oFilter)
        return oFilter.select(self.cardclass).distinct()

    def grouped_card_iter(self, oCardIter):
        """Return iterator over the card list grouping.

           Returns a triple of fGetCard (the function used to
           retrieve a card from an item), fGetCount (the function used to
           retrieve a card count from an item) and oGroupedIter (an iterator
           over the card groups)
           """
        aCards = []
        fGetCard = lambda x: x[0]
        fGetCount = lambda x: x[1][0]
        fGetExpanInfo = lambda x: x[1][1]
        dAbsCards = {}
        for oPhysCard in oCardIter:
            if not self.check_card_visible(oPhysCard):
                continue
            oAbsCard = IAbstractCard(oPhysCard)
            aCards.append(oPhysCard)
            dAbsCards.setdefault(oAbsCard, [0, {}])
            dAbsCards[oAbsCard][0] += 1
            if self.bExpansions:
                dExpanInfo = dAbsCards[oAbsCard][1]
                dExpanInfo.setdefault(oPhysCard, 0)
                dExpanInfo[oPhysCard] += 1

        aAbsCards = list(dAbsCards.iteritems())
        return (
         fGetCard, fGetCount, fGetExpanInfo,
         self.groupby(aAbsCards, fGetCard), aCards)

    def is_filtered(self):
        """Helper method for checking filtered state with the config filter"""
        return self._bApplyFilter or self._oConfigFilter is not None

    def get_current_filter(self):
        """Get the current applied filter.

           This is also responsible for handling the not legal filter case
           and any filter specified by the profile."""
        if self.configfilter:
            if self.applyfilter and self._bHideIllegal and self.selectfilter:
                return FilterAndBox([self.configfilter, self.selectfilter,
                 self.oLegalFilter])
            if self._bHideIllegal:
                return FilterAndBox([self.configfilter, self.oLegalFilter])
            if self.applyfilter and self.selectfilter:
                return FilterAndBox([self.configfilter, self.selectfilter])
            return self.configfilter
        else:
            if self.applyfilter and self._bHideIllegal and self.selectfilter:
                return FilterAndBox([self.selectfilter, self.oLegalFilter])
            if self._bHideIllegal:
                return self.oLegalFilter
            if self.applyfilter:
                return self.selectfilter
            return

    def combine_filter_with_base(self, oOtherFilter):
        """Return the combination of oOtherFilter with the base filter.

           This handles the cases where either filter is None properly."""
        if self.basefilter is None and oOtherFilter is None:
            return NullFilter()
        else:
            if self.basefilter is None:
                return oOtherFilter
            if oOtherFilter is None:
                return self.basefilter
            return FilterAndBox([self.basefilter, oOtherFilter])

    def get_card_name_from_path(self, oPath):
        """Get the card name associated with the current path. Handle the
           expansion level transparently."""
        oIter = self.get_iter(oPath)
        return self.get_card_name_from_iter(oIter)

    def get_card_name_from_iter(self, oIter):
        """Get the card name associated with the current iter. Handle the
           expansion level transparently."""
        oCard = self.get_abstract_card_from_iter(oIter)
        if oCard:
            return oCard.name
        return self.get_name_from_iter(oIter)

    def get_abstract_card_from_path(self, oPath):
        """Get the abstract card name for the current path."""
        oIter = self.get_iter(oPath)
        return self.get_abstract_card_from_iter(oIter)

    def get_physical_card_from_path(self, oPath):
        """Get the physical card name for the current path."""
        try:
            oIter = self.get_iter(oPath)
            return self.get_physical_card_from_iter(oIter)
        except ValueError:
            logging.warn('Invalid path (%s) in get_physical_card_from_path', oPath)
            return

        return

    def check_card_visible(self, oPhysCard):
        """Returns true if oPhysCard should be shown.

           Used by plugins to allow extra filtering of cards."""
        return True

    def get_all_iter_children(self, oIter):
        """Get a list of all the subiters of this iter"""
        aChildIters = []
        oChildIter = self.iter_children(oIter)
        while oChildIter:
            aChildIters.append(oChildIter)
            oChildIter = self.iter_next(oChildIter)

        return aChildIters

    def get_all_from_iter(self, oIter):
        """Get all relevent information about the current iter.

           Returns the tuple (CardName, Expansion info, Card Count,
           depth in the  model), where depth in the model is 1 for the top
           level of cards, and 2 for the expansion level.
           """
        iDepth = self.iter_depth(oIter)
        if iDepth == 0:
            return (
             None, None, 0, iDepth)
        else:
            sCardName = self.get_card_name_from_iter(oIter)
            if iDepth == 2:
                sExpansion = self.get_value(oIter, 0)
            else:
                sExpansion = None
            iCount = self.get_value(oIter, 1)
            return (sCardName, sExpansion, iCount, iDepth)

    def get_all_from_path(self, oPath):
        """Get all relevent information about the current path.

           Conveince wrapper around get_all_from_iter, for use in cases when
           it's easier to get the path than the iter (selections, etc.)
           """
        if oPath:
            oIter = self.get_iter(oPath)
            return self.get_all_from_iter(oIter)
        else:
            return (None, None, None, None)

    def get_child_entries_from_iter(self, oIter):
        """Return a list of (sExpansion, iCount) pairs for the children of
           this path"""
        aChildren = []
        iDepth = self.iter_depth(oIter)
        if iDepth != 1:
            return aChildren
        oChildIter = self.iter_children(oIter)
        while oChildIter:
            oPhysCard = self.get_value(oChildIter, 9)
            iCount = self.get_value(oChildIter, 1)
            aChildren.append((oPhysCard, iCount))
            oChildIter = self.iter_next(oChildIter)

        return aChildren

    def get_inc_dec_flags_from_path(self, oPath):
        """Get the settings of the inc + dec flags for the current path"""
        oIter = self.get_iter(oPath)
        bInc = self.get_value(oIter, 3)
        bDec = self.get_value(oIter, 4)
        return (bInc, bDec)

    def get_exp_name_from_path(self, oPath):
        """Get the expansion information from the model, returning None if this
           is not at a level where the expansion is known."""
        oIter = self.get_iter(oPath)
        if self.iter_depth(oIter) != 2:
            return None
        else:
            return self.get_name_from_iter(oIter)

    def get_name_from_iter(self, oIter):
        """Extract the value at oIter from the model, correcting for encoding
           issues."""
        sName = self.get_value(oIter, 0).decode('utf-8')
        return sName

    def get_card_count_from_iter(self, oIter):
        """Return the card count for a given iterator"""
        return self.get_value(oIter, 1)

    def get_parent_count_from_iter(self, oIter):
        """Return the parent count for a given iterator"""
        return self.get_value(oIter, 2)

    def get_abstract_card_from_iter(self, oIter):
        """Extract the Abstract Card at oIter from the model"""
        while self.iter_depth(oIter) > 1:
            oIter = self.iter_parent(oIter)

        return self.get_value(oIter, 8)

    def get_physical_card_from_iter(self, oIter):
        """Extract the Physical Card at oIter from the model"""
        return self.get_value(oIter, 9)

    def _get_empty_text(self):
        """Get the correct text for an empty model."""
        if self.get_card_iterator(None).count() == 0:
            sText = 'Empty'
        else:
            sText = 'No Cards found'
        return sText

    def _change_config_filter(self, sFilter):
        """Update the config filter when needed"""
        if sFilter == self._sCurConfigFilter:
            return False
        else:
            self._sCurConfigFilter = sFilter
            sFilterText = self._oConfig.get_filter(sFilter)
            oFilter = None
            if sFilterText:
                oAST = self._oFilterParser.apply(sFilterText)
                if oAST:
                    try:
                        oFilter = oAST.get_filter()
                    except RuntimeError as oErr:
                        do_exception_complaint('Failed to load Filter: %s' % oErr)

            if oFilter == self._oConfigFilter:
                return False
            self._oConfigFilter = oFilter
            return True

    def _change_level_mode(self, bLevel):
        """Set which extra information is shown."""
        if self.bExpansions != bLevel:
            self.bExpansions = bLevel
            return True
        return False

    def _change_icon_mode(self, bMode):
        """Set whether icons should be shown."""
        if self.bUseIcons != bMode:
            self.bUseIcons = bMode
            return True
        return False

    def _change_illegal_mode(self, bMode):
        """Set whether illegal cards should be shown."""
        if self._bHideIllegal != bMode:
            self._bHideIllegal = bMode
            return True
        return False

    def update_options(self, bSkipLoad=False):
        """Respond to config file changes"""
        sProfile = self._oConfig.get_profile(FULL_CARDLIST, FULL_CARDLIST)
        sExpMode = self._oConfig.get_profile_option(FULL_CARDLIST, sProfile, EXTRA_LEVEL_OPTION).lower()
        bExpMode = EXTRA_LEVEL_LOOKUP.get(sExpMode, True)
        bUseIcons = self._oConfig.get_profile_option(FULL_CARDLIST, sProfile, USE_ICONS)
        bHideIllegal = self._oConfig.get_profile_option(FULL_CARDLIST, sProfile, HIDE_ILLEGAL)
        sConfigFilter = self._oConfig.get_profile_option(FULL_CARDLIST, sProfile, 'filter')
        bReloadFilter = self._change_config_filter(sConfigFilter)
        bReloadELM = self._change_level_mode(bExpMode)
        bReloadIcons = self._change_icon_mode(bUseIcons)
        bReloadIllegal = self._change_illegal_mode(bHideIllegal)
        if not self._oController:
            return
        if not bSkipLoad and (bReloadELM or bReloadIcons or bReloadIllegal or bReloadFilter):
            self._oController.frame.queue_reload()

    def profile_option_changed(self, sType, _sProfile, _sKey):
        """One of the per-deck configuration items changed."""
        if sType != FULL_CARDLIST:
            return
        self.update_options()

    def profile_changed(self, sType, sId):
        """A profile option changed with a cardset changed."""
        if sType != FULL_CARDLIST or sId != FULL_CARDLIST:
            return
        self.update_options()

    def replace_filter(self, sKey, _sOldFilter, _sNewFilter):
        """Reload if the current config has changed"""
        if sKey == self._sCurConfigFilter:
            self._sCurConfigFilter = None
            if self._change_config_filter(sKey):
                self._oController.frame.queue_reload()
        return