# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/guimetadata.py
# Compiled at: 2019-09-27 22:20:52
# Size of source mod 2**32: 9273 bytes
"""
Metadata constants synopsizing high-level application behaviour.
"""
import sys
NAME = 'BETSEE'
LICENSE = '2-clause BSD'
PYTHON_VERSION_MIN = '3.5.0'
PYTHON_VERSION_MINOR_MAX = 8

def _convert_version_str_to_tuple(version_str: str) -> tuple:
    """
    Convert the passed human-readable ``.``-delimited version string into a
    machine-readable version tuple of corresponding integers.
    """
    assert isinstance(version_str, str), '"{}" not a version string.'.format(version_str)
    return tuple(int(version_part) for version_part in version_str.split('.'))


PYTHON_VERSION_MIN_PARTS = _convert_version_str_to_tuple(PYTHON_VERSION_MIN)
if sys.version_info[:3] < PYTHON_VERSION_MIN_PARTS:
    PYTHON_VERSION = '.'.join(str(version_part) for version_part in sys.version_info[:3])
    raise RuntimeError('{} requires at least Python {}, but the active interpreter is only Python {}. We feel deep sadness for you.'.format(NAME, PYTHON_VERSION_MIN, PYTHON_VERSION))
VERSION = '1.1.1.0'
VERSION_PARTS = _convert_version_str_to_tuple(VERSION)
SYNOPSIS = 'BETSEE, the BioElectric Tissue Simulation Engine Environment.'
DESCRIPTION = 'The BioElectric Tissue Simulation Engine Environment (BETSEE) is the official Qt 5-based graphical user interface (GUI) for BETSE, a finite volume simulator for 2D computational multiphysics problems in the life sciences -- including electrodiffusion, electro-osmosis, galvanotaxis, voltage-gated ion channels, gene regulatory networks, and biochemical reaction networks.'
AUTHORS = 'Alexis Pietak, Cecil Curry, et al.'
AUTHOR_EMAIL = 'leycec@gmail.com'
ORG_NAME = 'Paul Allen Discovery Center'
ORG_DOMAIN_NAME = 'alleninstitute.org'
URL_HOMEPAGE = 'https://gitlab.com/betse/betsee'
URL_DOWNLOAD = '{}/repository/archive.tar.gz?ref=v{}'.format(URL_HOMEPAGE, VERSION)
PACKAGE_NAME = NAME.lower()
MAIN_WINDOW_QRC_MODULE_NAME = PACKAGE_NAME + '_rc'
MAIN_WINDOW_UI_MODULE_NAME = PACKAGE_NAME + '_ui'