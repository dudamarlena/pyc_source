# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/qcrash/qcrash/_dialogs/review.py
# Compiled at: 2016-12-29 05:40:24
# Size of source mod 2**32: 2079 bytes
"""
This module contains the review dialog.
"""
from qcrash.qt import QtCore, QtGui, QtWidgets
from qcrash._forms import dlg_review_ui

class DlgReview(QtWidgets.QDialog):
    __doc__ = '\n    Dialog for reviewing the final report.\n    '

    def __init__(self, content, log, parent, window_icon):
        """
        :param content: content of the final report, before review
        :param parent: parent widget
        """
        super(DlgReview, self).__init__(parent)
        self.ui = dlg_review_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.edit_main.setPlainText(content)
        self.ui.edit_main.installEventFilter(self)
        self.ui.edit_log.installEventFilter(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(QtGui.QIcon.fromTheme('document-edit') if window_icon is None else window_icon)
        if log:
            self.ui.edit_log.setPlainText(log)
        else:
            self.ui.tabWidget.tabBar().hide()
        self.ui.edit_main.setFocus()

    def eventFilter(self, obj, event):
        interesting_objects = [
         self.ui.edit_log, self.ui.edit_main]
        if obj in interesting_objects and event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Return and event.modifiers() & QtCore.Qt.ControlModifier:
            self.accept()
            return True
        return False

    @classmethod
    def review(cls, content, log, parent, window_icon):
        """
        Reviews the final bug report.

        :param content: content of the final report, before review
        :param parent: parent widget

        :returns: the reviewed report content or None if the review was
                  canceled.
        """
        dlg = DlgReview(content, log, parent, window_icon)
        if dlg.exec_():
            return (dlg.ui.edit_main.toPlainText(),
             dlg.ui.edit_log.toPlainText())
        return (None, None)