# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cw12401/code/work/ampal/src/ampal/pseudo_atoms.py
# Compiled at: 2018-04-11 08:19:10
# Size of source mod 2**32: 11344 bytes
"""Contains AMPAL objects representing pseudo atoms."""
from collections import OrderedDict
from .base_ampal import Atom, Monomer, Polymer, write_pdb
from .geometry import distance, radius_of_circumcircle

class PseudoGroup(Polymer):
    __doc__ = 'Container for `PseudoMonomer`, inherits from `Polymer`.\n\n    Parameters\n    ----------\n    monomers : PseudoAtom or [PseudoGroup], optional\n        `PseudoMonomer` or list containing `PseudoMonomer` objects to form the\n        `PseudoGroup`.\n    polymer_id : str, optional\n        An ID that the user can use to identify the `PseudoGroup`. This is\n        used when generating a pdb file using `PseudoGroup().pdb`.\n    parent : ampal.Assembly, optional\n        Reference to `Assembly` containing the `PseudoGroup`.\n    sl : int, optional\n        The default smoothing level used when calculating the\n        backbone primitive.\n\n    Attributes\n    ----------\n    id : str\n        `PseudoGroup` ID\n    parent : ampal.Assembly or None\n        Reference to `Assembly` containing the `PseudoGroup`\n    molecule_type : str\n        A description of the type of `Polymer` i.e. Protein, DNA etc.\n    ligands : ampal.LigandGroup\n        A `LigandGroup` containing all the `Ligands` associated with this\n        `PseudoGroup` chain.\n    tags : dict\n        A dictionary containing information about this AMPAL object.\n        The tags dictionary is used by AMPAL to cache information\n        about this object, but is also intended to be used by users\n        to store any relevant information they have.\n    sl : int\n        The default smoothing level used when calculating the\n        backbone primitive.\n\n    Raises\n    ------\n    TypeError\n        `Polymer` type objects can only be initialised empty or using\n        a `Monomer`.\n    '

    def __init__(self, monomers=None, polymer_id=' ', parent=None, sl=2):
        super().__init__(monomers=monomers,
          polymer_id=polymer_id,
          molecule_type='pseudo_group',
          parent=parent,
          sl=sl)

    def __repr__(self):
        return '<PseudoGroup chain containing {} {}>'.format(len(self._monomers), 'PseudoMonomer' if len(self._monomers) == 1 else 'PseudoMonomers')


