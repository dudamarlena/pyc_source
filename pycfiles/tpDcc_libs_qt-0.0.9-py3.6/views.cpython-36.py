# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/widgets/views.py
# Compiled at: 2020-04-24 23:12:07
# Size of source mod 2**32: 7490 bytes
"""
Module that contains base classes for list views
"""
from __future__ import print_function, division, absolute_import
import os, glob
from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt.QtGui import *
from tpDcc.libs.python import python
from tpDcc.libs.qt.widgets import models

class BaseListView(QListView, object):
    __doc__ = '\n    Base class for list views\n    '

    def __ini__(self, parent=None):
        super(BaseListView, self).__init__(parent=parent)


class ListView(BaseListView, object):
    __doc__ = '\n    Extends basic QListView functionality\n    '
    current_selection_changed = Signal(object, object)
    middle_clicked = Signal(QModelIndex)

    def __init__(self, parent=None):
        super(ListView, self).__init__(parent)

    def appendItem(self, item):
        """
        Adds a new item to the list view model
        :param item: variant
        """
        if self.model():
            self.model().appendItem(item)

    def selectionChanged(self, selected, deselected):
        self.current_selection_changed.emit(models.ItemSelection(selected), models.ItemSelection(deselected))
        super(ListView, self).selectionChanged(models.ItemSelection(selected), models.ItemSelection(deselected))

    def selectedIndexes(self):
        """
        Override selectedIndexes behavior
        :warning: This method is override to avoid  a Qt 4.7.0 QModelIndexList destructor crash.
            See ItemSelection for more information.
        """
        item_selection = models.ItemSelection(self.selectionModel().selection())
        return item_selection.indexes()

    def mousePressEvent(self, event):
        if event.button() == Qt.MidButton:
            model_index = self.indexAt(event.pos())
            if model_index.row() >= 0:
                self.middle_clicked.emit(model_index)
        super(ListView, self).mousePressEvent(event)


class DraggableListView(ListView, object):
    __doc__ = '\n    Extends ListView functionality width draggable functionality\n    '
    addedItemDir = Signal(list)

    def __init__(self, parent=None):
        super(DraggableListView, self).__init__(parent=parent)
        self._accepted_files = list()
        self.setEditTriggers(QListView.NoEditTriggers)
        self.setDragEnabled(True)
        self.setDragDropMode(QListView.DragOnly)
        self.setDefaultDropAction(Qt.IgnoreAction)
        self.setAcceptDrops(True)
        self.setIconSize(QSize(120, 120))
        self.setViewMode(QListView.IconMode)
        self.setMovement(QListView.Snap)
        self.setResizeMode(QListView.Adjust)
        self.setUniformItemSizes(True)
        self.setMouseTracking(True)

    def startDrag(self, supported_actions):
        """
        Function that is called when we start dragging an item
        This function set ups the mime data and creates a copy of the image
        of the item that is show in cursor position while dragging action
        is enabled
        """
        index = self.currentIndex()
        model = self.model()
        item = model.itemFromIndex(index)
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setData('item_text', QByteArray(str(item.text())))
        mime_data.setData('item_size', QByteArray('%.1f %.1f' % (item.size.width(), item.size.height())))
        url = QUrl.fromLocalFile(item.text())
        mime_data.setUrls(url)
        drag.setMimeData(mime_data)
        pixmap = item.icon().pixmap(50, 50)
        drag.setDragCursor(pixmap, Qt.CopyAction)
        drag.start()

    def dragEnterEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            for path in map(lambda x: x.toLocalFile(), mime_data.urls()):
                if os.path.isdir(path) or os.path.isfile(path) and os.path.splitext(path)[(-1)].lower() in self._accepted_files:
                    self.setDragDropMode(QListView.InternalMove)
                    event.accept()
                    break

        super(DraggableListView, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        event.accept()
        super(DraggableListView, self).dragMoveEvent(event)

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            send_data = list()
            for path in map(lambda x: x.toLocalFile(), mime_data.urls()):
                for file in self._accepted_files:
                    if os.path.isdir(path) and glob.glob(os.path.join(path, '*' + file)) or os.path.isfile(path) and os.path.splitext(path)[(-1)].lower() == file:
                        send_data.append(path)

            if send_data:
                self.addedItemDir.emit(send_data)
            self.setDragEnabled(True)
            self.setDragDropMode(QListView.DragOnly)
            self.setDefaultDropAction(Qt.IgnoreAction)
            self.setAcceptDrops(True)
            super(DraggableListView, self).dropEvent(event)

    def set_accepted_files(self, list_files):
        list_files = python.force_list(list_files)
        for f in list_files:
            if not f.startswith('.'):
                f = '.' + f
            self._accepted_files.append(f)


class BaseTableView(QTableView, object):

    def __init__(self, parent=None, **kwargs):
        (super(BaseTableView, self).__init__)(parent=parent, **kwargs)
        self._last_indexes = list()
        self.installEventFilter(self)

    def focusOutEvent(self, event):
        if self.selectionModel().selectedIndexes():
            for index in self.selectionModel().selectedRows():
                self._last_indexes.append(QPersistentModelIndex(index))

        if self._last_indexes:
            for i in self._last_indexes:
                self.selectionModel().setCurrentIndex(i, QItemSelectionModel.Select)

        event.accept()

    def get_selected_indexes(self):
        """
        Returns the selected indexes
        """
        return self.selectionModel().selectedIndexes()

    def get_selected_rows(self):
        """
        Returns the selected rows
        """
        return self.selectionModel().selectedRows()


class BaseTreeView(QTreeView, object):
    __doc__ = '\n    Base class for tree views\n    '

    def __init__(self, parent=None):
        super(BaseTreeView, self).__init__(parent=parent)

    def expand_tree(self, root_node):
        """
        Expands all the collapsed elements in a tree starting at the rootNode
        :param root_node: Start node from which we start expanding the tree
        """
        parent = root_node.parent()
        parent_id = self.model().createIndex(parent.row(), 0, parent) if parent else QModelIndex()
        index = self.model().index(root_node.row(), 0, parent_id)
        self.setExpanded(index, True)
        for child in root_node.children:
            self.expand_tree(child)