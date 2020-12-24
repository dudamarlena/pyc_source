# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyinstruments\curvestore\tag_edit_list_widget.py
# Compiled at: 2013-12-15 10:53:54
from pyinstruments.curvestore.tag_widget import TAG_MODEL
from pyinstruments.curvestore import models
import os
from PyQt4 import QtCore, QtGui

class TagCompleter(QtGui.QCompleter):

    def __init__(self):
        super(TagCompleter, self).__init__()
        self.setModel(TAG_MODEL)

    def separator(self):
        return '/'

    def splitPath(self, path):
        return path.split('/')

    def pathFromIndex(self, index):
        strings = []
        strings.append(index.internalPointer().name)
        index = index.parent()
        while index.internalPointer() is not None:
            strings.append(index.internalPointer().name)
            index = index.parent()

        strings.reverse()
        return ('/').join(strings)


TAG_COMPLETER = TagCompleter()

class TagEditListWidget(QtGui.QWidget):
    value_changed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(TagEditListWidget, self).__init__(parent)
        self.lines = []
        self.need_refresh = False
        self.lay = QtGui.QHBoxLayout()
        self.label_tags = QtGui.QLabel('tags:')
        self.lay.addWidget(self.label_tags)
        self.lay.addStretch()
        self.current = ButtonLineEdit(self)
        self.lay.addWidget(self.current)
        self.setLayout(self.lay)
        self.current.validated.connect(self.add_line)
        self.setMinimumWidth(250)

    def add_line(self):
        self.current.setReadOnly(True)
        self.current.setStyleSheet('QLineEdit{background: cyan;}')
        self.lines.append(self.current)
        self.current.close_clicked.connect(self.current.remove)
        self.current = ButtonLineEdit(self)
        self.current.validated.connect(self.add_line)
        self.lay.addWidget(self.current)

    def clear(self):
        while True:
            try:
                button = self.lines.pop()
            except IndexError:
                return

            button.hide()
            button.deleteLater()

    def get_tags(self):
        return [ str(button.text()) for button in self.lines ]

    def set_tags(self, val):
        self.clear()
        for tag in val:
            self.current.setText(tag)
            self.add_line()


class ButtonLineEdit(QtGui.QLineEdit):
    close_clicked = QtCore.pyqtSignal(bool)
    validated = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(ButtonLineEdit, self).__init__(parent)
        self.button = QtGui.QToolButton(self)
        icon_file = os.path.join(os.path.split(os.path.split(__file__)[0])[0], 'icons', 'close.png')
        self.button.setIcon(QtGui.QIcon(icon_file))
        self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(QtCore.Qt.ArrowCursor)
        self.button.clicked.connect(self.close_clicked.emit)
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        buttonSize = self.button.sizeHint()
        self.setCompleter(TAG_COMPLETER)
        self.setStyleSheet('QLineEdit {padding-right: %dpx; }' % (buttonSize.width() + frameWidth + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), buttonSize.width() + frameWidth * 2 + 2), max(self.minimumSizeHint().height(), buttonSize.height() + frameWidth * 2 + 2))
        self.editingFinished.connect(self.validate)

    def focusInEvent(self, event):
        super(ButtonLineEdit, self).focusInEvent(event)
        if self.parent().need_refresh:
            TAG_MODEL.refresh()

    def remove(self):
        self.parent().lines.remove(self)
        self.deleteLater()
        self.parent().value_changed.emit()

    def validate(self):
        if self.isReadOnly():
            return
        if self.text() == '':
            return
        if self.text() in self.parent().get_tags():
            return
        if self.text() in [ tag.name for tag in models.Tag.objects.all() ]:
            self.validated.emit()
            self.parent().value_changed.emit()
        else:
            print 'nein!'

    def resizeEvent(self, event):
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frameWidth - buttonSize.width(), (self.rect().bottom() - buttonSize.height() + 1) / 2)
        super(ButtonLineEdit, self).resizeEvent(event)