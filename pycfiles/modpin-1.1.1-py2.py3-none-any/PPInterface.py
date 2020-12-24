# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/patri/MODPIN/modpin/./src/SBI/structure/contacts/interface/PPInterface.py
# Compiled at: 2020-04-28 10:16:58
"""
PPInterface

author: jbonet
date:   03/2013

@oliva's lab
"""
from . import Interface
from ..contact import ContactAA

class PPInterface(Interface):
    """
    {Interface} between two protein chains
    """

    def __init__(self, protein_chain=None, protein_interactor=None, threshold_type='cb', threshold_distance=12, protein_centers=None, interactor_centers=None):
        if protein_centers is None:
            protein_centers = protein_chain.geometric_center(structure=True, hetero=False, water=False, by_residue=True)
        if interactor_centers is None:
            interactor_centers = protein_interactor.geometric_center(structure=True, hetero=False, water=False, by_residue=True)
        super(PPInterface, self).__init__(chain1=protein_chain, chain2=protein_interactor, threshold_type=threshold_type, threshold_distance=threshold_distance, chain1_centres=protein_centers, chain2_centers=interactor_centers)
        return

    @property
    def protein_chain(self):
        return self._chain1

    @property
    def protein_id(self):
        return self._chain1.globalID

    @property
    def protein_centers(self):
        return self._chain1_centers

    @property
    def protein_interactor(self):
        return self._chain2

    @property
    def interactor_id(self):
        return self._chain2.globalID

    @property
    def interactor_centers(self):
        return self._chain1_centers

    @property
    def protein_positions(self):
        return self._list_positions(1)

    @property
    def protein_view_interface(self):
        return self._view_interface_from(1)

    @property
    def interactor_positions(self):
        return self._list_positions(2)

    @property
    def interactor_view_interface(self):
        return self._view_interface_from(2)

    def _build(self):
        if len(self.protein_chain.aminoacids) == 0 or len(self.protein_interactor.aminoacids) == 0:
            return
        if (self.protein_chain.is_only_ca or self.protein_interactor.is_only_ca) and self.threshold_type == 'cb':
            self._threshold_type = 'ca'
            self._threshold_distance = self.threshold_distance + 4
        super(PPInterface, self)._build()
        for i in range(len(self._filtered[0])):
            new_contact = ContactAA(aminoacid1=self.protein_chain.aminoacids[self._filtered[0][i]], aminoacid2=self.protein_interactor.aminoacids[self._filtered[1][i]], threshold_type=self.threshold_type, threshold_distance=self.threshold_distance)
            if new_contact.is_underthreshold:
                self.contacts = new_contact

    def toString(self, all_types=False):
        data = []
        if not all_types:
            data.append(('{0._chain1.chain}\t{0._chain2.chain}\t{0.threshold_type}\t{0.threshold_distance}').format(self))
        else:
            data.append(('{0._chain1.chain}\t{0._chain2.chain}\tmin\tca\tcb\tgeometric\tbackbone').format(self))
        data.append(super(PPInterface, self).toString(all_types))
        return ('\n').join(data)