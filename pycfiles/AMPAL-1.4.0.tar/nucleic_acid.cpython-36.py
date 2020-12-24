# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cw12401/code/work/ampal/src/ampal/nucleic_acid.py
# Compiled at: 2018-04-11 08:18:15
# Size of source mod 2**32: 4625 bytes
"""Contains AMPAL objects representing nucleic acids."""
from ampal.base_ampal import Polymer, Monomer

class Polynucleotide(Polymer):
    __doc__ = '`Polymer` type object that represents a `Polynucleotide`.\n\n    Parameters\n    ----------\n    monomers : Nucleotide or [Nucleotide], optional\n        `Nucleotide` or list containing `Nucleotide` objects to form the\n        `Polynucleotide`.\n    polymer_id : str, optional\n        An ID that the user can use to identify the `Polynucleotide`. This is\n        used when generating a pdb file using `Polynucleotide().pdb`.\n    parent : ampal.Assembly, optional\n        Reference to `Assembly` containing the `Polynucleotide`.\n    sl : int, optional\n        The default smoothing level used when calculating the\n        backbone primitive.\n\n    Attributes\n    ----------\n    id : str\n        `Polynucleotide` ID\n    parent : ampal.Assembly or None\n        Reference to `Assembly` containing the `Polynucleotide`\n    molecule_type : str\n        A description of the type of `Polymer` i.e. Protein, DNA etc.\n    ligands : ampal.LigandGroup\n        A `LigandGroup` containing all the `Ligands` associated with this\n        `Polynucleotide` chain.\n    tags : dict\n        A dictionary containing information about this AMPAL object.\n        The tags dictionary is used by AMPAL to cache information\n        about this object, but is also intended to be used by users\n        to store any relevant information they have.\n    sl : int\n        The default smoothing level used when calculating the\n        backbone primitive.\n\n    Raises\n    ------\n    TypeError\n        `Polymer` type objects can only be initialised empty or using\n        a `Monomer`.\n    '

    def __init__(self, monomers=None, polymer_id=' ', parent=None, sl=2):
        super().__init__(monomers=monomers,
          polymer_id=polymer_id,
          molecule_type='nucleic_acid',
          parent=parent,
          sl=sl)

    @property
    def sequence(self):
        """Returns the sequence of the `Polynucleotide` as a string.

        Returns
        -------
        sequence : str
            String of the monomer sequence of the `Polynucleotide`.
        """
        seq = [x.mol_code for x in self._monomers]
        return ' '.join(seq)


class Nucleotide(Monomer):
    __doc__ = 'Represents a nucleotide base.\n\n    Parameters\n    ----------\n    atoms : OrderedDict, optional\n        OrderedDict containing Atoms for the `Nucleotide`. OrderedDict\n        is used to maintain the order items were added to the\n        dictionary.\n    mol_code : str, optional\n        One or three letter code that represents the `Nucleotide`.\n    monomer_id : str, optional\n        String used to identify the `Nucleotide`.\n    insertion_code : str, optional\n        Insertion code of `Nucleotide`, used if reading from pdb.\n    is_hetero : bool, optional\n        True if is a hetero atom in pdb. Helps with PDB formatting.\n    parent : ampal.Polynucleotide, optional\n        Reference to `Polynucleotide` containing the `Nucleotide`.\n\n    Attributes\n    ----------\n    mol_code : str\n        PDB molecule code that represents the `Nucleotide`.\n    insertion_code : str\n        Insertion code of `Nucleotide`, used if reading from pdb.\n    is_hetero : bool\n        True if is a hetero atom in pdb. Helps with PDB formatting.\n    states : dict\n        Contains an `OrderedDicts` containing atom information for each\n        state available for the `Nucleotide`.\n    id : str\n        String used to identify the `Nucleotide`.\n    reference_atom : str\n        The key that corresponds to the reference `Atom`. This is used\n        by various functions, for example backbone primitives are\n        calculated using the `Atom` defined using this key.\n    parent : Polynucleotide or None\n        A reference to the `Polynucleotide` containing this `Nucleotide`.\n    tags : dict\n        A dictionary containing information about this AMPAL object.\n        The tags dictionary is used by AMPAL to cache information\n        about this object, but is also intended to be used by users\n        to store any relevant information they have.\n\n    Raises\n    ------\n    ValueError\n        Raised if `mol_code` is not length 1 or 3.\n    '

    def __init__(self, atoms=None, mol_code='UNK', monomer_id=' ', insertion_code=' ', is_hetero=False, parent=None):
        super().__init__(atoms, monomer_id, parent=parent)
        self.mol_code = mol_code
        self.mol_letter = mol_code[(-1)]
        self.insertion_code = insertion_code
        self.is_hetero = is_hetero
        self.reference_atom = 'P'


__author__ = 'Christopher W. Wood'