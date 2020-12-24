# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cw12401/code/work/ampal/src/ampal/ligands.py
# Compiled at: 2018-04-11 08:04:54
# Size of source mod 2**32: 3443 bytes
__doc__ = 'AMPAL objects that represent ligands.'
from ampal.base_ampal import Polymer, Monomer

class LigandGroup(Polymer):
    """LigandGroup"""

    def __init__(self, monomers=None, polymer_id=' ', parent=None, sl=2):
        super().__init__(monomers=monomers,
          polymer_id=polymer_id,
          molecule_type='ligands',
          parent=parent,
          sl=sl)

    def __repr__(self):
        return '<Ligands chain containing {} {}>'.format(len(self._monomers), 'Ligand' if len(self._monomers) == 1 else 'Ligands')


class Ligand(Monomer):
    """Ligand"""

    def __init__(self, mol_code, atoms=None, monomer_id=' ', insertion_code=' ', is_hetero=False, parent=None):
        super(Ligand, self).__init__(atoms,
          monomer_id, parent=parent)
        self.mol_code = mol_code
        self.insertion_code = insertion_code
        self.is_hetero = is_hetero

    def __repr__(self):
        return '<Ligand containing {} {}. Ligand code: {}>'.format(len(self.atoms), 'Atom' if len(self.atoms) == 1 else 'Atoms', self.mol_code)


__author__ = 'Christopher W. Wood, Kieran L. Hudson'