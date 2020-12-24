# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/__init__.py
# Compiled at: 2020-01-29 10:36:02
# Size of source mod 2**32: 894 bytes
"""
The Spike Package

"""
from __future__ import print_function
from .NPKError import NPKError
from .version import version as __version__
from .version import VersionName as __version_info__
from .version import ProgramName as __program_name__
from .version import rev_date as __date__
__author__ = 'Marc A. Delsuc <delsuc@igbmc.fr>'
SPIKE_version = __version__
from . import NPKData
from .plugins import load
load(debug=False)
name = 'SPIKE'