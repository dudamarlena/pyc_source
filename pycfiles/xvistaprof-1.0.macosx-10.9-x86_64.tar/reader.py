# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jsick/.virtualenvs/andromass/lib/python2.7/site-packages/xvistaprof/reader.py
# Compiled at: 2014-06-03 11:17:25
"""
Reader for XVISTA .prof tables.
"""
import numpy as np
from astropy.table import Table
from astropy.io import registry

def xvista_table_reader(filename):
    dt = [
     (
      'R', np.float), ('SB', np.float), ('SB_err', np.float),
     (
      'ELL', np.float), ('PA', np.float), ('EMAG', np.float),
     (
      'ELLMAG', np.float), ('ELLMAG_err', np.float), ('XC', np.float),
     (
      'YC', np.float), ('FRACONT', np.float), ('A1', np.float),
     (
      'A2', np.float), ('A4', np.float), ('CIRCMAG', np.float)]
    data = np.loadtxt(filename, dtype=np.dtype(dt), skiprows=15)
    return Table(data)


registry.register_reader('xvistaprof', Table, xvista_table_reader)