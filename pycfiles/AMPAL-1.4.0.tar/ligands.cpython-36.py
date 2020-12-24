# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cw12401/code/work/ampal/src/ampal/ligands.py
# Compiled at: 2018-04-11 08:04:54
# Size of source mod 2**32: 3443 bytes
"""AMPAL objects that represent ligands."""
from ampal.base_ampal import Polymer, Monomer

class LigandGroup(Polymer):
    __doc__ = 'A container for `Ligand` `Monomers`.\n\n    Parameters\n    ----------\n    monomers : Monomer or [Monomer], optional\n        Monomer or list containing Monomer objects to form the Polymer().\n    polymer_id : str, optional\n        An ID that the user can use to identify the `Polymer`. This is\n        used when generating a pdb file using `Polymer().pdb`.\n    parent : ampal.Assembly, optional\n        Reference to `Assembly` containing the `Polymer`.\n    sl : int, optional\n        The default smoothing level used when calculating the\n        backbone primitive.\n    '

    def __init__(self, monomers=None, polymer_id=' ', parent=None, sl=2):
        super().__init__(monomers=monomers,
          polymer_id=polymer_id,
          molecule_type='ligands',
          parent=parent,
          sl=sl)

    def __repr__(self):
        return '<Ligands chain containing {} {}>'.format(len(self._monomers), 'Ligand' if len(self._monomers) == 1 else 'Ligands')


class Ligand(Monomer):
    __doc__ = '`Monomer` that represents a `Ligand`.\n\n    Notes\n    -----\n    All `Monomers` that do not have dedicated classes are\n    represented using the `Ligand` class.\n\n    Parameters\n    ----------\n    mol_code : str\n        PDB molecule code that represents the monomer.\n    atoms : OrderedDict, optional\n        OrderedDict containing Atoms for the Monomer. OrderedDict\n        is used to maintain the order items were added to the\n        dictionary.\n    monomer_id : str, optional\n        String used to identify the residue.\n    insertion_code : str, optional\n        Insertion code of monomer, used if reading from pdb.\n    is_hetero : bool, optional\n        True if is a hetero atom in pdb. Helps with PDB formatting.\n\n    Attributes\n    ----------\n    atoms : OrderedDict\n        OrderedDict containing Atoms for the Monomer. OrderedDict\n        is used to maintain the order items were added to the\n        dictionary.\n    mol_code : str\n        PDB molecule code that represents the `Ligand`.\n    insertion_code : str\n        Insertion code of `Ligand`, used if reading from pdb.\n    is_hetero : bool\n        True if is a hetero atom in pdb. Helps with PDB formatting.\n    self.states : dict\n        Contains an `OrderedDicts` containing atom information for each\n        state available for the `Ligand`.\n    id : str\n        String used to identify the residue.\n    parent : Polymer or None\n        A reference to the `LigandGroup` containing this `Ligand`.\n    tags : dict\n        A dictionary containing information about this AMPAL object.\n        The tags dictionary is used by AMPAL to cache information\n        about this object, but is also intended to be used by users\n        to store any relevant information they have.\n    '

    def __init__(self, mol_code, atoms=None, monomer_id=' ', insertion_code=' ', is_hetero=False, parent=None):
        super(Ligand, self).__init__(atoms,
          monomer_id, parent=parent)
        self.mol_code = mol_code
        self.insertion_code = insertion_code
        self.is_hetero = is_hetero

    def __repr__(self):
        return '<Ligand containing {} {}. Ligand code: {}>'.format(len(self.atoms), 'Atom' if len(self.atoms) == 1 else 'Atoms', self.mol_code)


__author__ = 'Christopher W. Wood, Kieran L. Hudson'