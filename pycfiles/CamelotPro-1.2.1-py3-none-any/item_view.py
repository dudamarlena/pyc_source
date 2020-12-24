# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/action_steps/item_view.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\nVarious ``ActionStep`` subclasses that manipulate the `item_view` of \nthe `ListActionGuiContext`.\n'
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