# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/launcher/plugins/dccselector/dccs/photoshopdcc.py
# Compiled at: 2020-03-13 14:28:25
# Size of source mod 2**32: 850 bytes
"""
Module that contains functions to handle Photoshop functionality
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import os, platform
DEFAULT_DCC = 'photoshop.exe'

def get_executables_from_installation_path(installation_path):
    """
    Returns Maya executable from its installation path
    :param installation_path: str
    """
    pass


def get_installation_paths(photoshop_versions):
    """
    Returns the installation paths folder where Photoshop is located in the user computer
    :param photoshop_versions: list(str)
    :return: str
    """
    return {'2018': 'C://Program Files//Adobe//Adobe Photoshop CC 2018//Photoshop.exe'}