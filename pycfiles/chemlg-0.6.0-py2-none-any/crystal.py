# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gabriele/workspace/chemlab/chemlab/core/spacegroup/crystal.py
# Compiled at: 2015-11-03 19:31:06
__doc__ = '\nA module for chemlab for simple creation of crystalline structures from\nknowledge of the space group.\n\n'
import numpy as np
from collections import Counter
from .spacegroup import Spacegroup
from ..system import System
from .cell import cellpar_to_cell
__all__ = [
 'crystal']

def crystal(positions, molecules, group, cellpar=[
 1.0, 1.0, 1.0, 90, 90, 90], repetitions=[1, 1, 1]):
    """Build a crystal from atomic positions, space group and cell
    parameters.
    
    **Parameters**

    positions: list of coordinates
        A list of the atomic positions 
    molecules: list of Molecule
        The molecules corresponding to the positions, the molecule will be
        translated in all the equivalent positions.
    group: int | str
        Space group given either as its number in International Tables
        or as its Hermann-Mauguin symbol.
    repetitions:
        Repetition of the unit cell in each direction
    cellpar:
        Unit cell parameters

    This function was taken and adapted from the *spacegroup* module 
    found in `ASE <https://wiki.fysik.dtu.dk/ase/>`_.

    The module *spacegroup* module was originally developed by Jesper
    Frills.

    """
    sp = Spacegroup(group)
    sites, kind = sp.equivalent_sites(positions)
    nx, ny, nz = repetitions
    reptot = nx * ny * nz
    a, b, c = cellpar_to_cell(cellpar)
    cry = System()
    i = 0
    with cry.batch() as (batch):
        for x in range(nx):
            for y in range(ny):
                for z in range(nz):
                    for s, ki in zip(sites, kind):
                        tpl = molecules[ki]
                        tpl.move_to(s[0] * a + s[1] * b + s[2] * c + a * x + b * y + c * z)
                        batch.append(tpl.copy())

    cry.box_vectors = np.array([a * nx, b * ny, c * nz])
    return cry


if __name__ == '__main__':
    import doctest