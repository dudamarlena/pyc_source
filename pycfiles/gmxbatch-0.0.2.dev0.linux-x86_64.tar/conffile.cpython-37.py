# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/conffiles/conffile.py
# Compiled at: 2020-03-26 06:18:53
# Size of source mod 2**32: 17484 bytes
import os
from typing import List, Optional
import numpy as np
from ..moleculetype import MoleculeType
dt_atom = np.dtype([
 (
  'index', np.int32),
 ('name', 'U8'),
 (
  'resi', np.int32),
 ('resn', 'U8'),
 (
  'x', np.float64),
 (
  'y', np.float64),
 (
  'z', np.float64),
 (
  'vx', np.float64),
 (
  'vy', np.float64),
 (
  'vz', np.float64)])

class Coordinates:
    __doc__ = 'Coordinate representation of the studied system\n\n    This class contains the coordinates and velocities, names, indices and residue information of all atoms in the\n    system.\n\n    Atoms are stored in a structured numpy array, exported as `atoms`.\n\n    Box size information is held in the `boxinfo` attribute. This is simply a list of floating point values, as read\n    from the respective .gro or .g96 file.\n\n    I/O in .gro and .g96 formats is supported.\n    '
    boxinfo: List[float]
    title: str
    _atoms: Optional[np.ndarray]
    filename: Optional[str]

    def __init__(self, filename: Optional[str]=None, lazyload: bool=True):
        """Create a new Coordinates instance

        :param filename: default file name to read from/write to
        :type filename: str
        :param lazyload: if True, the contents of the file will only be loaded on demand.
        :type lazyload: bool
        """
        self.boxinfo = [
         0, 0, 0]
        self.title = 'Unnamed system'
        self._atoms = None
        self.filename = filename
        if filename is not None:
            if not lazyload:
                if filename.lower().endswith('.gro'):
                    self.loadGRO(filename)
                else:
                    if filename.lower().endswith('.g96'):
                        self.loadG96(filename)
                    else:
                        raise ValueError('Invalid file format: {}'.format(filename))

    def sortAgainstTopology(self, moleculetypes: List[MoleculeType]):
        """Sort atoms to conform the order in the topology

        Limitations: only in-molecule sorting is allowed.

        :param moleculetypes: ordered list of molecule types
        :type moleculetypes: list of MoleculeType instances
        """
        newatoms = np.empty_like(self.atoms)
        if len(self.atoms) != sum([mt.count * len(mt.atoms) for mt in moleculetypes]):
            raise ValueError(f"The number of atoms in the molecule types ({sum([mt.count * len(mt.atoms) for mt in moleculetypes])}) and the coordinate set ({len(self.atoms)})is not equal.")
        atomsdone = 0
        for imt, mt in enumerate(moleculetypes):
            for imol in range(mt.count):
                tobesorted = self.atoms[atomsdone:atomsdone + len(mt.atoms)]
                for itpatom in mt.atoms:
                    p = np.logical_and(np.logical_and(tobesorted['name'] == itpatom.name, tobesorted['resi'] == itpatom.resi), tobesorted['resn'] == itpatom.resn)
                    if p.sum() == 0:
                        raise ValueError('No corresponding atom found in the coordinate set for atom #{} in moleculetype {}'.format(itpatom.index, mt.name))
                    else:
                        if p.sum() > 1:
                            raise ValueError('Multiple corresponding atoms found in the coordinate set for atom #{} in moleculetype {}'.format(itpatom.index, mt.name))
                        newatoms[atomsdone] = tobesorted[p]
                        atomsdone += 1

        assert len(newatoms) == atomsdone
        newatoms['index'] = np.arange(len(newatoms)) + 1
        self._atoms = newatoms
        self.write('sorted_{}'.format(os.path.split(self.filename)[(-1)]))

    def _format_gro(self, index: int) -> str:
        """Representation of an atom in a .gro file

        :param index: atom index
        :type index: int
        :return: the representation
        :rtype: str
        """
        if np.isnan(self.atoms[index]['vx']):
            return '{0[resi]:>5d}{0[resn]:>5s}{0[name]:>5s}{0[index]:>5d}{0[x]:>8.3f}{0[y]:>8.3f}{0[z]:>8.3f}'.format(self.atoms[index])
        return '{0[resi]:>5d}{0[resn]:>5s}{0[name]:>5s}{0[index]:>5d}{0[x]:>8.3f}{0[y]:>8.3f}{0[z]:>8.3f}{0[vx]:>8.4f}{0[vy]:>8.4f}{0[vz]:>8.4f}'.format(self.atoms[index])

    def _format_g96_position(self, index: int) -> str:
        """Representation of an atom in the "POSITIONS" section of a .g96 file

        :param index: atom index
        :type index: int
        :return: the representation
        :rtype: str
        """
        return '{0[resi]:<5d} {0[resn]:<5s} {0[name]:<5s}{0[index]:<7d}{0[x]:>15.9f}{0[y]:>15.9f}{0[z]:>15.9f}'.format(self.atoms[index])

    def _format_g96_velocity(self, index: int) -> str:
        """Representation of an atom in the "VELOCITIES" section of a .g96 file

        :param index: atom index
        :type index: int
        :return: the representation
        :rtype: str
        """
        return '{0[resi]:<5d} {0[resn]:<5s} {0[name]:<5s}{0[index]:<7d}{0[vx]:>15.9f}{0[vy]:>15.9f}{0[vz]:>15.9f}'.format(self.atoms[index])

    def loadGRO(self, grofile: str):
        """Read the state from a .gro file

        :param grofile: file name
        :type grofile: str
        """
        with open(grofile, 'rt') as (f):
            self.title = f.readline().strip()
            count = int(f.readline())
            self._atoms = np.empty(count, dtype=dt_atom)
            for i in range(count):
                line = f.readline()
                index = int(line[15:20])
                name = line[10:15].strip()
                resi = int(line[0:5])
                resn = line[5:10].strip()
                try:
                    x, y, z, vx, vy, vz = line[20:].split()
                except ValueError:
                    try:
                        x, y, z = line[20:].split()
                        vx = vy = vz = np.nan
                    except ValueError:
                        raise

                self.atoms[i] = (
                 index, name, resi, resn, x, y, z, vx, vy, vz)

            self.boxinfo = [float(x) for x in f.readline().split()]
        self.filename = grofile

    def writeGRO(self, grofile: str):
        """Write a .gro file

        :param grofile: file name
        :type grofile: str
        """
        with open(grofile, 'wt') as (f):
            f.write(self.title + '\n')
            f.write('{:d}\n'.format(len(self.atoms)))
            for i in range(len(self.atoms)):
                f.write(self._format_gro(i) + '\n')

            f.write(' '.join([str(x) for x in self.boxinfo]) + '\n')
        self.filename = grofile

    def loadG96(self, g96file: str):
        """Read the state from a .g96 file

        :param g96file: file name
        :type g96file: str
        """
        newatoms = []
        with open(g96file, 'rt') as (f):
            section = None
            for line in f:
                l = line.split('#')[0].strip()
                if not l:
                    continue
                elif l == 'END':
                    section = None
                elif section is None:
                    section = l
                elif section == 'TITLE':
                    self.title = l
                elif section == 'POSITION':
                    newatoms.append([
                     int(line[17:24]),
                     line[12:17].strip(),
                     int(line[0:5]),
                     line[6:11].strip(),
                     float(line[24:39]),
                     float(line[39:54]),
                     float(line[54:69]),
                     None, None, None])
                elif section == 'VELOCITY':
                    index = int(line[17:24])
                    name = line[12:17].strip()
                    resi = int(line[0:5])
                    resn = line[6:11].strip()
                    vx = float(line[24:39])
                    vy = float(line[39:54])
                    vz = float(line[54:69])
                    atm = [a for a in newatoms if a[0] == index if a[1] == name if a[2] == resi if a[3] == resn]
                    if len(atm) < 1:
                        raise ValueError('No corresponding atom found for velocity entry.')
                    else:
                        if len(atm) > 1:
                            raise ValueError('Ambiguity in corresponding atoms for velocity entry')
                    atm[0][-3] = vx
                    atm[0][-2] = vy
                    atm[0][-1] = vz
                elif section == 'BOX':
                    self.boxinfo = [float(x) for x in l.split()]
                else:
                    raise ValueError('Unknown section in G96 file: {}'.format(section))

        self._atoms = np.array([tuple(a) for a in newatoms], dtype=dt_atom)
        self.filename = g96file

    def writeG96(self, g96file: str):
        """Write a .g96 file

        :param g96file: file name
        :type g96file: str
        """
        with open(g96file, 'wt') as (f):
            f.write('TITLE\n{}\nEND\n'.format(self.title))
            f.write('POSITION\n')
            for i in range(len(self.atoms)):
                f.write(self._format_g96_position(i) + '\n')

            f.write('END\n')
            if self.hasVelocity:
                f.write('VELOCITY\n')
                for i in range(len(self.atoms)):
                    f.write(self._format_g96_velocity(i) + '\n')

                f.write('END\n')
            f.write('BOX\n')
            for b in self.boxinfo:
                f.write('{:>15.9f}'.format(b))

            f.write('\nEND\n')
        self.filename = g96file

    def load(self, filename: Optional[str]=None):
        """Read structures from a file. Currently .gro and .g96 files are understood

        :param filename: file name
        :type filename: str
        """
        if filename is None:
            filename = self.filename
        elif filename.lower().endswith('.gro'):
            self.loadGRO(filename)
        else:
            if filename.lower().endswith('.g96'):
                self.loadG96(filename)
            else:
                raise ValueError('Unknown file type: {}'.format(filename))

    def write(self, filename: Optional[str]=None):
        """Write the structure to a file

        Currently .gro and .g96 formats are available.

        :param filename: file name
        :type filename: str
        """
        if filename is None:
            filename = self.filename
        elif filename.lower().endswith('.gro'):
            self.writeGRO(filename)
        else:
            if filename.lower().endswith('.g96'):
                self.writeG96(filename)
            else:
                raise ValueError('Unknown file type: {}'.format(filename))

    @property
    def hasVelocity(self) -> bool:
        """Check if all atoms have velocities or not.

        :return: True if all atoms have meaningful velocity values, False if one or more velocity values are invalid.
        :rtype: bool
        """
        finite_pred = np.logical_and(np.isfinite(self.atoms['vx']), np.logical_and(np.isfinite(self.atoms['vy']), np.isfinite(self.atoms['vz'])))
        return bool(np.all(finite_pred))

    def __iadd__(self, other: 'Coordinates'):
        """Stack two coordinate sets, keeping the box information and file name from the first one.

        :param other: other coordinate set
        :type other: Coordinates instance
        """
        self._atoms = np.concatenate((self.atoms, other.atoms))
        self.reindex()

    def reindex(self):
        """Update atom indices, starting from 1. Also residue indices, starting from 1. Residues must be contiguous."""
        self.atoms['index'] = np.arange(len(self.atoms)) + 1
        currentoldindex = None
        currentnewindex = 0
        for iatom in range(len(self.atoms)):
            if self.atoms[iatom]['resi'] != currentoldindex:
                currentoldindex = self.atoms[iatom]['resi']
                currentnewindex += 1
            self.atoms[iatom]['resi'] = currentnewindex

    def update_column(self, **kwargs):
        """Updates a specific column of the structure file with new values from another structure file.

        Columns to be updated have to be given as keyword arguments, with 1D array-like values. Valid
        keywords are e.g. 'name', 'resi', 'resn', 'index', 'x', 'y', 'z', 'vx', 'vy', 'vz'.

        :param kwargs: keyword arguments: column name -> one-dimensional array-like
        :type kwargs: 'str = 1D array-like' pairs
        """
        for key, values in kwargs.items():
            try:
                self.atoms[key] = values
            except ValueError:
                if key not in dt_atom.names:
                    print('There is no column named: {key}!\nUse head() function to see column names!'.format(key=key))
                if len(self.atoms[key]) != len(values):
                    print('Number of rows does not match for {key} column!'.format(key=key))

    def head(self, rows: int=5):
        """Prints out a given number of rows in a formatted way (GRO file scheme)

        :param rows: number of rows to show
        :type rows: int
        """
        if len(list(filter(lambda x: np.isnan(x), self.atoms[:rows]['vx']))) != 0:
            print('resi resn name index       x       y      z')
            for row in range(min(rows, len(self.atoms))):
                print(self._format_gro(row))

        else:
            print('resi resn name index       x       y       z      vx      vy      vz')
            for row in range(min(rows, len(self.atoms))):
                print(self._format_gro(row))

    def __deepcopy__(self, memodict={}) -> 'Coordinates':
        """Create a deep copy of this coordinate set."""
        copied = Coordinates()
        copied.filename = self.filename
        copied.boxinfo = self.boxinfo[:]
        copied.title = self.title
        if self._atoms is not None:
            copied._atoms = np.copy(self._atoms)
        else:
            copied._atoms = None
        return copied

    @property
    def atoms(self) -> np.ndarray:
        if self._atoms is None:
            self.load()
        return self._atoms

    def delAtom(self, index: Optional[int]=None, name: Optional[str]=None, resi: Optional[int]=None, resn: Optional[int]=None):
        """Remove one or more atoms, selected by matching index, name, resi or resn properties.

        Specifying None for the property acts as a wildcard.

        :param index: index of an atom to remove
        :type index: int or None
        :param name: name of the atom to remove
        :type name: str or None
        :param resi: residue index of the atom to remove
        :type resi: int or None
        :param resn: residue name of the atom to remove
        :type resn: int or None
        """
        deletable = self.selectAtoms(index, name, resi, resn)
        self._atoms = np.copy(self._atoms[(~deletable)])

    def selectAtoms(self, index: Optional[int]=None, name: Optional[str]=None, resi: Optional[int]=None, resn: Optional[int]=None) -> np.ndarray:
        """Select one or more atoms by matching index, name, resi or resn properties.

        Specifying None for the property acts as a wildcard.

        :param index: index of an atom to remove
        :type index: int or None
        :param name: name of the atom to remove
        :type name: str or None
        :param resi: residue index of the atom to remove
        :type resi: int or None
        :param resn: residue name of the atom to remove
        :type resn: int or None
        :return: one-dimensional numpy boolean array, having the same length as the number of atoms
        :rtype: np.ndarray (dtype: np.bool)
        """
        selected = np.ones((len(self._atoms)), dtype=(np.bool))
        if index is not None:
            selected = np.logical_and(selected, self.atoms['index'] == index)
        if name is not None:
            selected = np.logical_and(selected, self.atoms['name'] == name)
        if resi is not None:
            selected = np.logical_and(selected, self.atoms['resi'] == resi)
        if resn is not None:
            selected = np.logical_and(selected, self.atoms['resn'] == resn)
        return selected

    @property
    def residuenames(self) -> List[str]:
        """Get a list of residue names

        :return: list of residue names in order
        :rtype: list of str
        """
        return [self.atoms[(self.atoms['resi'] == resi)][0]['resn'] for resi in self.residuenumbers()]

    @property
    def residuenumbers(self) -> List[int]:
        """Get a list of residue numbers

        :return: residue numbers
        :rtype: list of integers
        """
        return sorted(list(np.unique(self.atoms['resi'])))

    def __len__(self):
        """Return the number of atoms"""
        return len(self.atoms)