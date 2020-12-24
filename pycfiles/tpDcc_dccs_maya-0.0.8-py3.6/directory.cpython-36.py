# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/dccs/maya/core/directory.py
# Compiled at: 2020-04-24 23:10:50
# Size of source mod 2**32: 1213 bytes
"""
Module that contains functions and classes related with directories and files in Maya
"""
from __future__ import print_function, division, absolute_import
import tpDcc.dccs.maya as maya

def select_file_dialog(title, start_directory=None, pattern=None):
    """
    Shows select file dialog
    :param title: str
    :param start_directory: str
    :param pattern: str
    :return: str
    """
    res = maya.cmds.fileDialog2(fm=1, dir=start_directory, cap=title, ff=pattern)
    if res:
        res = res[0]
    return res


def select_folder_dialog(title, start_directory=None):
    """
    Shows select folder dialog
    :param title: str
    :param start_directory: str
    :return: str
    """
    res = maya.cmds.fileDialog2(fm=3, dir=start_directory, cap=title)
    if res:
        res = res[0]
    return res


def save_file_dialog(title, start_directory=None, pattern=None):
    """
    Shows save file dialog
    :param title: str
    :param start_directory: str
    :param pattern: str
    :return: str
    """
    res = maya.cmds.fileDialog2(fm=0, dir=start_directory, cap=title, ff=pattern)
    if res:
        res = res[0]
    return res