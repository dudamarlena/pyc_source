# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpQtLib/widgets/messagehandler.py
# Compiled at: 2020-01-16 21:52:29
# Size of source mod 2**32: 2296 bytes
"""
Module that contains classes to show different kind of message boxes
"""
from __future__ import print_function, division, absolute_import
import tpDccLib as tp
from Qt.QtWidgets import *

class MessageHandler(object):

    def __init__(self):
        super(MessageHandler, self).__init__()
        self.parent_window = tp.Dcc.get_main_window()

    def set_message(self, msg, level=0):
        """
        Sets a message in the status bar
        :param msg: str, message to show
        :param level: message level (0=info, 1=warning, 2=error)
        """
        if level < 0:
            level = 0
        if level > 3:
            level = 3

    def show_confirm_dialog(self, msg, title='Title'):
        """
        Shows a yes/no confirmation dialog
        :param msg: str, message to show with the dialog
        :param title: str, title of the dialog
        :return: bool, Whether the user has pressed yes(True) or No(False)
        """
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Question)
        result = dialog.question(self.parent_window, title, msg, QMessageBox.Yes, QMessageBox.No)
        if result == QMessageBox.Yes:
            return True
        else:
            return False

    def show_warning_dialog(self, msg, detail=None):
        """
        Shows a warning dialog
        :param msg: str, message to show with the dialog
        :param detail: str, detail information to show (optional)
        """
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Warning)
        dialog.setWindowTitle('Warning')
        dialog.setText(msg)
        if detail:
            dialog.setDetailedText(detail)
        dialog.exec_()

    def show_info_dialog(self, msg, title='Info'):
        """
        Shows a info dialog
        :param msg: str, message to show with the dialog
        :param title: str, title of the dialog
        """
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Information)
        dialog.setWindowTitle(title)
        dialog.setText(msg)
        dialog.exec_()