class PseudoMonomer(Monomer):
    __doc__ = 'Represents a collection of `PsuedoAtoms`.\n\n    Parameters\n    ----------\n    pseudo_atoms : OrderedDict, optional\n        OrderedDict containing Atoms for the `PsuedoMonomer`. OrderedDict\n        is used to maintain the order items were added to the\n        dictionary.\n    mol_code : str, optional\n        One or three letter code that represents the `PsuedoMonomer`.\n    monomer_id : str, optional\n        String used to identify the `PsuedoMonomer`.\n    insertion_code : str, optional\n        Insertion code of `PsuedoMonomer`, used if reading from pdb.\n    is_hetero : bool, optional\n        True if is a hetero atom in pdb. Helps with PDB formatting.\n    parent : ampal.PseudoGroup, optional\n        Reference to `PseudoGroup` containing the `PsuedoMonomer`.\n\n    Attributes\n    ----------\n    mol_code : str\n        PDB molecule code that represents the `Nucleotide`.\n    insertion_code : str\n        Insertion code of `Nucleotide`, used if reading from pdb.\n    is_hetero : bool\n        True if is a hetero atom in pdb. Helps with PDB formatting.\n    states : dict\n        Contains an `OrderedDicts` containing atom information for each\n        state available for the `Nucleotide`.\n    id : str\n        String used to identify the `Nucleotide`.\n    reference_atom : str\n        The key that corresponds to the reference `Atom`. This is used\n        by various functions, for example backbone primitives are\n        calculated using the `Atom` defined using this key.\n    parent : Polynucleotide or None\n        A reference to the `Polynucleotide` containing this `Nucleotide`.\n    tags : dict\n        A dictionary containing information about this AMPAL object.\n        The tags dictionary is used by AMPAL to cache information\n        about this object, but is also intended to be used by users\n        to store any relevant information they have.\n\n    Raises\n    ------\n    ValueError\n        Raised if `mol_code` is not length 1 or 3.\n    '

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
    __doc__ = 'Object containing 3D coordinates and name.\n\n    Notes\n    -----\n    Used to represent pseudo atoms (e.g. centre_of_mass) in ISAMBARD.\n\n    Parameters\n    ----------\n    coordinates : 3D Vector (tuple, list, numpy.array)\n        Position of `PseudoAtom` in 3D space.\n    element : str\n        Element of `PseudoAtom`.\n    atom_id : str\n        Identifier for `PseudoAtom`, usually a number.\n    res_label : str, optional\n        Label used in `Monomer` to refer to the `PseudoAtom` type i.e.\n        "CA" or "OD1".\n    occupancy : float, optional\n        The occupancy of the `PseudoAtom`.\n    bfactor : float, optional\n        The bfactor of the `PseudoAtom`.\n    charge : str, optional\n        The point charge of the `PseudoAtom`.\n    state : str\n        The state of this `PseudoAtom`. Used to identify `PseudoAtoms`\n        with a number of conformations.\n    parent : ampal.Monomer, optional\n       A reference to the `Monomer` containing this `PseudoAtom`.\n\n    Attributes\n    ----------\n    id : str\n        Identifier for `PseudoAtom`, usually a number.\n    res_label : str\n        Label used in `PseudoGroup` to refer to the `Atom` type i.e. "CA" or "OD1".\n    element : str\n        Element of `Atom`.\n    parent : ampal.PseudoAtom\n       A reference to the `PseudoGroup` containing this `PseudoAtom`.\n        number of conformations.\n    tags : dict\n        A dictionary containing information about this AMPAL object.\n        The tags dictionary is used by AMPAL to cache information\n        about this object, but is also intended to be used by users\n        to store any relevant information they have.\n    '

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
    __doc__ = 'A backbone path composed of `PseudoAtoms`.\n\n    Parameters\n    ----------\n    pseudo_atoms : OrderedDict, optional\n        OrderedDict containing Atoms for the `PsuedoMonomer`. OrderedDict\n        is used to maintain the order items were added to the\n        dictionary.\n    mol_code : str, optional\n        One or three letter code that represents the `PsuedoMonomer`.\n    monomer_id : str, optional\n        String used to identify the `PsuedoMonomer`.\n    insertion_code : str, optional\n        Insertion code of `PsuedoMonomer`, used if reading from pdb.\n    is_hetero : bool, optional\n        True if is a hetero atom in pdb. Helps with PDB formatting.\n    parent : ampal.PseudoGroup, optional\n        Reference to `PseudoGroup` containing the `PsuedoMonomer`.\n\n    Attributes\n    ----------\n    mol_code : str\n        PDB molecule code that represents the `Nucleotide`.\n    insertion_code : str\n        Insertion code of `Nucleotide`, used if reading from pdb.\n    is_hetero : bool\n        True if is a hetero atom in pdb. Helps with PDB formatting.\n    states : dict\n        Contains an `OrderedDicts` containing atom information for each\n        state available for the `Nucleotide`.\n    id : str\n        String used to identify the `Nucleotide`.\n    reference_atom : str\n        The key that corresponds to the reference `Atom`. This is used\n        by various functions, for example backbone primitives are\n        calculated using the `Atom` defined using this key.\n    parent : Polynucleotide or None\n        A reference to the `Polynucleotide` containing this `Nucleotide`.\n    tags : dict\n        A dictionary containing information about this AMPAL object.\n        The tags dictionary is used by AMPAL to cache information\n        about this object, but is also intended to be used by users\n        to store any relevant information they have.\n\n    Raises\n    ------\n    ValueError\n        Raised if `mol_code` is not length 1 or 3.\n    '

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