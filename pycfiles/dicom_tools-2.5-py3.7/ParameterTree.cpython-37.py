# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/parametertree/ParameterTree.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 5662 bytes
from ..Qt import QtCore, QtGui
import widgets.TreeWidget as TreeWidget
import os, weakref, re
from .ParameterItem import ParameterItem

class ParameterTree(TreeWidget):
    __doc__ = 'Widget used to display or control data from a hierarchy of Parameters'

    def __init__(self, parent=None, showHeader=True):
        """
        ============== ========================================================
        **Arguments:**
        parent         (QWidget) An optional parent widget
        showHeader     (bool) If True, then the QTreeView header is displayed.
        ============== ========================================================
        """
        TreeWidget.__init__(self, parent)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.setAnimated(False)
        self.setColumnCount(2)
        self.setHeaderLabels(['Parameter', 'Value'])
        self.setAlternatingRowColors(True)
        self.paramSet = None
        self.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.setHeaderHidden(not showHeader)
        self.itemChanged.connect(self.itemChangedEvent)
        self.lastSel = None
        self.setRootIsDecorated(False)

    def setParameters(self, param, showTop=True):
        """
        Set the top-level :class:`Parameter <pyqtgraph.parametertree.Parameter>`
        to be displayed in this ParameterTree.

        If *showTop* is False, then the top-level parameter is hidden and only 
        its children will be visible. This is a convenience method equivalent 
        to::
        
            tree.clear()
            tree.addParameters(param, showTop)
        """
        self.clear()
        self.addParameters(param, showTop=showTop)

    def addParameters(self, param, root=None, depth=0, showTop=True):
        """
        Adds one top-level :class:`Parameter <pyqtgraph.parametertree.Parameter>`
        to the view. 
        
        ============== ==========================================================
        **Arguments:** 
        param          The :class:`Parameter <pyqtgraph.parametertree.Parameter>` 
                       to add.
        root           The item within the tree to which *param* should be added.
                       By default, *param* is added as a top-level item.
        showTop        If False, then *param* will be hidden, and only its 
                       children will be visible in the tree.
        ============== ==========================================================
        """
        item = param.makeTreeItem(depth=depth)
        if root is None:
            root = self.invisibleRootItem()
            if not showTop:
                item.setText(0, '')
                item.setSizeHint(0, QtCore.QSize(1, 1))
                item.setSizeHint(1, QtCore.QSize(1, 1))
                depth -= 1
        root.addChild(item)
        item.treeWidgetChanged()
        for ch in param:
            self.addParameters(ch, root=item, depth=(depth + 1))

    def clear(self):
        """
        Remove all parameters from the tree.        
        """
        self.invisibleRootItem().takeChildren()

    def focusNext(self, item, forward=True):
        """Give input focus to the next (or previous) item after *item*
        """
        while True:
            parent = item.parent()
            if parent is None:
                return
            nextItem = self.nextFocusableChild(parent, item, forward=forward)
            if nextItem is not None:
                nextItem.setFocus()
                self.setCurrentItem(nextItem)
                return
            item = parent

    def focusPrevious(self, item):
        self.focusNext(item, forward=False)

    def nextFocusableChild(self, root, startItem=None, forward=True):
        if startItem is None:
            if forward:
                index = 0
            else:
                index = root.childCount() - 1
        elif forward:
            index = root.indexOfChild(startItem) + 1
        else:
            index = root.indexOfChild(startItem) - 1
        if forward:
            inds = list(range(index, root.childCount()))
        else:
            inds = list(range(index, -1, -1))
        for i in inds:
            item = root.child(i)
            if hasattr(item, 'isFocusable'):
                if item.isFocusable():
                    return item
            item = self.nextFocusableChild(item, forward=forward)
            if item is not None:
                return item

    def contextMenuEvent(self, ev):
        item = self.currentItem()
        if hasattr(item, 'contextMenuEvent'):
            item.contextMenuEvent(ev)

    def itemChangedEvent(self, item, col):
        if hasattr(item, 'columnChangedEvent'):
            item.columnChangedEvent(col)

    def selectionChanged(self, *args):
        sel = self.selectedItems()
        if len(sel) != 1:
            sel = None
        if self.lastSel is not None:
            if isinstance(self.lastSel, ParameterItem):
                self.lastSel.selected(False)
        if sel is None:
            self.lastSel = None
            return
        self.lastSel = sel[0]
        if hasattr(sel[0], 'selected'):
            sel[0].selected(True)
        return (TreeWidget.selectionChanged)(self, *args)

    def wheelEvent(self, ev):
        self.clearSelection()
        return TreeWidget.wheelEvent(self, ev)