# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/File/BrukerMS.py
# Compiled at: 2019-04-25 08:10:54
# Size of source mod 2**32: 949 bytes
"""
Utility to import Bruker MS files

A wrapper around Solarix and Apex modules

Created by MAD on 03-2019.

Copyright (c) 2019 IGBMC. All rights reserved.
"""
from ..File import Apex, Solarix

def Import_1D(*arg, **kword):
    """
    Entry point to import 1D spectra
    It returns a FTICRData
    It writes a HDF5 file if an outfile is mentionned
    """
    try:
        return (Solarix.Import_1D)(*arg, **kword)
    except:
        return (Apex.Import_1D)(*arg, **kword)


def Import_2D(*arg, **kword):
    """
    Entry point to import 2D spectra
    It returns a FTICRData
    It writes a HDF5 file if an outfile is mentionned

    compression (compress=True) is efficient, but takes more time.
    """
    try:
        return (Solarix.Import_2D)(*arg, **kword)
    except:
        return (Apex.Import_2D)(*arg, **kword)