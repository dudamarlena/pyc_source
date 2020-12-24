# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patri/MODPIN/modpin/./src/SBI/structure/atom/AtomOfAminoAcid.py
# Compiled at: 2020-04-28 10:16:58
"""
AminoAtom

author: jbonet
date:   02/2013

@oliva's lab
"""
from . import Atom

class AtomOfAminoAcid(Atom):
    """
    An {AtomOfAminoAcid} is simply a point in space defined by 3 coordinates
    WITH specific functions for atoms in amino acids
    """
    backbone_atoms = set(['N', 'CA', 'C'])

    @property
    def is_Calpha(self):
        return self._name == 'CA'

    @property
    def is_Cbeta(self):
        return self._name == 'CB'

    @property
    def is_N(self):
        return self._name == 'N'

    @property
    def is_C(self):
        return self._name == 'C'

    @property
    def is_O(self):
        return self._name == 'O'