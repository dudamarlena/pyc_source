# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/garrigaf/Documents/git/darfix/build/lib/darfix/__init__.py
# Compiled at: 2020-03-03 08:28:12
# Size of source mod 2**32: 1824 bytes
"""The darfix package contains the following main sub-packages:

- silx.core: Core classes and functions
- silx.gui: Qt widgets for data visualization and data file browsing
- silx.image: Some processing functions for 2D images
- silx.io: Functions for input/output operations
- silx.utils: Miscellaneous convenient functions
"""
__authors__ = [
 'J. Garriga']
__license__ = 'MIT'
__date__ = '16/12/2019'
from ._config import Config as _Config
config = _Config()