# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cor/bin/src/crystal_torture/crystal_torture/test.py
# Compiled at: 2018-05-26 10:22:35
# Size of source mod 2**32: 371 bytes
from crystal_torture.pymatgen_interface import nodes_from_structure, clusters_from_file
from crystal_torture import Cluster, Node
if __name__ == '__main__':
    cluster = clusters_from_file('tests/POSCAR_2_cluster.vasp', 4.0)