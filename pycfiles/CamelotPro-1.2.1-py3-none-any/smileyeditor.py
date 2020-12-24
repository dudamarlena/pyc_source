# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/smileyeditor.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from customeditor import CustomEditor
from camelot.view.art import Icon
default_icon_names = [
 'face-angel',
 'face-crying',
 'face-devilish',
 'face-glasses',
 'face-grin',
 'face-kiss',
 'face-monkey',
 'face-plain',
 'face-sad',
 'face-smile',
 'face-smile-big',
 'face-surprise',
 'face-wink']
default_icons = list((icon_name, Icon('tango/16x16/emotes/%s.png' % icon_name)) for icon_name in default_icon_names)

class SmileyEditor(CustomEditor):

    def __init__(self, parent, editable=True, icons=default_icons, field_name='icons', **kwargs):
        CustomEditor.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self.setObjectName(field_name)
        self.box = QtGui.QComboBox()
        self.box.setFrame(True)
        self.box.setEditable(False)
        self.name_by_position = {0: None}
        self.position_by_name = {None: 0}
        self.box.addItem('')
        for i, (icon_name, icon) in enumerate(icons):
            self.name_by_position[i + 1] = icon_name
            self.position_by_name[icon_name] = i + 1
            self.box.addItem(icon.getQIcon(), '')
            self.box.setFixedHeight(self.get_height())

        self.setFocusPolicy(Qt.StrongFocus)
        layout = QtGui.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setAutoFillBackground(True)
        if not editable:
            self.box.setEnabled(False)
        else:
            self.box.setEnabled(True)
        self.box.activated.connect(self.smiley_changed)
        layout.addWidget(self.box)
        layout.addStretch()
        self.setLayout(layout)
        return

    def get_value(self):
        position = self.box.currentIndex()
        return CustomEditor.get_value(self) or self.name_by_position[position]

    def set_enabled(self, editable=True):
        self.box.setEnabled(editable)

    @QtCore.pyqtSlot(int)
    def smiley_changed(self, _index):
        self.editingFinished.emit()

    def set_value(self, value):
        name = CustomEditor.set_value(self, value)
        self.box.setCurrentIndex(self.position_by_name[name])