# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patricia/patricia/modppi/./src/SBI/structure/protein/Sequencer.py
# Compiled at: 2018-02-02 06:38:51


def _sequencer(pdb, mode):
    seq = ''
    idx = []
    for aa in range(len(pdb.aminoacids)):
        if aa == 0:
            if mode == 'seq':
                seq += pdb.aminoacids[aa].single_letter
            if mode == 'str':
                seq += pdb.aminoacids[aa].secondary_structure
            if mode == 'idx':
                idx.append(pdb.aminoacids[aa].identifier)
        elif pdb.aminoacids[aa].follows(pdb.aminoacids[(aa - 1)]):
            if mode == 'seq':
                seq += pdb.aminoacids[aa].single_letter
            if mode == 'str':
                seq += pdb.aminoacids[aa].secondary_structure
            if mode == 'idx':
                idx.append(pdb.aminoacids[aa].identifier)
        else:
            id_distance = -1 * pdb.aminoacids[aa].identifier_distance(pdb.aminoacids[(aa - 1)])
            if id_distance > 1:
                for x in range(id_distance - 1):
                    if mode == 'idx':
                        idx.append('X')
                    else:
                        seq += 'x'

            elif mode == 'idx':
                idx.append('X')
            else:
                seq += 'x'
            if mode == 'seq':
                seq += pdb.aminoacids[aa].single_letter
            if mode == 'str':
                seq += pdb.aminoacids[aa].secondary_structure
            if mode == 'idx':
                idx.append(pdb.aminoacids[aa].identifier)

    if mode == 'idx':
        return (';').join(idx)
    else:
        return seq