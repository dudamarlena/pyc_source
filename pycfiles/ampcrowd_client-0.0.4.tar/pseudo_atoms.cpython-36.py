# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cw12401/code/work/ampal/src/ampal/pseudo_atoms.py
# Compiled at: 2018-04-11 08:19:10
# Size of source mod 2**32: 11344 bytes
__doc__ = 'Contains AMPAL objects representing pseudo atoms.'
from collections import OrderedDict
from .base_ampal import Atom, Monomer, Polymer, write_pdb
from .geometry import distance, radius_of_circumcircle

class PseudoGroup(Polymer):
    """PseudoGroup"""

    def __init__(self, monomers=None, polymer_id=' ', parent=None, sl=2):
        super().__init__(monomers=monomers,
          polymer_id=polymer_id,
          molecule_type='pseudo_group',
          parent=parent,
          sl=sl)

    def __repr__(self):
        return '<PseudoGroup chain containing {} {}>'.format(len(self._monomers), 'PseudoMonomer' if len(self._monomers) == 1 else 'PseudoMonomers')


class PseudoMonomer(Monomer):
    """PseudoMonomer"""

    def __init__(self, pseudo_atoms=None, mol_code='UNK', monomer_id=' ', insertion_code=' ', parent=None):
        super(PseudoMonomer, self).__init__(atoms=pseudo_atoms,
          monomer_id=monomer_id,
          parent=parent)
        self.mol_code = mol_code
        self.insertion_code = insertion_code
        self.is_hetero = True

    def __repr__(self):
        return '<PseudoMonomer containing {} {}. PseudoMonomer code: {}>'.format(len(self.atoms), 'PseudoAtom' if len(self.atoms) == 1 else 'PseudoAtoms', self.mol_code)

    @property
    def pdb(self):
        """Generates a PDB string for the `PseudoMonomer`."""
        pdb_str = write_pdb([
         self], ' ' if not self.tags['chain_id'] else self.tags['chain_id'])
        return pdb_str


class PseudoAtom(Atom):
    """PseudoAtom"""

    def __init__(self, coordinates, name='', occupancy=1.0, bfactor=1.0, charge=' ', parent=None):
        super().__init__(coordinates, element='C', atom_id=' ', occupancy=occupancy,
          bfactor=bfactor,
          charge=charge,
          state='A',
          parent=parent)
        self.name = name

    def __repr__(self):
        return '<PseudoAtom. Name: {}. Coordinates: ({:.3f}, {:.3f}, {:.3f})>'.format(self.name, self.x, self.y, self.z)


class Primitive(PseudoGroup):
    """Primitive"""

    def __init__(self, monomers=None, polymer_id=' ', parent=None, sl=2):
        super().__init__(monomers=monomers,
          polymer_id=polymer_id,
          parent=parent,
          sl=sl)

    def __repr__(self):
        return '<Primitive chain containing {} {}>'.format(len(self._monomers), 'PseudoMonomer' if len(self._monomers) == 1 else 'PseudoMonomers')

    @classmethod
    def from_coordinates(cls, coordinates):
        """Creates a `Primitive` from a list of coordinates."""
        prim = cls()
        for coord in coordinates:
            pm = PseudoMonomer(parent=prim)
            pa = PseudoAtom(coord, parent=pm)
            pm.atoms = OrderedDict([('CA', pa)])
            prim.append(pm)

        prim.relabel_all()
        return prim

    @property
    def coordinates(self):
        """Returns the backbone coordinates for the `Primitive`."""
        return [x._vector for x in self.get_atoms()]

    def rise_per_residue(self):
        """The rise per residue at each point on the Primitive.

        Notes
        -----
        Each element of the returned list is the rise per residue,
        at a point on the Primitive. Element i is the distance
        between primitive[i] and primitive[i + 1]. The final value
        is None.
        """
        rprs = [distance(self[i]['CA'], self[(i + 1)]['CA']) for i in range(len(self) - 1)]
        rprs.append(None)
        return rprs

    def radii_of_curvature(self):
        """The radius of curvature at each point on the Polymer primitive.

        Notes
        -----
        Each element of the returned list is the radius of curvature,
        at a point on the Polymer primitive. Element i is the radius
        of the circumcircle formed from indices [i-1, i, i+1] of the
        primitve. The first and final values are None.
        """
        rocs = []
        for i, _ in enumerate(self):
            if 0 < i < len(self) - 1:
                rocs.append(radius_of_circumcircle(self[(i - 1)]['CA'], self[i]['CA'], self[(i + 1)]['CA']))
            else:
                rocs.append(None)

        return rocs


__author__ = 'Jack W. Heal'