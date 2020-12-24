# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\GitHub\AeroSandbox\aerosandbox\geometry\fuselage.py
# Compiled at: 2020-04-22 19:36:48
# Size of source mod 2**32: 3683 bytes
from aerosandbox.geometry.common import *

class Fuselage(AeroSandboxObject):
    __doc__ = '\n    Definition for a fuselage or other slender body (pod, etc.).\n    For now, all fuselages are assumed to be circular and fairly closely aligned with the body x axis. (<10 deg or so) # TODO update if this changes\n    '

    def __init__(self, name='Untitled Fuselage', x_le=0, y_le=0, z_le=0, xsecs=[], symmetric=False, circumferential_panels=24):
        self.name = name
        self.xyz_le = cas.vertcat(x_le, y_le, z_le)
        self.xsecs = xsecs
        self.symmetric = symmetric
        assert circumferential_panels % 2 == 0
        self.circumferential_panels = circumferential_panels

    def area_wetted(self):
        """
        Returns the wetted area of the fuselage.

        If the Fuselage is symmetric (i.e. two symmetric wingtip pods),
        returns the combined wetted area of both pods.
        :return:
        """
        area = 0
        for i in range(len(self.xsecs) - 1):
            this_radius = self.xsecs[i].radius
            next_radius = self.xsecs[(i + 1)].radius
            x_separation = self.xsecs[(i + 1)].x_c - self.xsecs[i].x_c
            area += cas.pi * (this_radius + next_radius) * cas.sqrt((this_radius - next_radius) ** 2 + x_separation ** 2)

        if self.symmetric:
            area *= 2
        return area

    def area_projected(self):
        """
        Returns the area of the fuselage as projected onto the XY plane (top-down view).

        If the Fuselage is symmetric (i.e. two symmetric wingtip pods),
        returns the combined projected area of both pods.
        :return:
        """
        area = 0
        for i in range(len(self.xsecs) - 1):
            this_radius = self.xsecs[i].radius
            next_radius = self.xsecs[(i + 1)].radius
            x_separation = self.xsecs[(i + 1)].x_c - self.xsecs[i].x_c
            area += (this_radius + next_radius) * x_separation

        if self.symmetric:
            area *= 2
        return area

    def length(self):
        """
        Returns the total front-to-back length of the fuselage. Measured as the difference between the x-coordinates
        of the leading and trailing cross sections.
        :return:
        """
        return cas.fabs(self.xsecs[(-1)].x_c - self.xsecs[0].x_c)


class FuselageXSec(AeroSandboxObject):
    __doc__ = '\n    Definition for a fuselage cross section ("X-section").\n    '

    def __init__(self, x_c=0, y_c=0, z_c=0, radius=0):
        self.x_c = x_c
        self.y_c = y_c
        self.z_c = z_c
        self.radius = radius
        self.xyz_c = cas.vertcat(x_c, y_c, z_c)

    def xsec_area(self):
        """
        Returns the FuselageXSec's cross-sectional (xsec) area.
        :return:
        """
        return cas.pi * self.radius ** 2