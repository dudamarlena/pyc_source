# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/combobox_input_dialog.py
# Compiled at: 2013-04-11 17:47:52
import logging
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QBoxLayout
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QPushButton
logger = logging.getLogger('camelot.view.controls.combobox_input_dialog')

class ComboBoxInputDialog(QDialog):

    def __init__(self, autoaccept=False, parent=None):
        """
        :param autoaccept: if True, the value of the ComboBox is immediately
        accepted after selecting it.
        """
        super(ComboBoxInputDialog, self).__init__(parent)
        self._autoaccept = autoaccept
        layout = QVBoxLayout()
        label = QtGui.QLabel()
        label.setObjectName('label')
        combobox = QtGui.QComboBox()
        combobox.setObjectName('combobox')
        combobox.activated.connect(self._combobox_activated)
        ok_button = QPushButton('OK')
        ok_button.setObjectName('ok')
        cancel_button = QPushButton('Cancel')
        cancel_button.setObjectName('cancel')
        ok_button.pressed.connect(self.accept)
        cancel_button.pressed.connect(self.reject)
        button_layout = QBoxLayout(QBoxLayout.RightToLeft)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(ok_button)
        layout.addWidget(label)
        layout.addWidget(combobox)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    @QtCore.pyqtSlot(int)
    def _combobox_activated(self, index):
        if self._autoaccept:
            self.accept()
        print index

    def set_label_text(self, text):
        label = self.findChild(QtGui.QWidget, 'label')
        if label != None:
            label.setText(text)
        return

    def set_items(self, items):
        combobox = self.findChild(QtGui.QWidget, 'combobox')
        if combobox != None:
            combobox.addItems(items)
        return

    def count(self):
        combobox = self.findChild(QtGui.QWidget, 'combobox')
        if combobox != None:
            return combobox.count()
        else:
            return 0

    def set_data(self, index, data, role):
        combobox = self.findChild(QtGui.QWidget, 'combobox')
        if combobox != None:
            combobox_model = combobox.model()
            model_index = combobox_model.index(index, 0)
            combobox_model.setData(model_index, data, role)
        return

    def get_text(self):
        combobox = self.findChild(QtGui.QWidget, 'combobox')
        if combobox != None:
            return combobox.currentText()
        else:
            return

    def set_ok_button_default(self):
        ok = self.findChild(QtGui.QWidget, 'ok')
        if ok != None:
            ok.setFocus()
        return

    def set_cancel_button_default(self):
        cancel = self.findChild(QtGui.QWidget, 'cancel')
        if cancel != None:
            cancel.setFocus()
        return

    def set_ok_button_text(self, text):
        ok = self.findChild(QtGui.QWidget, 'ok')
        if ok != None:
            ok.setText(text)
        return

    def set_cancel_button_text(self, text):
        cancel = self.findChild(QtGui.QWidget, 'cancel')
        if cancel != None:
            cancel.setText(text)
        return

    def set_window_title(self, title):
        self.setWindowTitle(title)

    def set_choice_by_text(self, text):
        combobox = self.findChild(QtGui.QWidget, 'combobox')
        if combobox != None:
            index = combobox.findText(text)
            self.set_choice_by_index(index)
        return

    def set_choice_by_index(self, index):
        combobox = self.findChild(QtGui.QWidget, 'combobox')
        if combobox != None:
            combobox.setCurrentIndex(index)
        else:
            raise Exception('No combobox to set the choice')
        return