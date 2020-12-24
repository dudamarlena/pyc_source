# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bin/tester_nams.py
# Compiled at: 2013-11-13 21:37:07
from nams import nams
import os, openbabel, pybel
data_path = os.path.join(os.path.dirname(nams.__file__), 'data')

def test_list(mfile, mtype, ms, hs, nelems_m):
    import time
    fil = open(mfile, 'rt')
    file_name1 = 'sim_matrix_nelems=' + str(nelems_m) + '_' + str(ms.BS_ALPHA) + '_aring=' + str(ms.ANRINGS_FAC) + '_chir=' + str(ms.ACHIR_FAC) + '_dbstereo=' + str(ms.DBSTEREO_FAC) + '_bring=' + str(ms.BRING_FAC) + '_barom=' + str(ms.BAROM_FAC) + '_border=' + str(ms.BORDER_FAC) + '_pen=' + str(ms.PEN) + '_H=' + str(hs) + '.txt'
    fout = open(file_name1, 'wt')
    file_name2 = 'tanimoto_matrix_nelems=' + str(nelems_m) + '_' + str(ms.BS_ALPHA) + '_aring=' + str(ms.ANRINGS_FAC) + '_chir=' + str(ms.ACHIR_FAC) + '_dbstereo=' + str(ms.DBSTEREO_FAC) + '_bring=' + str(ms.BRING_FAC) + '_barom=' + str(ms.BAROM_FAC) + '_border=' + str(ms.BORDER_FAC) + '_pen=' + str(ms.PEN) + '_H=' + str(hs) + '.txt'
    fout_t = open(file_name2, 'wt')
    lins = fil.readlines()
    fil.close()
    molecs = []
    print 'reading and processing data'
    count = 1
    t1 = time.time()
    tinit = t1
    for lin in lins[0:]:
        (molf, mol_id) = lin.split('\t')
        mol_id = mol_id.strip()
        if pybel.readstring(mtype, molf):
            mol = pybel.readstring(mtype, molf)
            if hs == True:
                mol.addh()
            natoms = len(mol.atoms)
            can_smi = mol.write('can')
            print '\t', count, mol_id, can_smi.strip()
            if natoms > 2:
                (mol1, mol_info) = ms.get_mol_info('can', can_smi, hs)
                molecs.append((mol_id, mol1, mol_info))
                count += 1
            else:
                print 'Warning: NAMS cannot be applied to molecules with less than 3 atoms (including hydrogen atoms). I am skipping this molecule....'
        else:
            print 'Warning: invalid molecule, input format or correspondence between the molecule and input format.. I am skipping this molecule....'

    t2 = time.time()
    print 'TIME SPENT', t2 - tinit
    t1 = t2
    dmat = {}
    print 'write headers and calc self_similarities'
    s = '      '
    i = 1
    tinit = t2
    for m in range(len(molecs)):
        s += '%s ' % molecs[m][0]
        (sim, d_atoms) = ms.get_similarity(molecs[m][2], molecs[m][2], False)
        t2 = time.time()
        print '\t%5s %8.3f %8.3f %8.3f' % (molecs[m][0], sim, t2 - t1, (t2 - tinit) / i)
        t1 = t2
        dmat[(m, m)] = sim
        i += 1

    s += '\n'
    t = s
    print 'calc similarities...'
    tinit = t2
    i = 1
    for m1 in range(1, len(molecs)):
        for m2 in range(m1):
            (sim12, d_atoms) = ms.get_similarity(molecs[m1][2], molecs[m2][2], False)
            dmat[(m1, m2)] = sim12
            dmat[(m2, m1)] = sim12
            i += 1

        t2 = time.time()
        print '\t%5s %8.3f %8.3f %8.3f' % (molecs[m1][0], sim, t2 - t1, (t2 - tinit) / i)
        t1 = t2

    print 'TIME SPENT', t2 - tinit
    print 'WRITING FILE'
    fout.write(s)
    fout_t.write(t)
    for m1 in range(len(molecs)):
        s = '%-s' % molecs[m1][0]
        t = '%-s' % molecs[m1][0]
        for m2 in range(len(molecs)):
            tanimoto = dmat[(m1, m2)] / (dmat[(m1, m1)] + dmat[(m2, m2)] - dmat[(m1, m2)])
            s += '%7.3f' % dmat[(m1, m2)]
            t += '%7.3f' % tanimoto

        s += '\n'
        t += '\n'
        fout.write(s)
        fout_t.write(t)

    fout.close()
    fout_t.close()
    print 'DONE!'


ms = nams.Nams()
ms.BS_ALPHA = 2.0
ms.ANRINGS_FAC = 0.8
ms.ACHIR_FAC = 0.95
ms.DBSTEREO_FAC = 0.95
ms.BRING_FAC = 0.9
ms.BAROM_FAC = 0.9
ms.BORDER_FAC = 0.8
ms.PEN = -0.2
nelems_m = 3
ms.set_elems_dists(nelems_m)
ms.set_bond_assigner('HEURISTIC')
h_experimental = True
mfile = os.path.join(data_path, 'HC_100.smi')
mtype = 'smi'
test_list(mfile, mtype, ms, h_experimental, nelems_m)