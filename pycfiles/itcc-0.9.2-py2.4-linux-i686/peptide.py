# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/ccs2/peptide.py
# Compiled at: 2008-04-20 13:19:45
"""custom function of peptide
"""
from itcc.ccs2 import base
__revision__ = '$Rev$'
__all__ = ['Peptide']

class Peptide(base.Base):
    __module__ = __name__

    def __init__(self, mol):
        base.Base.__init__(self, mol)
        self.mol = mol

    def getr6s(self, loopatoms, is_chain=False):
        types = gettypes(self.mol, loopatoms)
        if not is_chain:
            if ispair(types[(-1)], types[0]):
                types = types[1:] + types[:1]
                loopatoms = loopatoms[1:] + loopatoms[:1]
            idx = 0
            newloopatoms = []
            while idx < len(loopatoms) - 1:
                type1 = types[idx]
                type2 = types[(idx + 1)]
                if ispair(type1, type2):
                    newloopatoms.append((loopatoms[idx], loopatoms[(idx + 1)]))
                    idx += 2
                else:
                    newloopatoms.append((loopatoms[idx],))
                    idx += 1

            if idx == len(loopatoms) - 1:
                newloopatoms.append((loopatoms[(-1)],))
            else:
                assert idx == len(loopatoms)
            doubleloop = is_chain or newloopatoms * 2
            for i in range(len(newloopatoms)):
                yield tuple(doubleloop[i:i + 7])

        for i in range(len(newloopatoms) - 6):
            yield tuple(newloopatoms[i:i + 7])


def gettypes(mol, idxs):
    result = []
    for idx in idxs:
        result.append(mol.atoms[idx].atomchr() + str(degree(mol, idx)))

    return result


def degree(mol, idx):
    return sum(mol.connect[idx])


def ispair(type1, type2):
    return (
     type1, type2) in [('C3', 'N3'), ('N3', 'C3')]