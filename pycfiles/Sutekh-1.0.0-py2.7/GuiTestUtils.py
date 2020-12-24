# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/tests/GuiTestUtils.py
# Compiled at: 2019-12-11 16:37:52
"""Utilities and support classes that are useful for testing bits of the
   gui."""
from ..core.BaseAdapters import IAbstractCard
from ..gui.MessageBus import MessageBus
from ..gui.CardSetListModel import IGNORE_PARENT, NO_SECOND_LEVEL, THIS_SET_ONLY

class TestListener(object):
    """Listener used in the test cases.

       Pass bKeepCards to keep a copy of the all the cards passed to the
       listener for validation checks."""

    def __init__(self, oModel, bKeepCards):
        self.bLoadCalled = False
        self.iCnt = 0
        self.aCards = []
        self._bKeepCards = bKeepCards
        MessageBus.subscribe(oModel, 'load', self.load)
        MessageBus.subscribe(oModel, 'alter_card_count', self.alter_count)
        MessageBus.subscribe(oModel, 'add_new_card', self.alter_count)

    def load(self, aCards):
        """Called when the model is loaded."""
        self.bLoadCalled = True
        self.iCnt = len(aCards)
        if self._bKeepCards:
            self.aCards = [ IAbstractCard(oCard) for oCard in aCards ]

    def alter_count(self, _oCard, iChg):
        """Called when the model alters the card count or adds cards"""
        self.iCnt += iChg


class DummyCardSetController(object):
    """Dummy controller object for config tests"""

    def __init__(self):
        self.bReload = False

    view = property(fget=lambda self: self)
    frame = property(fget=lambda self: self)
    pane_id = property(fget=lambda self: 10)
    config_frame_id = property(fget=lambda self: 'pane10')

    def set_parent_count_col_vis(self, _bVal):
        pass

    def reload_keep_expanded(self):
        pass

    def queue_reload(self):
        self.bReload = True


def count_all_cards(oModel):
    """Count all the entries in the model."""
    iTotal = 0
    oIter = oModel.get_iter_first()
    while oIter:
        iTotal += oModel.iter_n_children(oIter)
        oIter = oModel.iter_next(oIter)

    return iTotal


def count_second_level(oModel):
    """Count all the second level entries in the model."""
    iTotal = 0
    oIter = oModel.get_iter_first()
    while oIter:
        oChildIter = oModel.iter_children(oIter)
        while oChildIter:
            iTotal += oModel.iter_n_children(oChildIter)
            oChildIter = oModel.iter_next(oChildIter)

        oIter = oModel.iter_next(oIter)

    return iTotal


def _get_all_child_counts(oModel, oIter, sName=''):
    """Recursively descend the children of oIter, getting all the
       relevant info."""
    aList = []
    oChildIter = oModel.iter_children(oIter)
    while oChildIter:
        if sName:
            sListName = sName + ':' + oModel.get_value(oChildIter, 0)
        else:
            sListName = oModel.get_value(oChildIter, 0)
        aList.append((oModel.get_value(oChildIter, 1),
         oModel.get_value(oChildIter, 2), sListName))
        if oModel.iter_n_children(oChildIter) > 0:
            oGCIter = oModel.iter_children(oChildIter)
            while oGCIter:
                sGCName = sListName + ':' + oModel.get_value(oGCIter, 0)
                if oModel.iter_n_children(oGCIter) > 0:
                    aList.extend(_get_all_child_counts(oModel, oGCIter, sGCName))
                else:
                    aList.append((oModel.get_value(oGCIter, 1),
                     oModel.get_value(oGCIter, 2), sGCName))
                oGCIter = oModel.iter_next(oGCIter)

        oChildIter = oModel.iter_next(oChildIter)

    return aList


def get_all_counts(oModel):
    """Return a list of iCnt, iParCnt, sCardName tuples from the Model"""
    return sorted(_get_all_child_counts(oModel, None))


def count_top_level(oModel):
    """Count all the top level entries in the model."""
    iTotal = oModel.iter_n_children(None)
    return iTotal


def get_card_names(oModel):
    """Return a set of all the cards listed in the model"""
    oIter = oModel.get_iter_first()
    aResults = set()
    while oIter:
        oChildIter = oModel.iter_children(oIter)
        while oChildIter:
            aResults.add(oModel.get_value(oChildIter, 0))
            oChildIter = oModel.iter_next(oChildIter)

        oIter = oModel.iter_next(oIter)

    return aResults


def reset_modes(oModel):
    """Set the model to the minimal state."""
    oModel._change_parent_count_mode(IGNORE_PARENT)
    oModel._change_level_mode(NO_SECOND_LEVEL)
    oModel.bEditable = False
    oModel._change_count_mode(THIS_SET_ONLY)


def cleanup_models(aModels):
    """Utility function to cleanup models signals, etc."""
    for oModel in aModels:
        oModel.cleanup()