# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/modeltree.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = 'custom tree and tree-items widgets'
import logging
logger = logging.getLogger('camelot.view.controls.modeltree')
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from camelot.core.utils import ugettext as _

class ModelItem(QtGui.QTreeWidgetItem):
    """Custom tree item widget"""

    def __init__(self, parent, columns_names, section_item):
        logger.debug('creating new modelitem')
        super(ModelItem, self).__init__(parent, columns_names)
        self.textColumn = 0
        self.iconColumn = 1
        self.section_item = section_item
        for column in (self.textColumn, self.iconColumn):
            self.setToolTip(column, _('Right click to open in New Tab'))

    def _underline(self, enable=False):
        font = self.font(self.textColumn)
        font.setUnderline(enable)
        self.setFont(self.textColumn, font)

    def set_icon(self, icon):
        self.setIcon(self.iconColumn, icon)


class ModelTree(QtGui.QTreeWidget):
    """Custom tree widget"""

    def __init__(self, header_labels=[
 ''], parent=None):
        logger.debug('creating new modeltree')
        super(ModelTree, self).__init__(parent)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.setMouseTracking(True)
        self.header_labels = header_labels
        self.setColumnCount(2)
        self.setColumnWidth(0, 160)
        self.setColumnWidth(1, 18)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSelectionBehavior(self.SelectRows)
        self.clear_model_items()
        self.clear_section_items()
        self.fix_header_labels()

    def resizeEvent(self, event):
        self.setColumnWidth(0, self.width() - 30)

    def fix_header_labels(self):
        self.setHeaderHidden(True)

    def clear_section_items(self):
        self.section_items = []

    def clear_model_items(self):
        self.modelitems = []

    def mousePressEvent(self, event):
        """Custom context menu"""
        if event.button() == Qt.RightButton:
            self.customContextMenuRequested.emit(event.pos())
            event.accept()
        else:
            QtGui.QTreeWidget.mousePressEvent(self, event)

    def leaveEvent(self, event):
        if not self.modelitems:
            return
        for item in self.modelitems:
            item._underline(False)

    def mouseMoveEvent(self, event):
        if not self.modelitems:
            return
        for item in self.modelitems:
            item._underline(False)

        item = self.itemAt(self.mapFromGlobal(self.cursor().pos()))
        if item:
            item._underline(True)