# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bin/tester_chirality.py
# Compiled at: 2013-09-24 12:16:05
from nams import chirality
line_notation = 'C([C@@H](C(=O)O)N)S'
input_type = 'smi'
chir = chirality.Chirality(line_notation, input_type)
print chir.can_smi
for atom_id in range(chir.n_atoms):
    print chir.get_chirality(atom_id)