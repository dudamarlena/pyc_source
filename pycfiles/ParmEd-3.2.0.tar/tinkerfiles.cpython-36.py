# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/tinker/tinkerfiles.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 12939 bytes
"""
This module contains classes for reading various TINKER-style files
"""
from parmed.exceptions import TinkerError
from parmed.formats.registry import FileFormatType, load_file
from parmed.periodic_table import element_by_name, AtomicNum
from parmed.structure import Structure
from parmed.topologyobjects import Atom, Bond, Residue
from parmed.utils.io import genopen
from parmed.utils.six import add_metaclass, string_types
from parmed.utils.six.moves import range, zip

class KeywordControlFile(object):
    __doc__ = ' Reads and processes a keyword control file for TINKER simulations '
    _datatypes = {'PARAMETERS':str,  'A-AXIS':float,  'B-AXIS':float,  'C-AXIS':float, 
     'ALPHA':float,  'BETA':float,  'GAMMA':float}

    def __init__(self, fname):
        self.keywords = {'PARAMETERS':None, 
         'A-AXIS':None,  'B-AXIS':None,  'C-AXIS':None, 
         'ALPHA':None,  'BETA':None,  'GAMMA':None}
        for line in open(fname, 'r'):
            if not line.strip():
                pass
            else:
                words = line.split()
                key = words[0].upper()
                result = line.replace(words[0], '').strip()
                try:
                    self.keywords[key] = self._datatypes[key](result)
                except KeyError:
                    pass
                except ValueError:
                    raise TinkerError('Malformed keyword control file! Could not convert the value of %s into type %s' % (
                     key, self._datatypes[key]))


@add_metaclass(FileFormatType)
class XyzFile(Structure):
    __doc__ = ' Reads and processes a Tinker XYZ file\n\n    Parameters\n    ----------\n    fname : str or file-like\n        Name of the file, or the file object containing the XYZ file contents\n    seq : str, optional\n        Name of the file containing the residue (and chain) sequence. Default is\n        None (so every atom will be part of the same residue)\n    '

    @staticmethod
    def _check_atom_record(words):
        """ Checks that the tokenized line is consistent with an atom record

        Parameters
        ----------
        words : list of str
            Result of line.split() on a line of the file

        Returns
        -------
        is_atom : bool
            If it is consistent with an atom record, return True. Otherwise,
            False
        """
        if len(words) < 6:
            return False
        else:
            try:
                int(words[0])
            except ValueError:
                return False
            else:
                try:
                    float(words[1])
                except ValueError:
                    try:
                        int(words[1])
                    except ValueError:
                        pass
                    else:
                        return False
                else:
                    return False
                    try:
                        [float(w) for w in words[2:5]]
                    except ValueError:
                        return False
                    else:
                        try:
                            [int(w) for w in words[2:5]]
                        except ValueError:
                            pass
                        else:
                            return False
                            try:
                                [int(w) for w in words[5:]]
                            except ValueError:
                                return False

            return True

    @staticmethod
    def id_format(filename):
        """ Identify the file as a Tinker XYZ file

        Parameters
        ----------
        filename : str
            Name of the file to test whether or not it is a mol2 file

        Returns
        -------
        is_fmt : bool
            True if it is a xyz file, False otherwise
        """
        f = genopen(filename, 'r')
        words = f.readline().split()
        if not words:
            return False
        try:
            natom = int(words[0])
        except (ValueError, IndexError):
            return False
        else:
            if natom <= 0:
                return False
            else:
                words = f.readline().split()
                if len(words) == 6:
                    try:
                        [float(w) for w in words]
                    except ValueError:
                        if XyzFile._check_atom_record(words):
                            return True
                        return False
                    else:
                        words = f.readline().split()
                return XyzFile._check_atom_record(words)

    def __init__(self, fname, seq=None):
        super(XyzFile, self).__init__()
        if isinstance(fname, string_types):
            fxyz = genopen(fname, 'r')
            own_handle_xyz = True
        else:
            fxyz = fname
            own_handle_xyz = False
        if seq is not None:
            seqstruct = load_file(seq)
        else:
            try:
                natom = int(fxyz.readline().split()[0])
            except (ValueError, IndexError):
                raise TinkerError('Bad XYZ file format; first line')

            if seq is not None:
                if natom != len(seqstruct.atoms):
                    raise ValueError('Sequence file %s # of atoms does not match the # of atoms in the XYZ file' % seq)
            words = fxyz.readline().split()
            if len(words) == 6:
                if not XyzFile._check_atom_record(words):
                    self.box = [float(w) for w in words]
                    words = fxyz.readline().split()
            residue = Residue('SYS')
            residue.number = 1
            residue._idx = 0
            if seq is not None:
                residue = seqstruct.residues[0]
                atomic_number = _guess_atomic_number(words[1], residue)
            else:
                atomic_number = AtomicNum[element_by_name(words[1])]
        atom = Atom(atomic_number=atomic_number, name=(words[1]), type=(words[5]))
        atom.xx, atom.xy, atom.xz = [float(w) for w in words[2:5]]
        self.add_atom(atom, residue.name, residue.number, residue.chain, residue.insertion_code, residue.segid)
        bond_ids = [[int(w) for w in words[6:]]]
        for i, line in enumerate(fxyz):
            words = line.split()
            if seq is not None:
                residue = seqstruct.atoms[(i + 1)].residue
                atomic_number = _guess_atomic_number(words[1], residue)
            else:
                atomic_number = AtomicNum[element_by_name(words[1])]
            atom = Atom(atomic_number=atomic_number, name=(words[1]), type=(words[5]))
            atom.xx, atom.xy, atom.xz = [float(w) for w in words[2:5]]
            self.add_atom(atom, residue.name, residue.number, residue.chain, residue.insertion_code, residue.segid)
            bond_ids.append([int(w) for w in words[6:]])

        for atom, bonds in zip(self.atoms, bond_ids):
            i = atom.idx + 1
            for idx in bonds:
                if idx > i:
                    self.bonds.append(Bond(atom, self.atoms[(idx - 1)]))

        if seq is None:
            for atom in self.atoms:
                if len(atom.bonds) == 0:
                    atom.atomic_number = _guess_atomic_number(atom.name)

        if own_handle_xyz:
            fxyz.close()


