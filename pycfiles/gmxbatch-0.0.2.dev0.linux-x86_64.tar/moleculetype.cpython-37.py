# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/moleculetype/moleculetype.py
# Compiled at: 2020-03-26 06:19:25
# Size of source mod 2**32: 3474 bytes
import copy
from typing import List
from .atom import Atom

class MoleculeType:
    itpfile: str
    count: int
    posresdefine: str
    atoms: List[Atom]
    name: str
    kind = 'Solute'
    kind: str

    def __init__(self, name: str, itpfile: str, count: int=1, posresdefine: str='', kind='Solute'):
        self.itpfile = itpfile
        self.name = name
        self.count = count
        self.posresdefine = posresdefine
        self.kind = kind
        self.atoms = []

    @classmethod
    def loadITP(cls, itpfile: str, kind: str='Solute'):
        """Generator function for loading molecule types from an ITP file.

        :param itpfile: itp file name
        :type itpfile: str
        :param kind: molecule kind: Solvent, Solute, Ion
        :type kind: str
        """
        with open(itpfile, 'rt') as (f):
            obj = None
            section = None
            for line in f:
                l = line.split(';', 1)[0].strip()
                if not l:
                    continue
                elif l.startswith('#ifdef'):
                    deflabel = l.split()[1]
                    if 'POSR' in deflabel.upper():
                        obj.posresdefine = deflabel
                elif l.startswith('#'):
                    continue
                elif l.startswith('[') and l.endswith(']'):
                    section = l[1:-1].strip()
                    if section == 'moleculetype':
                        if obj is not None:
                            obj.classify()
                            yield obj
                        obj = cls(name='', itpfile=itpfile,
                          count=0,
                          posresdefine='',
                          kind=kind)
                elif section == 'atoms':
                    obj.atoms.append(Atom.fromITPLine(l))
                elif section == 'moleculetype':
                    obj.name = l.split()[0]

            if obj is not None:
                obj.classify()
                yield obj

    def __deepcopy__(self, memodict={}) -> 'MoleculeType':
        """Deep copy operation"""
        mt = MoleculeType(self.name, self.itpfile, self.count, self.posresdefine, self.kind)
        mt.atoms = [copy.deepcopy(a) for a in self.atoms]
        return mt

    def classify(self):
        """Very crude heuristics to classify molecule types into Solute, Solvent, Ion categories"""
        if self.name.upper() in ('LI', 'NA', 'K', 'CS', 'CL', 'CA', 'MG', 'ZN') or self.itpfile.endswith('ions.itp'):
            self.kind = 'Ion'
        else:
            if self.name.upper() in ('HOH', 'TIP3', 'SOL', 'MEOH', 'OCOH', 'DMSO',
                                     'TP3', 'H2O'):
                self.kind = 'Solvent'
        print('Classified {} to {} (atoms: {})'.format(self.name, self.kind, len(self.atoms)))

    def __str__(self):
        return f"MoleculeType: {self.name}\n" + f"   kind: {self.kind}\n" + f"   count: {self.count}\n" + f"   itp: {self.itpfile}\n" + f"   atoms: {len(self.atoms)}\n" + f"   posres macro: {self.posresdefine}"