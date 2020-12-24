# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fatfrog/Documents/backmap/tests/test_backmap.py
# Compiled at: 2018-04-06 16:47:28
# Size of source mod 2**32: 1653 bytes
from unittest import TestCase
import matplotlib.pyplot as plt, backmap, backmap as bm
__author__ = 'ranjanmannige'
__copyright__ = 'Ranjan Mannige'
__license__ = 'MIT'

def test_ramachandran_number():
    if not backmap.R(180, 180) == 1.0:
        raise AssertionError
    else:
        assert backmap.R(-180, -180) == 0.0
        assert backmap.R(0, 0) == 0.5


def test_load_pdb():
    pdbfn = 'tests/pdbs/1mba.pdb'
    data = bm.read_pdb(pdbfn)
    if not set(data[1:, 0]) == set([1]):
        raise AssertionError
    elif not len(data[1:, 0]) == 146:
        raise AssertionError


def test_plot_graph():
    pdbfn = 'tests/pdbs/1mba.pdb'
    data = bm.read_pdb(pdbfn)
    cmap = 'Chirality'
    grouped_data = bm.group_data_by(data, group_by='chain', columns_to_return=['model', 'resid', 'R'])
    for chain in list(grouped_data.keys()):
        print('\\t', chain)
        models, residues, Rs = grouped_data[chain]
        response = False
        response = bm.draw_xyz(X=models, Y=residues, Z=Rs, xlabel='Frame #',
          ylabel='Residue #',
          zlabel='$\\mathcal{R}$',
          cmap=cmap,
          title=cmap,
          vmin=0,
          vmax=1)
        assert response