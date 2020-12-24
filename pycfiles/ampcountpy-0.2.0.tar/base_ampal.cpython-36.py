# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cw12401/code/work/ampal/src/ampal/base_ampal.py
# Compiled at: 2018-04-18 11:55:36
# Size of source mod 2**32: 26361 bytes
__doc__ = 'Contains the base and common classes for all AMPAL objects.'
from collections import OrderedDict
import itertools, numpy
from .data import ELEMENT_DATA, PDB_ATOM_COLUMNS
from .geometry import distance, Quaternion, centre_of_mass, rmsd

def cap(v, l):
    """Shortens string is above certain length."""
    s = str(v)
    if len(s) <= l:
        return s
    else:
        return s[-l:]


def find_atoms_within_distance(atoms, cutoff_distance, point):
    """Returns atoms within the distance from the point.

    Parameters
    ----------
    atoms : [ampal.atom]
        A list of `ampal.atoms`.
    cutoff_distance : float
        Maximum distance from point.
    point : (float, float, float)
        Reference point, 3D coordinate.

    Returns
    -------
    filtered_atoms : [ampal.atoms]
        `atoms` list filtered by distance.
    """
    return [x for x in atoms if distance(x, point) <= cutoff_distance]


def centre_of_atoms(atoms, mass_weighted=True):
    """ Returns centre point of any list of atoms.

    Parameters
    ----------
    atoms : list
        List of AMPAL atom objects.
    mass_weighted : bool, optional
        If True returns centre of mass, otherwise just geometric centre of points.

    Returns
    -------
    centre_of_mass : numpy.array
        3D coordinate for the centre of mass.
    """
    points = [x._vector for x in atoms]
    if mass_weighted:
        masses = [x.mass for x in atoms]
    else:
        masses = []
    return centre_of_mass(points=points, masses=masses)


def write_pdb(residues, chain_id=' ', alt_states=False, strip_states=False):
    """Writes a pdb file for a list of residues.

    Parameters
    ----------
    residues : list
        List of Residue objects.
    chain_id : str
        String of the chain id, defaults to ' '.
    alt_states : bool, optional
        If true, include all occupancy states of residues, else outputs primary state only.
    strip_states : bool, optional
        If true, remove all state labels from residues. Only use with alt_states false.

    Returns
    -------
    pdb_str : str
        String of the PDB file.
    """
    pdb_atom_col_dict = PDB_ATOM_COLUMNS
    out_pdb = []
    if len(str(chain_id)) > 1:
        poly_id = ' '
    else:
        poly_id = str(chain_id)
    for monomer in residues:
        if len(monomer.states) > 1:
            if alt_states:
                if not strip_states:
                    atom_list = (itertools.chain)(*[x[1].items() for x in sorted(monomer.states.items())])
        else:
            atom_list = monomer.atoms.items()
        if 'chain_id' in monomer.tags:
            poly_id = monomer.tags['chain_id']
        for atom_t, atom in atom_list:
            if strip_states:
                state_label = ' '
            elif atom.tags['state'] == 'A':
                if len(monomer.states) == 1:
                    state_label = ' '
            else:
                state_label = atom.tags['state']
            atom_data = {'atom_number':'{:>5}'.format(cap(atom.id, 5)),  'atom_name':'{:<4}'.format(cap(pdb_atom_col_dict[atom_t], 4)), 
             'alt_loc_ind':'{:<1}'.format(cap(state_label, 1)), 
             'residue_type':'{:<3}'.format(cap(monomer.mol_code, 3)), 
             'chain_id':'{:<1}'.format(cap(poly_id, 1)), 
             'res_num':'{:>4}'.format(cap(monomer.id, 4)), 
             'icode':'{:<1}'.format(cap(monomer.insertion_code, 1)), 
             'coord_str':'{0:>8.3f}{1:>8.3f}{2:>8.3f}'.format(*[x for x in atom]), 
             'occupancy':'{:>6.2f}'.format(atom.tags['occupancy']), 
             'temp_factor':'{:>6.2f}'.format(atom.tags['bfactor']), 
             'element':'{:>2}'.format(cap(atom.element, 2)), 
             'charge':'{:<2}'.format(cap(atom.tags['charge'], 2))}
            if monomer.is_hetero:
                pdb_line_template = 'HETATM{atom_number} {atom_name}{alt_loc_ind}{residue_type} {chain_id}{res_num}{icode}   {coord_str}{occupancy}{temp_factor}          {element}{charge}\n'
            else:
                pdb_line_template = 'ATOM  {atom_number} {atom_name}{alt_loc_ind}{residue_type} {chain_id}{res_num}{icode}   {coord_str}{occupancy}{temp_factor}          {element}{charge}\n'
            out_pdb.append((pdb_line_template.format)(**atom_data))

    return ''.join(out_pdb)