class DynFile(object):
    __doc__ = ' Reads and processes a Tinker DYN file '

    def __init__(self, fname=None):
        if fname is not None:
            self.read(fname)

    def read(self, fname):
        """ Parses the .dyn file """
        f = open(fname, 'r')
        try:
            if f.readline().strip() != 'Number of Atoms and Title :':
                raise TinkerError('%s is not a recognized TINKER .dyn file' % fname)
            else:
                line = f.readline()
                self.natom, self.title = int(line[0:8].strip()), line[8:].strip()
                if f.readline().strip() != 'Periodic Box Dimensions :':
                    raise TinkerError('No periodic box dimension line')
                self.box = [0.0 for i in range(6)]
                words = f.readline().upper().split()
                self.box[0] = float(words[0].replace('D', 'E'))
                self.box[1] = float(words[1].replace('D', 'E'))
                self.box[2] = float(words[2].replace('D', 'E'))
                words = f.readline().upper().split()
                self.box[3] = float(words[0].replace('D', 'E'))
                self.box[4] = float(words[1].replace('D', 'E'))
                self.box[5] = float(words[2].replace('D', 'E'))
                if f.readline().strip() != 'Current Atomic Positions :':
                    raise TinkerError('No atomic positions in .dyn file')
                self.positions = [[0.0, 0.0, 0.0] for i in range(self.natom)]
                DynFile._read_section(f, self.positions, self.natom)
                line = f.readline().strip()
                if line == 'Current Translational Velocities :':
                    self.rigidbody = True
                    self.translational_velocities = [[0.0, 0.0, 0.0] for i in range(self.natom)]
                    DynFile._read_section(f, self.translational_velocities, self.natom)
                    if f.readline().strip() != 'Current Angular Velocities :':
                        raise TinkerError('Could not find Angular velocity section in .dyn file')
                    self.angular_velocities = [[0.0, 0.0, 0.0] for i in range(self.natom)]
                    DynFile._read_section(f, self.angular_velocities, self.natom)
                    if f.readline().strip() != 'Current Angular Momenta :':
                        raise TinkerError('Could not find angular momenta section in .dyn file')
                    self.angular_momenta = [[0.0, 0.0, 0.0] for i in range(self.natom)]
                    DynFile._read_section(f, self.angular_momenta, self.natom)
                else:
                    if line == 'Current Atomic Velocities :':
                        self.rigidbody = False
                        self.velocities = [[0.0, 0.0, 0.0] for i in range(self.natom)]
                        DynFile._read_section(f, self.velocities, self.natom)
                        if f.readline().strip() != 'Current Atomic Accelerations :':
                            raise TinkerError('Could not find accelerations in %s ' % fname)
                        self.accelerations = [[0.0, 0.0, 0.0] for i in range(self.natom)]
                        DynFile._read_section(f, self.accelerations, self.natom)
                        if f.readline().strip() != 'Alternate Atomic Accelerations :':
                            raise TinkerError('Could not find old accelerations in %s' % fname)
                        self.old_accelerations = [[0.0, 0.0, 0.0] for i in range(self.natom)]
                        DynFile._read_section(f, self.old_accelerations, self.natom)
                    else:
                        raise TinkerError('No velocities in %s' % fname)
        finally:
            f.close()

    @staticmethod
    def _read_section(f, container, natom):
        """
        Reads a section of an open file into the passed container. The
        container should be a 2-dimensional list of length natom x 3
        """
        for i in range(natom):
            words = f.readline().upper().split()
            try:
                container[i][0] = float(words[0].replace('D', 'E'))
                container[i][1] = float(words[1].replace('D', 'E'))
                container[i][2] = float(words[2].replace('D', 'E'))
            except (IndexError, ValueError):
                raise TinkerError('Could not parse values from dyn file')


def is_float(thing):
    try:
        float(thing)
        return True
    except ValueError:
        return False


def _guess_atomic_number(name, residue=None):
    """ Guesses the atomic number """
    name = ''.join(c for c in name if c.isalpha())
    if residue is None or len(residue.atoms) == 1:
        if len(name) > 1:
            try:
                return AtomicNum[(name[0].upper() + name[1].lower())]
            except KeyError:
                return AtomicNum[element_by_name(name)]

    return AtomicNum[element_by_name(name)]