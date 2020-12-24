# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/sella/internal/get_internal.py
# Compiled at: 2020-01-27 19:04:42
# Size of source mod 2**32: 2705 bytes
import numpy as np
from sella.constraints import get_constraints, merge_internal_constraints, cons_to_dict
from .int_find2 import find_angles, find_dihedrals
from sella.internal.int_find import find_bonds
from sella.internal.int_classes import CartToInternal
_cons_shapes = dict(cart=2, bonds=2, angles=3, dihedrals=4, angle_sums=4, angle_diffs=4)

def extract_dummy_constraints(natoms, con_user):
    con_dummy = dict()
    for key, size in _cons_shapes.items():
        data = []
        for row in con_user.get(key, []):
            if np.any(np.asarray(row) >= natoms):
                data.append(row)

        con_dummy[key] = np.array(data, dtype=(np.int32)).reshape((-1, size))

    return con_dummy


def get_internal(atoms, con_user=None, target_user=None, atol=15.0, dummies=None, conslast=None):
    if con_user is None:
        con_user = dict()
    else:
        if target_user is None:
            target_user = dict()
        bonds, nbonds, c10y = find_bonds(atoms)
        if conslast is None:
            dinds = None
        else:
            dinds = np.array(conslast.dinds)
        con_user, target_user = cons_to_dict(conslast)
    con_dummy = extract_dummy_constraints(len(atoms), con_user)
    angles, dummies, dinds, angle_sums, bcons, acons, dcons, adiffs = find_angles(atoms, atol, bonds, nbonds, c10y, dummies, dinds)
    dihedrals = find_dihedrals(atoms + dummies, atol, bonds, angles, nbonds, c10y, dinds)
    bonds = np.vstack((bonds, np.atleast_2d(con_dummy['bonds']), bcons))
    angles = np.vstack((angles, np.atleast_2d(con_dummy['angles']), acons))
    dihedrals = np.vstack((dihedrals, np.atleast_2d(con_dummy['dihedrals']),
     dcons))
    adiffs = np.vstack((np.atleast_2d(con_dummy['angle_diffs']), adiffs))
    internal = CartToInternal(atoms, bonds=bonds,
      angles=angles,
      dihedrals=dihedrals,
      angle_sums=angle_sums,
      angle_diffs=adiffs,
      dummies=dummies,
      atol=atol)
    con, target = merge_internal_constraints(con_user, target_user, bcons, acons, dcons, adiffs)
    constraints = get_constraints(atoms, con, target, dummies, dinds, proj_trans=False,
      proj_rot=False)
    return (
     internal, constraints, dummies)