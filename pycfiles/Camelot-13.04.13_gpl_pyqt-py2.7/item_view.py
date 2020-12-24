# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/action_steps/item_view.py
# Compiled at: 2013-04-11 17:47:52
"""
Various ``ActionStep`` subclasses that manipulate the `item_view` of 
the `ListActionGuiContext`.
"""
from PyQt4.QtCore import Qt
from camelot.admin.action.base import ActionStep

class Sort(ActionStep):

    def __init__(self, column, order=Qt.AscendingOrder):
        """Sort the items in the item view ( list, table or tree )
        
        :param column: the index of the column on which to sort
        :param order: a :class:`Qt.SortOrder`
        """
        self.column = column
        self.order = order

    def gui_run(self, gui_context):
        if gui_context.item_view != None:
            model = gui_context.item_view.model()
            model.sort(self.column, self.order)
        return