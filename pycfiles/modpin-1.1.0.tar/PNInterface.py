# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patricia/patricia/modppi/./src/SBI/structure/contacts/interface/PNInterface.py
# Compiled at: 2018-02-02 06:38:53
"""
PNInterface

author: jbonet
date:   03/2013

@oliva's lab
"""
from . import Interface
from ..contact import ContactAN
from SBI import SBIglobals

class PNInterface(Interface):
    """
    {Interface} between two protein chains
    """

    def __init__(self, protein=None, nucleotide=None, threshold_type='min', threshold_distance=8, protein_centers=None, nucleotide_centers=None):
        if protein_centers is None:
            protein_centers = protein.geometric_center(structure=True, hetero=False, water=False, by_residue=True)
        if nucleotide_centers is None:
            nucleotide_centers = nucleotide.geometric_center(structure=True, hetero=False, water=False, by_residue=True)
        super(PNInterface, self).__init__(chain1=protein, chain2=nucleotide, threshold_type=threshold_type, threshold_distance=threshold_distance, chain1_centres=protein_centers, chain2_centers=nucleotide_centers)
        return

    @property
    def protein(self):
        return self._chain1

    @property
    def protein_id(self):
        return self._chain1.globalID

    @property
    def protein_centers(self):
        return self._chain1_centers

    @property
    def nucleotide(self):
        return self._chain2

    @property
    def nucleotide_id(self):
        return self._chain2.globalID

    @property
    def nucleotide_centers(self):
        return self._chain1_centers

    @property
    def protein_positions(self):
        return self._list_positions(1)

    @property
    def protein_view_interface(self):
        return self._view_interface_from(1)

    @property
    def nucleotide_positions(self):
        return self._list_positions(2)

    @property
    def nucleotide_view_interface(self):
        return self._view_interface_from(2)

    def _build(self):
        if len(self.protein.aminoacids) == 0 or len(self.nucleotide.nucleotides) == 0:
            return
        super(PNInterface, self)._build()
        for i in range(len(self._filtered[0])):
            SBIglobals.alert('deepdebug', self, ('Analyze AN Contact for {0.type}:{0.number} - {1.type}:{1.number}').format(self.protein.aminoacids[self._filtered[0][i]], self.nucleotide.nucleotides[self._filtered[1][i]]))
            new_contact = ContactAN(aminoacid=self.protein.aminoacids[self._filtered[0][i]], nucleotide=self.nucleotide.nucleotides[self._filtered[1][i]], threshold_type=self.threshold_type, threshold_distance=self.threshold_distance)
            if new_contact.is_underthreshold:
                self.contacts = new_contact

    def toString(self, all_types=False):
        data = []
        if not all_types:
            data.append(('{0._chain1.chain}\t{0._chain2.chain}\t{0.threshold_type}\t{0.threshold_distance}').format(self))
        else:
            data.append(('{0._chain1.chain}\t{0._chain2.chain}\tmin\tgeometric\tcbbackbone').format(self))
        data.append(super(PNInterface, self).toString(all_types))
        return ('\n').join(data)