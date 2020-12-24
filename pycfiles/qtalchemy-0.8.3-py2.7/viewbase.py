# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/qtalchemy/widgets/viewbase.py
# Compiled at: 2012-06-23 09:45:15
from qtalchemy import writeTableColumnGeo

class ViewBase(object):
    """
    This handles functions common to TreeView and TableView.  At this 
    point, it's innards are not well encapsulated, but at least the 
    code is not duplicated.
    """

    def nextIndex(self, index):
        model = self.model()
        if index.column() + 1 < model.columnCount(index.parent()):
            return model.index(index.row(), index.column() + 1, index.parent())
        else:
            if index.row() + 1 < model.rowCount(index.parent()):
                return model.index(index.row() + 1, 0, index.parent())
            return model.index(0, 0, index.parent())

    def prevIndex(self, index):
        model = self.model()
        if index.column() > 0:
            return model.index(index.row(), index.column() - 1, index.parent())
        else:
            if index.row() > 0:
                return model.index(index.row() - 1, model.columnCount(index.parent()) - 1, index.parent())
            return model.index(model.rowCount(index.parent()) - 1, model.columnCount(index.parent()) - 1, index.parent())

    def delKeyPressed(self):
        model = self.model()
        index = self.currentIndex()
        model.removeRows(index.row(), 1, index.parent())

    def saveSections(self):
        if self.property('ExtensionId') is not None and self.model() is not None:
            writeTableColumnGeo(self, self.property('ExtensionId'))
        return