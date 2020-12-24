# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\GitHub\AeroSandbox\aerosandbox\performance.py
# Compiled at: 2020-04-18 12:09:58
# Size of source mod 2**32: 5616 bytes
import casadi as cas
from aerosandbox.geometry import *

class OperatingPoint(AeroSandboxObject):

    def __init__(self, density=1.225, viscosity=1.81e-05, velocity=10, mach=0, alpha=5, beta=0, p=0, q=0, r=0):
        self.density = density
        self.viscosity = viscosity
        self.velocity = velocity
        self.mach = mach
        self.alpha = alpha
        self.beta = beta
        self.p = p
        self.q = q
        self.r = r

    def dynamic_pressure(self):
        """ Dynamic pressure of the working fluid
        .. math:: p = \x0crac{\\rho u^2}{2}
        Args:
            self.density (float): Density of the working fluid in .. math:: \x0crac{kg}{m^3}
            self.velocity (float): Velocity of the working fluid in .. math:: \x0crac{m}{s}
        Returns:
            float: Dynamic pressure of the working fluid in .. math:: \x0crac{N}{m^2}
        """
        return 0.5 * self.density * self.velocity ** 2

    def compute_rotation_matrix_wind_to_geometry(self):
        sinalpha = cas.sin(self.alpha * cas.pi / 180)
        cosalpha = cas.cos(self.alpha * cas.pi / 180)
        sinbeta = cas.sin(self.beta * cas.pi / 180)
        cosbeta = cas.cos(self.beta * cas.pi / 180)
        alpharotation = cas.vertcat(cas.horzcat(cosalpha, 0, -sinalpha), cas.horzcat(0, 1, 0), cas.horzcat(sinalpha, 0, cosalpha))
        betarotation = cas.vertcat(cas.horzcat(cosbeta, -sinbeta, 0), cas.horzcat(sinbeta, cosbeta, 0), cas.horzcat(0, 0, 1))
        axesflip = cas.DM([
         [
          -1, 0, 0],
         [
          0, 1, 0],
         [
          0, 0, -1]])
        eye = cas.DM_eye(3)
        r = axesflip @ alpharotation @ betarotation @ eye
        return r

    def compute_freestream_direction_geometry_axes(self):
        vel_dir_wind = cas.DM([-1, 0, 0])
        vel_dir_geometry = self.compute_rotation_matrix_wind_to_geometry() @ vel_dir_wind
        return vel_dir_geometry

    def compute_freestream_velocity_geometry_axes(self):
        return self.compute_freestream_direction_geometry_axes() * self.velocity

    def compute_rotation_velocity_geometry_axes(self, points):
        angular_velocity_vector_geometry_axes = cas.vertcat(-self.p, self.q, -self.r)
        a = angular_velocity_vector_geometry_axes
        b = points
        rotation_velocity_geometry_axes = cas.horzcat(a[1] * b[:, 2] - a[2] * b[:, 1], a[2] * b[:, 0] - a[0] * b[:, 2], a[0] * b[:, 1] - a[1] * b[:, 0])
        rotation_velocity_geometry_axes = -rotation_velocity_geometry_axes
        return rotation_velocity_geometry_axes

    def compute_reynolds(self, reference_length):
        """
        Computes a reynolds number with respect to a given reference length.
        :param reference_length: A reference length you choose [m]
        :return: Reynolds number [unitless]
        """
        return self.density * self.velocity * reference_length / self.viscosity


class AeroData:

    def __init__(self, force_wind_axes=None, force_geometry_axes=None, CL=None, CD=None, CY=None, Cl=None, Cm=None, Cn=None, stability_jacobian=None):
        self.force_wind_axes = force_wind_axes
        self.force_geometry_axes = force_geometry_axes
        self.CL = CL
        self.CD = CD
        self.CY = CY
        self.Cl = Cl
        self.Cm = Cm
        self.Cn = Cn
        self.stability_jacobian = stability_jacobian