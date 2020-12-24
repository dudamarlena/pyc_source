# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bin/tester_doubleb_e_z.py
# Compiled at: 2013-09-24 12:17:10
from nams import doubleb_e_z
line_notation = 'I/C=C/Cl'
input_type = 'smi'
stereo = doubleb_e_z.Stereodoubleb(line_notation, input_type)
print stereo.can_smi
for bond_id in range(stereo.n_bonds):
    print stereo.get_e_z_bond(bond_id)