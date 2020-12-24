# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bin/tester_2mols.py
# Compiled at: 2013-11-13 13:27:04
from nams import nams
ms = nams.Nams()
mol_t1 = ('smi', 'CCC(=O)C(c1ccccc1)c2ccccc2')
mol_t2 = ('smi', 'O=C(CC)N(c1ccncc1)c3ccccc3')
(mol1, mol_info1) = ms.get_mol_info(mol_t1[0], mol_t1[1])
(mol2, mol_info2) = ms.get_mol_info(mol_t2[0], mol_t2[1])
(sim11, d_atoms) = ms.get_similarity(mol_info1, mol_info1)
(sim22, d_atoms) = ms.get_similarity(mol_info2, mol_info2)
(sim12, d_atoms) = ms.get_similarity(mol_info1, mol_info2)
print 'Self similarity 1: %6.2f' % sim11
print 'Self similarity 2: %6.2f' % sim22
print 'Total similarity: %6.2f -> Jaccard: %6.3f' % (sim12, sim12 / (sim11 + sim22 - sim12))
ks = d_atoms.keys()
ks.sort()
for k in ks:
    print '\t%5d (%3s)  -%3d  (%3s) --> %6.2f' % (k[0], mol1.atoms[(k[0] - 1)].OBAtom.GetType(), k[1], mol2.atoms[(k[1] - 1)].OBAtom.GetType(), d_atoms[k])