class BaseAmpal(object):
    """BaseAmpal"""

    @property
    def pdb(self):
        """Runs make_pdb in default mode."""
        return self.make_pdb()

    @property
    def centre_of_mass(self):
        """Returns the centre of mass of AMPAL object.

        Notes
        -----
        All atoms are included in calculation, call `centre_of_mass`
        manually if another selection is require.

        Returns
        -------
        centre_of_mass : numpy.array
            3D coordinate for the centre of mass.
        """
        elts = set([x.element for x in self.get_atoms()])
        masses_dict = {e:ELEMENT_DATA[e]['atomic mass'] for e in elts}
        points = [x._vector for x in self.get_atoms()]
        masses = [masses_dict[x.element] for x in self.get_atoms()]
        return centre_of_mass(points=points, masses=masses)

    def is_within(self, cutoff_dist, point):
        """Returns all atoms in ampal object within `cut-off` distance from the `point`."""
        return find_atoms_within_distance(self.get_atoms(), cutoff_dist, point)

    def get_atoms(self, ligands=True, inc_alt_states=False):
        raise NotImplementedError

    def make_pdb(self):
        raise NotImplementedError

    def rotate(self, angle, axis, point=None, radians=False, inc_alt_states=True):
        """Rotates every atom in the AMPAL object.

        Parameters
        ----------
        angle : float
            Angle that AMPAL object will be rotated.
        axis : 3D Vector (tuple, list, numpy.array)
            Axis about which the AMPAL object will be rotated.
        point : 3D Vector (tuple, list, numpy.array), optional
            Point that the axis lies upon. If `None` then the origin is used.
        radians : bool, optional
            True is `angle` is define in radians, False is degrees.
        inc_alt_states : bool, optional
            If true, will rotate atoms in all states i.e. includes
            alternate conformations for sidechains.
        """
        q = Quaternion.angle_and_axis(angle=angle, axis=axis, radians=radians)
        for atom in self.get_atoms(inc_alt_states=inc_alt_states):
            atom._vector = q.rotate_vector(v=(atom._vector), point=point)

    def translate(self, vector, inc_alt_states=True):
        """Translates every atom in the AMPAL object.

        Parameters
        ----------
        vector : 3D Vector (tuple, list, numpy.array)
            Vector used for translation.
        inc_alt_states : bool, optional
            If true, will rotate atoms in all states i.e. includes
            alternate conformations for sidechains.
        """
        vector = numpy.array(vector)
        for atom in self.get_atoms(inc_alt_states=inc_alt_states):
            atom._vector += vector

    def rmsd(self, other, backbone=False):
        """Calculates the RMSD between two AMPAL objects.

        Notes
        -----
        No fitting operation is performs and both AMPAL objects must
        have the same number of atoms.

        Parameters
        ----------
        other : AMPAL Object
            Any AMPAL object with `get_atoms` method.
        backbone : bool, optional
            Calculates RMSD of backbone only.
        """
        if not type(self) is type(other):
            raise AssertionError
        elif backbone and hasattr(self, 'backbone'):
            points1 = self.backbone.get_atoms()
            points2 = other.backbone.get_atoms()
        else:
            points1 = self.get_atoms()
            points2 = other.get_atoms()
        points1 = [x._vector for x in points1]
        points2 = [x._vector for x in points2]
        return rmsd(points1=points1, points2=points2)


