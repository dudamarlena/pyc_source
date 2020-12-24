# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/CardSetFrame.py
# Compiled at: 2019-12-11 16:37:48
"""Sutekh Frame for holding Card Sets"""
from sqlobject import SQLObjectNotFound
from ..core.BaseTables import PhysicalCardSet
from ..core.BaseAdapters import IPhysicalCardSet
from .CardListFrame import CardListFrame
from .CardSetMenu import CardSetMenu
from .CardSetController import CardSetController

class CardSetFrame(CardListFrame):
    """class for Card Set frames.

       Handles most of the functionality - subclasses set the style name
       and the various other properties correctly for the type.
       """
    _cModelType = PhysicalCardSet

    def __init__(self, oMainWindow, sName, bStartEditable, cPCSWriter):
        super(CardSetFrame, self).__init__(oMainWindow)
        try:
            _oCS = IPhysicalCardSet(sName)
        except SQLObjectNotFound:
            raise RuntimeError('Card Set %s does not exist' % sName)

        self._oController = CardSetController(sName, oMainWindow, self, bStartEditable)
        self._sName = sName
        self.init_plugins()
        self._oMenu = CardSetMenu(self, self._oController, self._oMainWindow, cPCSWriter)
        self.set_name('physical card set card list')
        self.add_parts()
        self.update_name(sName)

    name = property(fget=lambda self: self._sName, doc='Frame Name')
    cardset_name = property(fget=lambda self: self._oController.view.sSetName, doc='Name of the card set for this frame')

    def cleanup(self, bQuit=False):
        """Cleanup function called before pane is removed by the Main Window"""
        super(CardSetFrame, self).cleanup(bQuit)
        if not bQuit:
            self._oMainWindow.reload_pcs_list()
        self._oController.cleanup()

    def update_name(self, sNewName):
        """Update the frame name to the current card set name."""
        iCount = 0
        sFinalName = sNewName
        aOtherOpenSets = [ x.title for x in self._oMainWindow.find_cs_pane_by_set_name(sNewName) if x is not self
                         ]
        while sFinalName in aOtherOpenSets:
            iCount += 1
            sFinalName = '%s (%d)' % (sNewName, iCount)

        self._sName = sFinalName
        self.set_title(self._sName)

    def is_card_set(self, sSetName):
        """Return true if we're a copy of the given set"""
        return self.cardset_name == sSetName

    def update_to_new_db(self):
        """Re-associate internal data against the database.

           Needed for re-reading WW cardlists and such.
           Instruct controller + model to update themselves,
           then reload.
           """
        self._oController.update_to_new_db()
        self.reload()