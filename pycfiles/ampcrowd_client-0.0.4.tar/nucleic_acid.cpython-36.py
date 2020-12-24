# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cw12401/code/work/ampal/src/ampal/nucleic_acid.py
# Compiled at: 2018-04-11 08:18:15
# Size of source mod 2**32: 4625 bytes
__doc__ = 'Contains AMPAL objects representing nucleic acids.'
from ampal.base_ampal import Polymer, Monomer

class Polynucleotide(Polymer):
    """Polynucleotide"""

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
    """Nucleotide"""

    def __init__(self, atoms=None, mol_code='UNK', monomer_id=' ', insertion_code=' ', is_hetero=False, parent=None):
        super().__init__(atoms, monomer_id, parent=parent)
        self.mol_code = mol_code
        self.mol_letter = mol_code[(-1)]
        self.insertion_code = insertion_code
        self.is_hetero = is_hetero
        self.reference_atom = 'P'


__author__ = 'Christopher W. Wood'