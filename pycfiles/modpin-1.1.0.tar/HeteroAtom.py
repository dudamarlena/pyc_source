# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patricia/patricia/modppi/./src/SBI/structure/header/HeteroAtom.py
# Compiled at: 2018-02-02 06:38:51
from .MiniRes import MiniResidue
from SBI.beans.JSONer import JSONer

class Hetero(MiniResidue, JSONer):
    """
    {Hetero} includes all the data related to a heteroatom in the PDB.
    This does not include modified AminoAcids or Nucleotides in the main chain.
    """

    def __init__(self, restype, position):
        super(Hetero, self).__init__(restype, position)
        self._name = ''
        self._form = ''

    @property
    def name(self):
        return self._name.strip()

    @property
    def formula(self):
        return self._form.strip()

    def add_name(self, line):
        self._name += ' ' + line

    def add_formula(self, line):
        self._form += ' ' + line

    def __hash__(self):
        return hash((self._type, self._chain))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return hash(self) == hash(other)
        raise NotImplemented

    def as_dict(self):
        nobj = {}
        nobj['type'] = self.restype
        nobj['name'] = self.name
        nobj['formula'] = self.formula
        return nobj