# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/inheritance.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = 'Controls related to visualizing object hierarchy'
import logging
logger = logging.getLogger('camelot.view.controls.inheritance')
from PyQt4 import QtGui
from PyQt4 import QtCore
from camelot.view.model_thread import post
from camelot.view.controls.modeltree import ModelTree
from camelot.view.controls.modeltree import ModelItem
QT_MAJOR_VERSION = float(('.').join(str(QtCore.QT_VERSION_STR).split('.')[0:2]))

class SubclassItem(ModelItem):

    def __init__(self, parent, admin):
        ModelItem.__init__(self, parent, [admin.get_verbose_name()], None)
        self.admin = admin
        return


class SubclassTree(ModelTree):
    """Widget to select subclasses of a certain entity, where the subclasses
    are represented in a tree

    emits subclassClicked when a subclass has been selected
    """
    subclass_clicked_signal = QtCore.pyqtSignal(object)

    def __init__(self, admin, parent):
        header_labels = [
         'Types']
        ModelTree.__init__(self, header_labels, parent)
        self.admin = admin
        self.subclasses = []
        post(self.admin.get_subclass_tree, self.setSubclasses)
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.clicked.connect(self.emit_subclass_clicked)

    def setSubclasses(self, subclasses):
        logger.debug('setting subclass tree')
        self.subclasses = subclasses

        def append_subclasses(class_item, subclasses):
            for subclass_admin, subsubclasses in subclasses:
                subclass_item = SubclassItem(class_item, subclass_admin)
                self.modelitems.append(subclass_item)
                append_subclasses(subclass_item, subsubclasses)

        if len(subclasses):
            self.clear_model_items()
            top_level_item = SubclassItem(self, self.admin)
            self.modelitems.append(top_level_item)
            append_subclasses(top_level_item, subclasses)
            top_level_item.setExpanded(True)
            self.setMaximumWidth(self.fontMetrics().width(' ') * 70)
        else:
            self.setMaximumWidth(0)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def emit_subclass_clicked(self, index):
        logger.debug('subclass clicked at position %s' % index.row())
        item = self.itemFromIndex(index)
        self.subclass_clicked_signal.emit(item.admin)


class SubclassDialog(QtGui.QDialog):
    """A dialog requesting the user to select a subclass"""

    def __init__(self, parent, admin):
        QtGui.QDialog.__init__(self, parent)
        subclass_tree = SubclassTree(admin, self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(subclass_tree)
        layout.addStretch(1)
        self.setLayout(layout)
        self.selected_subclass = None
        subclass_tree.subclass_clicked_signal.connect(self._subclass_clicked)
        return

    @QtCore.pyqtSlot(object)
    def _subclass_clicked(self, admin):
        self.selected_subclass = admin
        self.accept()