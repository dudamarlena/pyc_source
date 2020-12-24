# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cw12401/code/work/ampal/src/ampal/data.py
# Compiled at: 2018-04-11 08:16:26
# Size of source mod 2**32: 718 bytes
"""Loads data required for running ISAMBARD."""
import json, pathlib
AA_PATH = pathlib.Path(__file__).parent / 'datafiles' / 'amino_acids.json'
CE_PATH = pathlib.Path(__file__).parent / 'datafiles' / 'chemical_elements.json'
COL_PATH = pathlib.Path(__file__).parent / 'datafiles' / 'pdb_atom_column_format.json'
REF_PATH = pathlib.Path(__file__).parent / 'datafiles' / 'non_canonical_amino_acids'
with open(str(CE_PATH), 'r') as (inf):
    ELEMENT_DATA = json.loads(inf.read())
with open(str(COL_PATH), 'r') as (inf):
    PDB_ATOM_COLUMNS = json.loads(inf.read())
with open(str(AA_PATH), 'r') as (inf):
    AMINO_ACIDS_DATA = json.loads(inf.read())
__author__ = 'Christopher W. Wood'