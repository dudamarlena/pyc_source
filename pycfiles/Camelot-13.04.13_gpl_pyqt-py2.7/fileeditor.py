# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/fileeditor.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from customeditor import CustomEditor, set_background_color_palette
from camelot.view.art import Icon
from camelot.core.utils import ugettext as _
from camelot.view.controls.decorated_line_edit import DecoratedLineEdit

class FileEditor(CustomEditor):
    """Widget for editing File fields"""
    filter = 'All files (*)'
    add_icon = Icon('tango/16x16/actions/list-add.png')
    open_icon = Icon('tango/16x16/actions/document-open.png')
    clear_icon = Icon('tango/16x16/actions/edit-delete.png')
    save_as_icon = Icon('tango/16x16/actions/document-save-as.png')
    document_pixmap = Icon('tango/16x16/mimetypes/x-office-document.png')

    def __init__(self, parent=None, storage=None, field_name='file', remove_original=False, **kwargs):
        CustomEditor.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self.setObjectName(field_name)
        self.storage = storage
        self.filename = None
        self.value = None
        self.remove_original = remove_original
        self.setup_widget()
        return

    def setup_widget(self):
        """Called inside init, overwrite this method for custom
        file edit widgets"""
        self.layout = QtGui.QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.save_as_button = QtGui.QToolButton()
        self.save_as_button.setFocusPolicy(Qt.ClickFocus)
        self.save_as_button.setIcon(self.save_as_icon.getQIcon())
        self.save_as_button.setToolTip(_('Save file as'))
        self.save_as_button.setAutoRaise(True)
        self.save_as_button.clicked.connect(self.save_as_button_clicked)
        self.clear_button = QtGui.QToolButton()
        self.clear_button.setFocusPolicy(Qt.ClickFocus)
        self.clear_button.setIcon(self.clear_icon.getQIcon())
        self.clear_button.setToolTip(_('Delete file'))
        self.clear_button.setAutoRaise(True)
        self.clear_button.clicked.connect(self.clear_button_clicked)
        self.open_button = QtGui.QToolButton()
        self.open_button.setFocusPolicy(Qt.ClickFocus)
        self.open_button.setIcon(self.open_icon.getQIcon())
        self.open_button.setToolTip(_('Open file'))
        self.open_button.clicked.connect(self.open_button_clicked)
        self.open_button.setAutoRaise(True)
        self.add_button = QtGui.QToolButton()
        self.add_button.setFocusPolicy(Qt.StrongFocus)
        self.add_button.setIcon(self.add_icon.getQIcon())
        self.add_button.setToolTip(_('Attach file'))
        self.add_button.clicked.connect(self.add_button_clicked)
        self.add_button.setAutoRaise(True)
        self.filename = DecoratedLineEdit(self)
        self.filename.set_minimum_width(20)
        self.filename.setFocusPolicy(Qt.ClickFocus)
        self.document_label = QtGui.QLabel(self)
        self.document_label.setPixmap(self.document_pixmap.getQPixmap())
        self.layout.addWidget(self.document_label)
        self.layout.addWidget(self.filename)
        self.layout.addWidget(self.clear_button)
        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.save_as_button)
        self.setLayout(self.layout)

    def file_completion_activated(self, index):
        from camelot.view.storage import create_stored_file
        source_index = index.model().mapToSource(index)
        if not self.completions_model.isDir(source_index):
            path = self.completions_model.filePath(source_index)
            create_stored_file(self, self.storage, self.stored_file_ready, filter=self.filter, remove_original=self.remove_original, filename=path)

    def set_value(self, value):
        value = CustomEditor.set_value(self, value)
        self.value = value
        if value:
            self.clear_button.setVisible(True)
            self.save_as_button.setVisible(True)
            self.open_button.setVisible(True)
            self.add_button.setVisible(False)
            self.filename.setText(value.verbose_name)
        else:
            self.clear_button.setVisible(False)
            self.save_as_button.setVisible(False)
            self.open_button.setVisible(False)
            self.add_button.setVisible(True)
            self.filename.setText('')
        return value

    def get_value(self):
        return CustomEditor.get_value(self) or self.value

    def set_field_attributes(self, editable=True, background_color=None, tooltip=None, remove_original=False, **kwargs):
        self.set_enabled(editable)
        if self.filename:
            set_background_color_palette(self.filename, background_color)
            self.filename.setToolTip(unicode(tooltip or ''))
        self.remove_original = remove_original

    def set_enabled(self, editable=True):
        self.clear_button.setEnabled(editable)
        self.add_button.setEnabled(editable)
        self.filename.setEnabled(editable)
        self.filename.setReadOnly(not editable)
        self.document_label.setEnabled(editable)
        self.setAcceptDrops(editable)

    def stored_file_ready(self, stored_file):
        """Slot to be called when a new stored_file has been created by
        the storage"""
        self.set_value(stored_file)
        self.editingFinished.emit()

    def save_as_button_clicked(self):
        from camelot.view.storage import save_stored_file
        value = self.get_value()
        if value:
            save_stored_file(self, value)

    def add_button_clicked(self):
        from camelot.view.storage import create_stored_file
        create_stored_file(self, self.storage, self.stored_file_ready, filter=self.filter, remove_original=self.remove_original)

    def open_button_clicked(self):
        from camelot.view.storage import open_stored_file
        open_stored_file(self, self.value)

    def clear_button_clicked(self):
        answer = QtGui.QMessageBox.question(self, _('Remove this file ?'), _('If you continue, you will no longer be able to open this file.'), QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if answer == QtGui.QMessageBox.Yes:
            self.value = None
            self.editingFinished.emit()
        return

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        from camelot.view.storage import create_stored_file
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            filename = url.toLocalFile()
            if filename:
                create_stored_file(self, self.storage, self.stored_file_ready, filter=self.filter, remove_original=self.remove_original, filename=filename)