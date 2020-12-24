# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/PhysicalCardView.py
# Compiled at: 2019-12-11 16:37:48
"""Provide a TreeView for the physical card collection"""
import gtk
from .CardListView import CardListView
from .CardListModel import CardListModel
from .CellRendererIcons import CellRendererIcons

class PhysicalCardView(CardListView):
    """The card list view for the physical card collection.

       Special cases Editable card list with those properties
       needed for the card collection - the drag prefix, the
       card_drop handling and handling of pasted data.
       """
    sDragPrefix = 'Phys:'

    def __init__(self, oController, oWindow, oConfig):
        oModel = CardListModel(oConfig)
        oModel.enable_sorting()
        super(PhysicalCardView, self).__init__(oController, oWindow, oModel, oConfig)
        self.oNameCell = CellRendererIcons(5)
        oColumn = gtk.TreeViewColumn('Cards', self.oNameCell, text=0, textlist=5, icons=6)
        oColumn.set_expand(True)
        oColumn.set_resizable(True)
        oColumn.set_sort_column_id(0)
        self.append_column(oColumn)
        self.set_expander_column(oColumn)