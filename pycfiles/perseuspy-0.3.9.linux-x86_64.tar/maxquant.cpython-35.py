# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/perseuspy/io/maxquant.py
# Compiled at: 2019-11-19 08:16:09
# Size of source mod 2**32: 895 bytes
"""
utility functions for parsing various generic output tables
of MaxQuant/Perseus
"""
import pandas as pd
from os import path

def read_rawFilesTable(filename):
    """parse the 'rawFilesTable.txt' file into a pandas dataframe"""
    exp = pd.read_table(filename)
    expected_columns = {'File', 'Exists', 'Size', 'Data format', 'Parameter group', 'Experiment', 'Fraction'}
    found_columns = set(exp.columns)
    if len(expected_columns - found_columns) > 0:
        message = '\n'.join(['The raw files table has the wrong format!',
         'It should contain columns:',
         ', '.join(sorted(expected_columns)),
         'Found columns:',
         ', '.join(sorted(found_columns))])
        raise ValueError(message)
    exp['Raw file'] = exp['File'].apply(path.basename).apply(path.splitext).str.get(0)
    exp['Experiment'] = exp['Experiment'].astype(str)
    return exp