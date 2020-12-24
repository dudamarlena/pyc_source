# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyinstruments\curvefinder\gui\curve_display_widget\curve_alter_widget.py
# Compiled at: 2013-12-16 17:26:28
from pyinstruments.curvestore.curve_create_widget import CurveCreateWidget
from pyinstruments.curvestore import models
from pyinstruments.curvefinder.gui.curve_display_widget.id_display_widget import IdDisplayWidget
from pyinstruments.curvestore.tag_widget import TAG_MODEL
import os
from PyQt4 import QtCore, QtGui

class CurveAlterWidget(CurveCreateWidget):
    curve_saved = QtCore.pyqtSignal()
    delete_done = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(CurveAlterWidget, self).__init__(parent=parent)
        self.curve_modified.connect(self.save_button.show)
        self.save_button.clicked.connect(self.save_button.hide)
        self.save_button.clicked.connect(self.save)
        self.current_curve = None
        self.delete_button = QtGui.QPushButton('delete')
        self.delete_button.clicked.connect(self.delete)
        self.lay3.addWidget(self.delete_button)
        return

    def delete(self, dummy=False, confirm=True):
        if self.current_curve == None:
            return
        else:
            if confirm:
                message_box = QtGui.QMessageBox(self)
                answer = message_box.question(self, 'delete', 'are you sure you want to delete curve id =' + str(self.current_curve.id) + ' ?', 'No', 'Yes')
                if not answer:
                    return
            self.current_curve.delete()
            self.delete_done.emit()
            return

    def save(self):
        if self.current_curve != None:
            self.save_curve(self.current_curve)
            self.curve_saved.emit()
        return

    def display_curve(self, curve):
        self.current_curve = curve
        self.dump_in_gui(curve)