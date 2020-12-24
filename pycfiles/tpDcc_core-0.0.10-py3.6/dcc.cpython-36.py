# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/core/dcc.py
# Compiled at: 2020-04-24 23:10:11
# Size of source mod 2**32: 1858 bytes
"""
Module that contains DCC functionality for non DCC based environemnts
"""
from __future__ import print_function, division, absolute_import
import tpDcc
from tpDcc.abstract import dcc as abstract_dcc

class UnknownDCC(abstract_dcc.AbstractDCC, object):

    @staticmethod
    def get_name():
        """
        Returns the name of the DCC
        :return: str
        """
        return tpDcc.Dccs.Unknown

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
        :param value: float
        :return: float
        """
        return 1.0 * value

    @staticmethod
    def get_version():
        """
        Returns version of the DCC
        :return: int
        """
        return -1

    @staticmethod
    def get_version_name():
        """
        Returns version of the DCC
        :return: int
        """
        return ''

    @staticmethod
    def is_batch():
        """
        Returns whether DCC is being executed in batch mode or not
        :return: bool
        """
        return False

    @staticmethod
    def get_main_window():
        """
        Returns Qt object that references to the main DCC window
        :return:
        """
        pass

    @staticmethod
    def warning(message):
        """
        Prints a warning message
        :param message: str
        :return:
        """
        print('[WARNING]: {}'.format(message))

    @staticmethod
    def error(message):
        """
        Prints a error message
        :param message: str
        :return:
        """
        print('[ERROR]: {}'.format(message))