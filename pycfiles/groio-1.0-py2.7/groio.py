# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/groio/groio.py
# Compiled at: 2015-09-10 10:57:17
""" A simple library to handle the reading and writing of GRO file """
from __future__ import absolute_import
import itertools
GRO_FIELDS = {'resid': (
           (0, 5), int), 
   'resname': (
             (5, 10), str), 
   'atom_name': (
               (10, 15), str), 
   'atomid': (
            (15, 20), int), 
   'x': (
       (20, 28), float), 
   'y': (
       (28, 36), float), 
   'z': (
       (36, 44), float)}

class FormatError(Exception):
    """
    Exception raised when the file format is wrong.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


def parse_file(filin):
    """
    Handle the file type before calling the read function

    :Parameters:
        - filin: the filename name in str.
    :Returns:
        - the return of :read_gro:
    :Raise:
        -FormatError: raised if the file format does not fit.
    """
    with open(filin) as (f):
        try:
            return read_gro(f)
        except FormatError as e:
            raise FormatError(('{0} ({1})').format(e, filin))


def stop_at_empty_line(iterator):
    """
    Yield all item of an iterator but stop when the item is an empty line.

    An empty line is a string which is empty when stripped.
    """
    for line in iterator:
        if line.strip() == '':
            return
        yield line


def read_gro(lines):
    """
    Read the atoms, the header, and the box description from a gro file.

    Atoms are represented as dictionaries.

    :Parameters:
        - lines: an iterator over atom lines from the gro file. The two header
                 lines and the bottom line describing the box have to be
                 included.

    :Returns:
        - title: the title of the system as written on line 1 of the file
        - atoms: a list of atom, each atom is stored as a dictionary
        - box: the box description as written on the last line

    :Raise:
        - FormatError: raised if the file format does not fit.
    """
    lines = iter(lines)
    title = next(lines)
    nb_atoms = next(lines)
    for header in [title, nb_atoms]:
        try:
            a = dict((key, convert(header[begin:end].strip())) for key, ((begin, end), convert) in GRO_FIELDS.items())
            raise FormatError('Something is wrong in the format')
        except ValueError:
            pass

    atoms = []
    prev_line = next(lines)
    for line in stop_at_empty_line(lines):
        try:
            atoms.append(dict((key, convert(prev_line[begin:end].strip())) for key, ((begin, end), convert) in GRO_FIELDS.items()))
            prev_line = line
        except ValueError:
            raise FormatError('Something is wrong in the format')

    box = prev_line
    return (title, atoms, box)


def write_gro(title, atoms, box):
    """
    Yield lines of a GRO file from a title, a list of atoms and a box

    :Parameters:
        - title: the title of the system
        - atoms: a list of atom, each atom is stored as a dictionary
        - box: the box description as written on the last line
    """
    yield title
    yield ('{0}\n').format(len(atoms))
    for atom in atoms:
        yield ('{resid:>5}{resname:<5}{atom_name:>5}{atomid:>5}{x:8.3f}{y:8.3f}{z:8.3f}\n').format(**atom)

    yield box


def renumber(atoms):
    """
    Renumber the atoms and the residues from a list of atom.

    :Parameters:
        - atoms: a list of atom, each atom is stored as a dictionary

    :Returns:
        - new_atoms: the new list renumbered
    """
    new_atoms = []
    resid = 0
    prev_resid = 0
    for atomid, atom in enumerate(atoms, start=1):
        if atom['resid'] != prev_resid:
            resid += 1
            prev_resid = atom['resid']
        atom['resid'] = resid % 100000
        atom['atomid'] = atomid % 100000
        new_atoms.append(atom)

    return new_atoms