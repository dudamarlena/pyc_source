# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cw12401/code/work/isambard/src/isambard/specifications/solenoid.py
# Compiled at: 2018-04-18 05:11:38
# Size of source mod 2**32: 4764 bytes
"""Contains classes for modeling alpha-solenoid proteins."""
import copy
from ampal import Assembly
import numpy
from .helix import Helix

class HelixPair(Assembly):
    __doc__ = 'Generates a pair of helixes oriented relative to a central axis.\n\n    Parameters\n    ----------\n    aas: (int, int), optional\n        Number of residues per helix.\n    axis_distances: (float, float), optional\n        Distance from central axis (Å).\n    z_shifts: (float, float), optional\n        Z-shift of the helices relative to the central axis.\n    phis: (float, float), optional\n        Rotation of the component helices around their local helical axis.\n    splays: (float, float), optional\n        The tiltedness of the helices in the plane relative to each other.\n    off_plane : (float, float), optional\n        The tiltedness of the helices out of plane relative to each other.\n    build: bool\n        Automatically build.\n\n    Attributes\n    ----------\n    aas: (int, int)\n        Number of residues per helix.\n    axis_distances: (float, float)\n        Distance from central axis (Å).\n    z_shifts: (float, float)\n        Z-shift of the helices relative to the central axis.\n    phis: (float, float)\n        Rotation of the component helices around their local helical axis.\n    splays: (float, float)\n        The tiltedness of the helices in the plane relative to each other.\n    off_plane : (float, float)\n        The tiltedness of the helices out of plane relative to each other.\n    '

    def __init__(self, aas=(10, 10), axis_distances=(-4.5, 4.5), z_shifts=(0, 0), phis=(0, 0), splays=(0, 0), off_plane=(0, 0), build=True):
        super().__init__()
        self.aas = aas
        self.axis_distances = axis_distances
        self.z_shifts = z_shifts
        self.phis = phis
        self.splays = splays
        self.off_plane = off_plane
        if build:
            self.build()
        self.relabel_all()

    def build(self):
        """Builds a `HelixPair` using the defined attributes."""
        for i in range(2):
            self._molecules.append(self.make_helix(self.aas[i], self.axis_distances[i], self.z_shifts[i], self.phis[i], self.splays[i], self.off_plane[i]))

    @staticmethod
    def make_helix(aa, axis_distance, z_shift, phi, splay, off_plane):
        """Builds a helix for a given set of parameters."""
        start = numpy.array([axis_distance, 0 + z_shift, 0])
        end = numpy.array([axis_distance, aa * 1.52 + z_shift, 0])
        mid = (start + end) / 2
        helix = Helix.from_start_and_end(start, end, aa=aa)
        helix.rotate(splay, (0, 0, 1), mid)
        helix.rotate(off_plane, (1, 0, 0), mid)
        helix.rotate(phi, helix.axis.unit_tangent, helix.helix_start)
        return helix


class Solenoid(Assembly):
    __doc__ = 'Generates a `Solenoid` from a repeating unit.\n\n    Parameters\n    ----------\n    repeat_unit: Ampal Object\n        Any AMPAL object.\n    num_of_repeats: int\n        Number of copies of the repeating unit.\n    radius:\n        Radius of super-helix.\n    rise:\n        Rise of super-helix\n    rot_ang:\n        Delta angle of each repeating unit.\n    handedness:\n        Handedness of the super-helix.\n\n    Attributes\n    ----------\n    repeat_unit: Ampal Object\n        Any AMPAL object.\n    num_of_repeats: int\n        Number of copies of the repeating unit.\n    radius:\n        Radius of super-helix.\n    rise:\n        Rise of super-helix\n    rot_ang:\n        Delta angle of each repeating unit.\n    handedness:\n        Handedness of the super-helix.\n    '

    def __init__(self, repeat_unit, num_of_repeats, radius, rise, rot_ang, handedness):
        super().__init__()
        ru = copy.deepcopy(repeat_unit)
        ru.translate(numpy.array([radius, 0, 0]) - ru.centre_of_mass)
        self.repeat_unit = ru
        self.num_of_repeats = num_of_repeats
        self.radius = radius
        self.rise = rise
        self.rot_ang = rot_ang
        self.handedness = handedness
        self.build()
        self.relabel_all()

    def build(self):
        """Builds a Solenoid using the defined attributes."""
        self._molecules = []
        if self.handedness == 'l':
            handedness = -1
        else:
            handedness = 1
        rot_ang = self.rot_ang * handedness
        for i in range(self.num_of_repeats):
            dup_unit = copy.deepcopy(self.repeat_unit)
            z = self.rise * i * numpy.array([0, 0, 1])
            dup_unit.translate(z)
            dup_unit.rotate(rot_ang * i, [0, 0, 1])
            self.extend(dup_unit)

        self.relabel_all()


__author__ = 'Christopher W. Wood'