# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellalauncher/artelladccs/substancepainterdcc.py
# Compiled at: 2019-08-27 13:12:05
# Size of source mod 2**32: 838 bytes
"""
Module that contains functions to handle Substance Painter functionality
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import os, platform
DEFAULT_DCC = 'painter.exe'

def get_executables_from_installation_path(installation_path):
    """
    Returns Substance Painter executable from its installation path
    :param installation_path: str
    """
    pass


def get_installation_paths(painter_versions):
    """
    Returns the installation folder of Substance Painter
    :param painter_versions: list(str)
    :return:
    """
    versions = dict()
    return {'4R8': 'C://Program Files//Pixologic//ZBrush 4R8//ZBrush.exe'}