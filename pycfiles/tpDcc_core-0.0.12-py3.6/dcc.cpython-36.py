# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/standalone/core/dcc.py
# Compiled at: 2020-05-13 19:27:59
# Size of source mod 2**32: 3104 bytes
"""
Module that contains DCC functionality for standalone applications
"""
from __future__ import print_function, division, absolute_import
import tpDcc
from tpDcc import register
from tpDcc.abstract import dcc as abstract_dcc
from Qt.QtCore import *
from Qt.QtWidgets import *

class StandaloneDcc(abstract_dcc.AbstractDCC, object):

    @staticmethod
    def get_name():
        """
        Returns the name of the DCC
        :return: str
        """
        return tpDcc.Dccs.Standalone

    @staticmethod
    def get_extensions():
        """
        Returns supported extensions of the DCC
        :return: list(str)
        """
        return []

    @staticmethod
    def get_dpi(value=1):
        """
        Returns current DPI used by DCC
        :param value: float
        :return: float
        """
        return 1.0

    @staticmethod
    def get_dpi_scale(value):
        """
        Returns current DPI scale used by DCC
        :return: float
        """
        return 1.0

    @staticmethod
    def get_version():
        """
        Returns version of the DCC
        :return: int
        """
        return 0

    @staticmethod
    def get_version_name():
        """
        Returns version of the DCC
        :return: str
        """
        return '0.0.0'

    @staticmethod
    def is_batch():
        """
        Returns whether DCC is being executed in batch mode or not
        :return: bool
        """
        return False

    @staticmethod
    def enable_component_selection():
        """
        Enables DCC component selection mode
        """
        pass

    @staticmethod
    def get_main_window():
        """
        Returns Qt object that references to the main DCC window
        :return:
        """
        pass

    @staticmethod
    def get_main_menubar():
        """
        Returns Qt object that references to the main DCC menubar
        :return:
        """
        pass

    @staticmethod
    def confirm_dialog(title, message, button=None, cancel_button=None, default_button=None, dismiss_string=None):
        """
        Shows DCC confirm dialog
        :param title:
        :param message:
        :param button:
        :param cancel_button:
        :param default_button:
        :param dismiss_string:
        :return:
        """
        from tpDcc.libs.qt.widgets import messagebox
        buttons = button or QDialogButtonBox.Yes | QDialogButtonBox.No
        if cancel_button:
            buttons = buttons | QDialogButtonBox.Cancel
        return messagebox.MessageBox.question(None, title=title, text=message, buttons=buttons)

    @staticmethod
    def warning(message):
        """
        Prints a warning message
        :param message: str
        :return:
        """
        print('WARNING: {}'.format(message))

    @staticmethod
    def error(message):
        """
        Prints a error message
        :param message: str
        :return:
        """
        print('ERROR: {}'.format(message))


register.register_class('Dcc', StandaloneDcc)