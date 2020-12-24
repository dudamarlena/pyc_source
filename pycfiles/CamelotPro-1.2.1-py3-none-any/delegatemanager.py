# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/delegatemanager.py
# Compiled at: 2013-04-11 17:47:52
import logging
logger = logging.getLogger('camelot.view.controls.delegates.delegatemanager')
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

class DelegateManager(QtGui.QItemDelegate):
    """Manages custom delegates, should not be used by the application
  developer
  """

    def __init__(self, parent=None, **kwargs):
        QtGui.QItemDelegate.__init__(self, parent)
        self.delegates = {}

    def set_columns_desc(self, columnsdesc):
        self.columnsdesc = columnsdesc

    def get_column_delegate(self, column):
        try:
            return self.delegates[column]
        except KeyError:
            logger.error('Programming Error, no delegate available for column %s' % column)
            logger.error('Available columns : %s' % unicode(self.delegates.keys()))
            raise KeyError

    def insertColumnDelegate(self, column, delegate):
        """Inserts a custom column delegate"""
        logger.debug('inserting delegate for column %s' % column)
        assert delegate != None
        delegate.setParent(self)
        self.delegates[column] = delegate
        delegate.commitData.connect(self._commit_data)
        delegate.closeEditor.connect(self._close_editor)
        return

    def _commit_data(self, editor):
        self.commitData.emit(editor)

    @QtCore.pyqtSlot(QtGui.QWidget, QtGui.QAbstractItemDelegate.EndEditHint)
    def _close_editor(self, editor, hint):
        self.closeEditor.emit(editor, hint)

    def removeColumnDelegate(self, column):
        """Removes custom column delegate"""
        logger.debug('removing a custom column delegate')
        if column in self.delegates:
            del self.delegates[column]

    def paint(self, painter, option, index):
        """Use a custom delegate paint method if it exists"""
        delegate = self.get_column_delegate(index.column())
        delegate.paint(painter, option, index)

    def createEditor(self, parent, option, index):
        """Use a custom delegate createEditor method if it exists"""
        try:
            delegate = self.get_column_delegate(index.column())
            editor = delegate.createEditor(parent, option, index)
        except Exception as e:
            logger.error('Programming Error : could not createEditor editor data for editor at column %s' % index.column(), exc_info=e)
            return QtGui.QWidget(parent=parent)

        return editor

    def setEditorData(self, editor, index):
        """Use a custom delegate setEditorData method if it exists"""
        logger.debug('setting editor data for column %s' % index.column())
        try:
            delegate = self.get_column_delegate(index.column())
            delegate.setEditorData(editor, index)
        except Exception as e:
            logger.error('Programming Error : could not set editor data for editor at column %s' % index.column(), exc_info=e)
            logger.error('value that could not be set : %s' % unicode(index.model().data(index, Qt.EditRole)))

    def setModelData(self, editor, model, index):
        """Use a custom delegate setModelData method if it exists"""
        logger.debug('setting model data for column %s' % index.column())
        delegate = self.get_column_delegate(index.column())
        delegate.setModelData(editor, model, index)

    def sizeHint(self, option, index):
        option = QtGui.QStyleOptionViewItem()
        delegate = self.get_column_delegate(index.column())
        return delegate.sizeHint(option, index)