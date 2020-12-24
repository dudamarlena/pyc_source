# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\christian\documents\github\arduino_helpers\arduino_helpers\hardware\teensy\pdb.py
# Compiled at: 2015-11-11 17:04:24
import numpy as np, pandas as pd
PDB_SC_CONT = 2
PDB_SC_DMAEN = 32768
PDB_SC_LDOK = 1
PDB_SC_PDBEIE = 131072
PDB_SC_PDBEN = 128
PDB_SC_PDBIE = 32
PDB_SC_PDBIF = 64
PDB_SC_SWTRIG = 65536
PDB0_IDLY = 1073963020
PDB0_MOD = 1073963012
PDB0_SC = 1073963008

def PDB_SC_TRGSEL(n):
    return (n & 15) << 8


def PDB_SC_PRESCALER(n):
    return (n & 7) << 12


def PDB_SC_MULT(n):
    return (n & 3) << 2


def PDB_SC_LDMOD(n):
    return (n & 3) << 18


def get_pdb_divide_params(frequency, F_BUS=int(48000000.0)):
    mult_factor = np.array([1, 10, 20, 40])
    prescaler = np.arange(8)
    clock_divide = pd.DataFrame([ [i, m, p, m * (1 << p)] for i, m in enumerate(mult_factor) for p in prescaler
                                ], columns=[
     'mult_', 'mult_factor',
     'prescaler', 'combined']).drop_duplicates(subset=[
     'combined']).sort_values('combined', ascending=True)
    clock_divide['clock_mod'] = (F_BUS / frequency / clock_divide.combined).astype(int)
    return clock_divide.loc[(clock_divide.clock_mod <= 65535)]