class Polymer(BaseAmpal):
    """Polymer"""

    def __init__(self, monomers=None, ligands=None, polymer_id=' ', molecule_type='', parent=None, sl=2):
        if monomers:
            if isinstance(monomers, Monomer):
                self._monomers = [
                 monomers]
            else:
                if isinstance(monomers, list):
                    if isinstance(monomers[0], Monomer):
                        self._monomers = list(monomers)
                raise TypeError('Polymer objects can only be initialised empty, using a Monomer or a list of Monomers.')
        else:
            self._monomers = []
        self.id = str(polymer_id)
        self.parent = parent
        self.molecule_type = molecule_type
        self.ligands = ligands
        self.tags = {}
        self.sl = sl

    def __add__(self, other):
        if isinstance(other, Polymer):
            merged_polymer = self._monomers + other._monomers
        else:
            raise TypeError('Only Polymer objects may be merged with a Polymer.')
        return Polymer(monomers=merged_polymer, polymer_id=(self.id))

    def __len__(self):
        return len(self._monomers)

    def __getitem__(self, item):
        if isinstance(item, str):
            id_dict = {str(m.id):m for m in self._monomers}
            return id_dict[item]
        else:
            if isinstance(item, int):
                return self._monomers[item]
            return Polymer((self._monomers[item]), polymer_id=(self.id))

    def __repr__(self):
        return '<Polymer containing {} {}>'.format(len(self._monomers), 'Monomer' if len(self._monomers) == 1 else 'Monomers')

    def append(self, item):
        """Appends a `Monomer to the `Polymer`.

        Notes
        -----
        Does not update labelling.
        """
        if isinstance(item, Monomer):
            self._monomers.append(item)
        else:
            raise TypeError('Only Monomer objects can be appended to an Polymer.')

    def extend(self, polymer):
        """Extends the `Polymer` with the contents of another `Polymer`.

        Notes
        -----
        Does not update labelling.
        """
        if isinstance(polymer, Polymer):
            self._monomers.extend(polymer)
        else:
            raise TypeError('Only Polymer objects may be merged with a Polymer using "+".')

    def get_monomers(self, ligands=True):
        """Retrieves all the `Monomers` from the AMPAL object.

        Parameters
        ----------
        ligands : bool, optional
            If true, will include ligand `Monomers`.
        """
        if ligands:
            if self.ligands:
                monomers = self._monomers + self.ligands._monomers
        else:
            monomers = self._monomers
        return iter(monomers)

    def get_atoms(self, ligands=True, inc_alt_states=False):
        """Flat list of all the Atoms in the Polymer.

        Parameters
        ----------
        inc_alt_states : bool
            If true atoms from alternate conformations are included rather
            than only the "active" states.

        Returns
        -------
        atoms : itertools.chain
            Returns an iterator of all the atoms. Convert to list if you
            require indexing.
        """
        if ligands:
            if self.ligands:
                monomers = self._monomers + self.ligands._monomers
        else:
            monomers = self._monomers
        atoms = (itertools.chain)(*(list(m.get_atoms(inc_alt_states=inc_alt_states)) for m in monomers))
        return atoms

    def relabel_monomers(self, labels=None):
        """Relabels the either in numerically or using a list of labels.

        Parameters
        ----------
        labels : list, optional
            A list of new labels.

        Raises
        ------
        ValueError
            Raised if the number of labels does not match the number of
            component Monoer objects.
        """
        if labels:
            if len(self._monomers) == len(labels):
                for monomer, label in zip(self._monomers, labels):
                    monomer.id = str(label)

            else:
                error_string = 'Number of Monomers ({}) and number of labels ({}) must be equal.'
                raise ValueError(error_string.format(len(self._monomers), len(labels)))
        else:
            for i, monomer in enumerate(self._monomers):
                monomer.id = str(i + 1)

    def relabel_atoms(self, start=1):
        """Relabels all `Atoms` in numerical order.

        Parameters
        ----------
        start : int, optional
            Offset the labelling by `start` residues.
        """
        counter = start
        for atom in self.get_atoms():
            atom.id = counter
            counter += 1

    def relabel_all(self):
        """Relabels all `Monomers` and `Atoms` using default labeling."""
        self.relabel_monomers()
        self.relabel_atoms()

    def make_pdb(self, alt_states=False, inc_ligands=True):
        """Generates a PDB string for the `Polymer`.

        Parameters
        ----------
        alt_states : bool, optional
            Include alternate conformations for `Monomers` in PDB.
        inc_ligands : bool, optional
            Includes `Ligands` in PDB.

        Returns
        -------
        pdb_str : str
            String of the pdb for the `Polymer`. Generated using information
            from the component `Monomers`.
        """
        if any([False if x.id else True for x in self._monomers]):
            self.relabel_monomers()
        elif self.ligands and inc_ligands:
            monomers = self._monomers + self.ligands._monomers
        else:
            monomers = self._monomers
        pdb_str = write_pdb(monomers, (self.id), alt_states=alt_states)
        return pdb_str

    def get_reference_coords(self):
        """Gets list of coordinates of all reference atoms in the `Polymer`.

        Returns
        -------
        ref_coords : [numpy.array]
            List has the same length as the `Polymer`.
            The first, second and third elements of array i contain the
            x, y and z coordinates of the i-th reference atom.
        """
        return [x[x.reference_atom].array for x in self._monomers]


