# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cor/bin/src/crystal_torture/crystal_torture/test.py
# Compiled at: 2018-05-26 10:22:35
# Size of source mod 2**32: 371 bytes
from crystal_torture.pymatgen_interface import nodes_from_structure, clusters_from_file
from crystal_torture import Cluster, Node
if __name__ == '__main__':
    cluster = clusters_from_file('tests/POSCAR_2_cluster.vasp', 4.0)