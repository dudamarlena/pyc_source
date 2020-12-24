# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/launcher/plugins/dccselector/dccs/nukedcc.py
# Compiled at: 2020-03-13 14:28:25
# Size of source mod 2**32: 1496 bytes
"""
Module that contains functions to handle Nuke functionality
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import os, platform
DEFAULT_DCC = 'nuke.exe'

def get_executables_from_installation_path(installation_path):
    """
    Returns Nuke executable from its installation path
    :param installation_path: str
    """
    if os.path.exists(installation_path):
        nuke_files = os.listdir(installation_path)
        houdini_ex = os.path.basename(installation_path).split('v')[0] + '.exe'
        if houdini_ex in nuke_files:
            return os.path.join(installation_path, houdini_ex)


def get_installation_paths(nuke_versions):
    """
    Returns the installation folder of Nuke
    :param nuke_versions: list(str)
    :return:
    """
    versions = dict()
    if platform.system().lower() == 'windows':
        for nuke_version in nuke_versions:
            nuke_path = 'C://Program Files//Nuke{}'.format(nuke_version)
            if not os.path.exists(nuke_path):
                continue
            nuke_executable = get_executables_from_installation_path(nuke_path)
            if not nuke_executable is None:
                if not os.path.isfile(nuke_executable):
                    pass
                else:
                    versions['{}'.format(nuke_version)] = nuke_executable

    return versions