class Monomer(BaseAmpal):
    """Monomer"""

    def __init__(self, atoms=None, monomer_id=' ', parent=None):
        if isinstance(atoms, OrderedDict):
            self.states = dict(A=atoms)
            self._active_state = 'A'
        else:
            if isinstance(atoms, dict):
                self.states = atoms
                self._active_state = sorted(self.states.keys())[0]
            else:
                self.states = {'A': OrderedDict()}
                self._active_state = 'A'
        self.id = str(monomer_id)
        self.parent = parent
        self.tags = {}

    def __getitem__(self, key):
        return self.atoms.__getitem__(key)

    def __setitem__(self, key, value):
        self.atoms.__setitem__(key, value)

    def __iter__(self):
        return iter(self.atoms.values())

    def __len__(self):
        return len(self.atoms)

    def __repr__(self):
        return '<Monomer containing {} {}>'.format(len(self.atoms), 'Atom' if len(self.atoms) == 1 else 'Atoms')

    @property
    def active_state(self):
        """Defines which state dictionary should be used currently."""
        return self._active_state

    @active_state.setter
    def active_state(self, value):
        if value in self.states.keys():
            self._active_state = value
        else:
            raise KeyError('Selected alternate state is not available please use: {}'.format(list(self.states.keys())))

    @property
    def atoms(self):
        """Atoms in the currently active state."""
        return self.states[self.active_state]

    @atoms.setter
    def atoms(self, atom_dict):
        if not isinstance(atom_dict, OrderedDict):
            raise TypeError('Atoms dict must be of the type OrderedDict.')
        if self.states:
            self.states[self.active_state] = atom_dict

    def get_monomers(self):
        """Returns the this `Monomer`.

        Notes
        -----
        This function is only present for consistency in the interface.
        """
        return [
         self]

    def get_atoms(self, inc_alt_states=False):
        """Returns all atoms in the `Monomer`.

        Parameters
        ----------
        inc_alt_states : bool, optional
            If `True`, will return `Atoms` for alternate states.
        """
        if inc_alt_states:
            return (itertools.chain)(*[x[1].values() for x in sorted(list(self.states.items()))])
        else:
            return self.atoms.values()

    def make_pdb(self):
        """Generates a PDB string for the `Monomer`."""
        pdb_str = write_pdb([
         self], ' ' if not self.parent else self.parent.id)
        return pdb_str

    def close_monomers(self, group, cutoff=4.0):
        """Returns a list of Monomers from within a cut off distance of the Monomer

        Parameters
        ----------
        group: BaseAmpal or Subclass
            Group to be search for Monomers that are close to this Monomer.
        cutoff: float
            Distance cut off.

        Returns
        -------
        nearby_residues: [Monomers]
            List of Monomers within cut off distance.
        """
        nearby_residues = []
        for self_atom in self.atoms.values():
            nearby_atoms = group.is_within(cutoff, self_atom)
            for res_atom in nearby_atoms:
                if res_atom.parent not in nearby_residues:
                    nearby_residues.append(res_atom.parent)

        return nearby_residues


