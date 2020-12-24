# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patri/MODPIN/modpin/./src/SBI/structure/atom/AtomOfNucleotide.py
# Compiled at: 2020-04-28 10:16:58
"""
NucleotideAtom

author: jbonet
date:   02/2013

@oliva's lab
"""
from . import Atom

class AtomOfNucleotide(Atom):
    """
    An {AtomOfNucleotide} is simply a point in space defined by 3 coordinates
    WITH specific functions for atoms in amino acids
    """
    backbone_atoms = set(['P', 'O1P', 'O2P', 'O3P', "O5'", "C5'", "C4'", "O4'", "C3'", "O3'", "C2'", "O2'", "C1'",
     'OP1', 'OP2', 'OP3', 'O5*', 'C5*', 'C4*', 'O4*', 'C3*', 'O3*', 'C2*', 'O2*', 'C1*'])

    @property
    def is_Phosphate(self):
        return self._name == 'P'

    @property
    def is_SugarOxygen3(self):
        return self._name in set(['O3*', "O3'"])

    @property
    def is_PhosphoOxygen(self):
        return self._name in set(['O1P', 'O2P', 'O3P', 'OP1', 'OP2', 'OP3'])