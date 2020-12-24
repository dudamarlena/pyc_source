# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\keurf\Documents\GitHub\Pycker\pycker\__init__.py
# Compiled at: 2017-10-13 05:16:08
# Size of source mod 2**32: 477 bytes
"""
Pycker provides user-friendly routines to visualize seismic traces and pick
first break arrival times.

Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""
from .pick import Pick
from .quantity_error import QuantityError
from .wiggle import wiggle
from .read_stream import StreamReader
from .gui import PyckerGUI
__version__ = '1.1.1'
__all__ = ['Pick', 'QuantityError', 'wiggle', 'StreamReader', 'PyckerGUI']