class Atom(object):
    """Atom"""

    def __init__(self, coordinates, element, atom_id=' ', res_label=None, occupancy=1.0, bfactor=1.0, charge=' ', state='A', parent=None):
        self._vector = numpy.array(coordinates)
        self.id = atom_id
        self.res_label = res_label
        self.element = element
        self.parent = parent
        self.tags = {'occupancy':occupancy, 
         'bfactor':bfactor, 
         'charge':charge, 
         'state':state}
        self._ff_id = None

    def __repr__(self):
        return '<{} Atom{}. Coordinates: ({:.3f}, {:.3f}, {:.3f})>'.format(ELEMENT_DATA[self.element.title()]['name'], '' if not self.res_label else ' ({})'.format(self.res_label), self.x, self.y, self.z)

    def __getitem__(self, item):
        return self._vector[item]

    def __setitem__(self, item, value):
        self._vector[item] = value

    def __sub__(self, other):
        """Subtracts coordinates and returns a `numpy.array`.

        Notes
        -----
        Objects themselves remain unchanged.
        """
        assert isinstance(other, Atom)
        return self._vector - other._vector

    def __add__(self, other):
        """Adds coordinates and returns a `numpy.array`.

        Notes
        -----
        Objects themselves remain unchanged.
        """
        assert isinstance(other, Atom)
        return self._vector + other._vector

    @property
    def array(self):
        """Converts the atomic coordinate to a `numpy.array`."""
        return self._vector

    @property
    def x(self):
        """The x coordinate."""
        return self._vector[0]

    @property
    def y(self):
        """The y coordinate."""
        return self._vector[1]

    @property
    def z(self):
        """The z coordinate."""
        return self._vector[2]

    @property
    def unique_id(self):
        """Creates a unique ID for the `Atom` based on its parents.

        Returns
        -------
        unique_id : (str, str, str)
            (polymer.id, residue.id, atom.id)
        """
        chain = self.parent.parent.id
        residue = self.parent.id
        return (
         chain, residue, self.id)

    def rotate(self, angle, axis, point=None, radians=False):
        """Rotates `Atom` by `angle`.

        Parameters
        ----------
        angle : float
            Angle that `Atom` will be rotated.
        axis : 3D Vector (tuple, list, numpy.array)
            Axis about which the `Atom` will be rotated.
        point : 3D Vector (tuple, list, numpy.array), optional
            Point that the `axis` lies upon. If `None` then the origin is used.
        radians : bool, optional
            True is `angle` is define in radians, False is degrees.
        """
        q = Quaternion.angle_and_axis(angle=angle, axis=axis, radians=radians)
        self._vector = q.rotate_vector(v=(self._vector), point=point)

    def translate(self, vector):
        """Translates `Atom`.

        Parameters
        ----------
        vector : 3D Vector (tuple, list, numpy.array)
            Vector used for translation.
        inc_alt_states : bool, optional
            If true, will rotate atoms in all states i.e. includes
            alternate conformations for sidechains.
        """
        vector = numpy.array(vector)
        self._vector += numpy.array(vector)


__author__ = 'Christopher W. Wood, Kieran L. Hudson'