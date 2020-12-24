# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/molecule/_radius_of_gyration.py
# Compiled at: 2008-04-20 13:19:45
import numpy, math

def radius_of_gyration(mol):
    """return the radius of gyration of molecule"""
    if len(mol) == 0:
        return 0.0
    sum_coords = numpy.array([0.0, 0.0, 0.0])
    sum_mass = 0.0
    for i in range(len(mol)):
        sum_mass += mol.atoms[i].mass
        sum_coords += mol.atoms[i].mass * mol.coords[i]

    sum_coords /= sum_mass
    res = 0.0
    for i in range(len(mol)):
        res += sum((mol.coords[i] - sum_coords) ** 2) * mol.atoms[i].mass

    return math.sqrt(res / sum_mass)