# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/genmechanics/linkages.py
# Compiled at: 2020-03-26 14:17:33
# Size of source mod 2**32: 21703 bytes
"""
Created on Wed Nov 16 13:14:34 2016

@author: Steven Masfaraud
"""
import numpy as npy
from math import cos, sin
import genmechanics.geometry as geometry

class Linkage:

    def __init__(self, part1, part2, position, euler_angles, static_matrix1, static_matrix2, static_behavior_occurence_matrix, static_behavior_nonlinear_eq_indices, static_behavior_linear_eq, static_behavior_nonlinear_eq, static_require_kinematic, name=''):
        self.part1 = part1
        self.part2 = part2
        self.position = npy.array(position)
        self.euler_angles = euler_angles
        self.name = name
        self.static_matrix1 = static_matrix1
        self.static_matrix2 = static_matrix2
        self.static_behavior_occurence_matrix = static_behavior_occurence_matrix
        self.static_behavior_nonlinear_eq_indices = static_behavior_nonlinear_eq_indices
        self.static_behavior_linear_eq = static_behavior_linear_eq
        self.static_behavior_nonlinear_eq = static_behavior_nonlinear_eq
        self.static_require_kinematic = static_require_kinematic
        self.n_static_unknowns = static_matrix1.shape[1]
        self.P = (geometry.Euler2TransferMatrix)(*self.euler_angles)

    def Babylon(self, length, forces, torques):
        xa, za, ya = self.P[:, 0]
        x, z, y = self.position
        s = '\n        var sphere = BABYLON.Mesh.CreateSphere("{} center", 8, {}, scene);\n        sphere.position=new BABYLON.Vector3({},{},{});    \n        var lineX = BABYLON.Mesh.CreateDashedLines("{} axis", [\n            new BABYLON.Vector3({}, {}, {}),\n            new BABYLON.Vector3({}, {}, {})\n        ],0.05,0.05,10, scene);\n        '.format(self.name, length / 30, x, y, z, self.name, x - 0.5 * xa, y - 0.5 * ya, z - 0.5 * za, x + 0.5 * xa, y + 0.5 * ya, z + 0.5 * za)
        if forces is not None:
            s += 'var lineF = BABYLON.Mesh.CreateLines("{} axis", [\n            new BABYLON.Vector3({}, {}, {}),\n            new BABYLON.Vector3({}, {}, {})\n        ], scene);\n            lineF.color=new BABYLON.Color3(1,0,0);'.format('force {}'.format(self.name), x, y, z, x + forces[0], y + forces[1], z + forces[2])
        return s


class HolonomicLinkage(Linkage):
    holonomic = True

    def __init__(self, part1, part2, position, euler_angles, static_matrix1, static_matrix2, static_behavior_occurence_matrix, static_behavior_nonlinear_eq_indices, static_behavior_linear_eq, static_behavior_nonlinear_eq, kinematic_matrix, static_require_kinematic=False, name=''):
        Linkage.__init__(self, part1, part2, position, euler_angles, static_matrix1, static_matrix2, static_behavior_occurence_matrix, static_behavior_nonlinear_eq_indices, static_behavior_linear_eq, static_behavior_nonlinear_eq, static_require_kinematic, name)
        self.kinematic_matrix = kinematic_matrix
        self.n_kinematic_unknowns = kinematic_matrix.shape[1]


class NonHolonomicLinkage(Linkage):
    holonomic = False

    def __init__(self, part1, part2, position, euler_angles, static_matrix1, static_matrix2, static_behavior_occurence_matrix, static_behavior_nonlinear_eq_indices, static_behavior_linear_eq, static_behavior_nonlinear_eq, kinematic_directions, static_require_kinematic=False, name=''):
        Linkage.__init__(self, part1, part2, position, euler_angles, static_matrix1, static_matrix2, static_behavior_occurence_matrix, static_behavior_nonlinear_eq_indices, static_behavior_linear_eq, static_behavior_nonlinear_eq, static_require_kinematic, name)
        self.kinematic_directions = kinematic_directions


class FrictionlessRevoluteLinkage(HolonomicLinkage):

    def __init__(self, part1, part2, position, euler_angles, name='Frictionless Revolute Linkage'):
        static_matrix2 = npy.array([[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]])
        static_matrix1 = -static_matrix2
        static_behavior_occurence_matrix = npy.array([])
        static_behavior_nonlinear_eq_indices = []
        static_behavior_linear_eq = npy.array([])
        static_behavior_nonlinear_eq = []
        kinematic_matrix = npy.array([[1], [0], [0], [0], [0], [0]])
        static_require_kinematic = False
        HolonomicLinkage.__init__(self, part1, part2, position, euler_angles, static_matrix1, static_matrix2, static_behavior_occurence_matrix, static_behavior_nonlinear_eq_indices, static_behavior_linear_eq, static_behavior_nonlinear_eq, kinematic_matrix, static_require_kinematic, name)


class RevoluteLinkage(HolonomicLinkage):

    def __init__(self, part1, part2, position, euler_angles, Ca, Cr, Cw, name='Revolute Linkage'):
        self.Ca = Ca
        self.Cr = Cr
        self.Cw = Cw
        static_matrix2 = npy.array([[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]])
        static_matrix1 = -static_matrix2
        static_behavior_occurence_matrix = npy.array([[1, 1, 1, 1, 0, 0]])
        static_behavior_nonlinear_eq_indices = [0]
        static_behavior_linear_eq = npy.array([])
        static_behavior_nonlinear_eq = [
         lambda x, w, v:          if w[0] != 0:
abs(w[0]) / w[0] * (Ca * abs(x[0]) + Cr * (x[1] ** 2 + x[2] ** 2) ** 0.5 + Cw * w[0]) + x[3] # Avoid dead code: x[3]]
        kinematic_matrix = npy.array([[1], [0], [0], [0], [0], [0]])
        static_require_kinematic = True
        HolonomicLinkage.__init__(self, part1, part2, position, euler_angles, static_matrix1, static_matrix2, static_behavior_occurence_matrix, static_behavior_nonlinear_eq_indices, static_behavior_linear_eq, static_behavior_nonlinear_eq, kinematic_matrix, static_require_kinematic, name)

    def ChangeCoefficients(self, Ca, Cr, Cw):
        self.Ca = Ca
        self.Cr = Cr
        self.Cw = Cw
        self.static_behavior_nonlinear_eq = [
         lambda x, w, v:          if w[0] != 0:
abs(w[0]) / w[0] * (Ca * abs(x[0]) + Cr * (x[1] ** 2 + x[2] ** 2) ** 0.5 + Cw * w[0]) + x[3] # Avoid dead code: x[3]]


class FrictionlessBallLinkage(HolonomicLinkage):

    def __init__(self, part1, part2, position, euler_angles, name=''):
        static_matrix2 = npy.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
        static_matrix1 = -static_matrix2
        static_behavior_occurence_matrix = npy.array([])
        static_behavior_nonlinear_eq_indices = []
        static_behavior_linear_eq = npy.array([])
        static_behavior_nonlinear_eq = []
        kinematic_matrix = npy.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
        static_require_kinematic = False
        HolonomicLinkage.__init__(self, part1, part2, position, euler_angles, static_matrix1, static_matrix2, static_behavior_occurence_matrix, static_behavior_nonlinear_eq_indices, static_behavior_linear_eq, static_behavior_nonlinear_eq, kinematic_matrix, static_require_kinematic, name)


class FrictionlessLinearAnnularLinkage(HolonomicLinkage):

    def __init__(self, part1, part2, position, euler_angles, name='Frictionless Linear Annular Linkage'):
        static_matrix2 = npy.array([[0, 0], [1, 0], [0, 1], [0, 0], [0, 0], [0, 0]])
        static_matrix1 = -static_matrix2
        static_behavior_occurence_matrix = npy.array([])
        static_behavior_nonlinear_eq_indices = []
        static_behavior_linear_eq = npy.array([])
        static_behavior_nonlinear_eq = []
        kinematic_matrix = npy.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0]])
        static_require_kinematic = False
        HolonomicLinkage.__init__(self, part1, part2, position, euler_angles, static_matrix1, static_matrix2, static_behavior_occurence_matrix, static_behavior_nonlinear_eq_indices, static_behavior_linear_eq, static_behavior_nonlinear_eq, kinematic_matrix, static_require_kinematic, name)


class BallLinkage(HolonomicLinkage):

    def __init__(self, part1, part2, position, euler_angles, Ca, Cr, Cw, name='Ball Linkage'):
        self.Ca = Ca
        self.Cr = Cr
        self.Cw = Cw
        static_matrix2 = npy.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0]])
        static_matrix1 = -static_matrix2
        static_behavior_occurence_matrix = npy.array([[1, 1, 1, 1]])
        static_behavior_nonlinear_eq_indices = [0]
        static_behavior_linear_eq = npy.array([])
        static_behavior_nonlinear_eq = [
         lambda x, w, v:          if w[0] != 0:
abs(w[0]) / w[0] * (Ca * abs(x[0]) + Cr * (x[1] ** 2 + x[2] ** 2) ** 0.5 + Cw * w[0]) + x[3] # Avoid dead code: x[3]]
        kinematic_matrix = npy.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
        static_require_kinematic = True
        HolonomicLinkage.__init__(self, part1, part2, position, euler_angles, static_matrix1, static_matrix2, static_behavior_occurence_matrix, static_behavior_nonlinear_eq_indices, static_behavior_linear_eq, static_behavior_nonlinear_eq, kinematic_matrix, static_require_kinematic, name)

    def ChangeCoefficients(self, Ca, Cr, Cw):
        self.Ca = Ca
        self.Cr = Cr
        self.Cw = Cw
        self.static_behavior_nonlinear_eq = [
         lambda x, w, v:          if w[0] != 0:
abs(w[0]) / w[0] * (Ca * abs(x[0]) + Cr * (x[1] ** 2 + x[2] ** 2) ** 0.5 + Cw * w[0]) + x[3] # Avoid dead code: x[3]]


class LinearAnnularLinkage(HolonomicLinkage):

    def __init__(self, part1, part2, position, euler_angles, Cr, Cw, name='Linear Annular Linkage'):
        self.Cr = Cr
        self.Cw = Cw
        static_matrix2 = npy.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, 0], [0, 0, 0]])
        static_matrix1 = -static_matrix2
        static_behavior_occurence_matrix = npy.array([[1, 1, 1]])
        static_behavior_nonlinear_eq_indices = [0]
        static_behavior_linear_eq = npy.array([])
        static_behavior_nonlinear_eq = [
         lambda x, w, v:          if w[0] != 0:
abs(w[0]) / w[0] * (Cr * (w[0] ** 2 + x[1] ** 2) ** 0.5 + Cw * w[0]) + x[2] # Avoid dead code: x[2]]
        kinematic_matrix = npy.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0]])
        static_require_kinematic = True
        HolonomicLinkage.__init__(self, part1, part2, position, euler_angles, static_matrix1, static_matrix2, static_behavior_occurence_matrix, static_behavior_nonlinear_eq_indices, static_behavior_linear_eq, static_behavior_nonlinear_eq, kinematic_matrix, static_require_kinematic, name)

    def ChangeCoefficients(self, Cr, Cw):
        self.Cr = Cr
        self.Cw = Cw
        self.static_behavior_nonlinear_eq = [
         lambda x, w, v:          if w[0] != 0:
abs(w[0]) / w[0] * (Cr * (w[0] ** 2 + x[1] ** 2) ** 0.5 + Cw * w[0]) + x[2] # Avoid dead code: x[2]]


class RotationalStop(HolonomicLinkage):

    def __init__(self, part1, part2, position, euler_angles, name='Rotational Stop'):
        static_matrix2 = npy.array([[0], [0], [0], [1], [0], [0]])
        static_matrix1 = -static_matrix2
        static_behavior_occurence_matrix = npy.array([])
        static_behavior_nonlinear_eq_indices = []
        static_behavior_linear_eq = npy.array([])
        static_behavior_nonlinear_eq = []
        kinematic_matrix = npy.array([[0, 0, 0, 0, 0], [1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]])
        static_require_kinematic = True
        HolonomicLinkage.__init__(self, part1, part2, position, euler_angles, static_matrix1, static_matrix2, static_behavior_occurence_matrix, static_behavior_nonlinear_eq_indices, static_behavior_linear_eq, static_behavior_nonlinear_eq, kinematic_matrix, static_require_kinematic, name)


class FrictionLessGearSetLinkage(NonHolonomicLinkage):
    __doc__ = '\n    :param alpha: pressure angle\n    :param beta: helix angle\n    '

    def __init__(self, part1, part2, position, euler_angles, alpha, beta, name='Gear Set Linkage'):
        self.alpha = alpha
        self.beta = beta
        static_matrix2 = npy.array([[cos(beta) * cos(alpha), 0], [sin(beta), 0], [0, -1], [0, 0], [0, 0], [0, 0]])
        static_matrix1 = -static_matrix2
        static_behavior_occurence_matrix = npy.array([[1, 1]])
        static_behavior_nonlinear_eq_indices = [0]
        static_behavior_linear_eq = npy.array([])
        static_behavior_nonlinear_eq = [lambda x, w, v: abs(sin(beta) * cos(alpha) * abs(x[0])) + x[1]]
        directions = [npy.array([1, 0, 0])]
        static_require_kinematic = True
        NonHolonomicLinkage.__init__(self, part1, part2, position, euler_angles, static_matrix1, static_matrix2, static_behavior_occurence_matrix, static_behavior_nonlinear_eq_indices, static_behavior_linear_eq, static_behavior_nonlinear_eq, directions, static_require_kinematic, name)

    def ChangeParameters(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.static_matrix2 = npy.array([[cos(beta) * cos(alpha), 0, 0], [sin(beta), 0, 0], [0, 0, -1], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.static_matrix1 = npy.array([[0, cos(beta) * cos(alpha), 0], [0, sin(beta), 0], [0, 0, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.static_behavior_nonlinear_eq = [lambda x, w, v: abs(sin(beta) * cos(alpha) * abs(x[0])) + x[1]]


class GearSetLinkage(NonHolonomicLinkage):
    __doc__ = '\n    :param alpha: pressure angle\n    :param beta: helix angle\n    '

    def __init__(self, part1, part2, position, euler_angles, alpha, beta, Cf, Cv, name='Gear Set Linkage'):
        self.alpha = alpha
        self.beta = beta
        self.Cf = Cf
        self.Cv = Cv
        static_matrix2 = npy.array([[cos(beta) * cos(alpha), 0, 0], [sin(beta), 0, 0], [0, 0, -1], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
        static_matrix1 = npy.array([[0, cos(beta) * cos(alpha), 0], [0, sin(beta), 0], [0, 0, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
        static_behavior_occurence_matrix = npy.array([[1, 1, 1], [1, 1, 0]])
        static_behavior_nonlinear_eq_indices = [0, 1]
        static_behavior_linear_eq = npy.array([])
        static_behavior_nonlinear_eq = self.UpdateBehavior()
        directions = [
         npy.array([1, 0, 0])]
        static_require_kinematic = True
        NonHolonomicLinkage.__init__(self, part1, part2, position, euler_angles, static_matrix1, static_matrix2, static_behavior_occurence_matrix, static_behavior_nonlinear_eq_indices, static_behavior_linear_eq, static_behavior_nonlinear_eq, directions, static_require_kinematic, name)

    def UpdateBehavior(self):
        f1 = lambda x, w, v: abs(sin(self.beta) * cos(self.alpha) * max(abs(x[0]), abs(x[1]))) + x[2]

        def f2(x, w, v):
            if x[0] == 0.0:
                if v[0] * x[1] > 0:
                    r = x[1] - x[0] * (self.Cf * (1 + sin(self.beta) ** 2 * cos(self.alpha) ** 2) ** 0.5 - 1) + self.Cv * abs(v[0])
                else:
                    r = x[0] - x[1] * (self.Cf * (1 + sin(self.beta) ** 2 * cos(self.alpha) ** 2) ** 0.5 - 1) + self.Cv * abs(v[0])
            else:
                if v[0] * x[0] < 0:
                    r = x[1] - x[0] * (self.Cf * (1 + sin(self.beta) ** 2 * cos(self.alpha) ** 2) ** 0.5 - 1) + self.Cv * abs(v[0])
                else:
                    r = x[0] - x[1] * (self.Cf * (1 + sin(self.beta) ** 2 * cos(self.alpha) ** 2) ** 0.5 - 1) + self.Cv * abs(v[0])
            return r

        return [
         f1, f2]

    def ChangeCoefficients(self, Cf, Cv):
        self.Cf = Cf
        self.Cv = Cv
        self.static_behavior_nonlinear_eq = self.UpdateBehavior()

    def ChangeParameters(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        self.static_matrix2 = npy.array([[cos(beta) * cos(alpha), 0, 0], [sin(beta), 0, 0], [0, 0, -1], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.static_matrix1 = npy.array([[0, cos(beta) * cos(alpha), 0], [0, sin(beta), 0], [0, 0, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.static_behavior_nonlinear_eq = self.UpdateBehavior()


class FrictionlessGearSetLinkage(NonHolonomicLinkage):
    __doc__ = '\n    :param alpha: pressure angle\n    :param beta: helix angle\n    '

    def __init__(self, part1, part2, position, euler_angles, alpha, beta, name='Gear Set Linkage'):
        self.alpha = alpha
        self.beta = beta
        static_matrix2 = npy.array([[cos(beta) * cos(alpha), 0], [sin(beta), 0], [0, -1], [0, 0], [0, 0], [0, 0]])
        static_matrix1 = -static_matrix2
        static_behavior_occurence_matrix = npy.array([[1, 1, 1]])
        static_behavior_nonlinear_eq_indices = [0]
        static_behavior_linear_eq = npy.array([])
        static_behavior_nonlinear_eq = [lambda x, w, v: abs(sin(beta) * cos(alpha) * abs(x[0])) + x[1]]
        directions = [npy.array([1, 0, 0])]
        static_require_kinematic = True
        NonHolonomicLinkage.__init__(self, part1, part2, position, euler_angles, static_matrix1, static_matrix2, static_behavior_occurence_matrix, static_behavior_nonlinear_eq_indices, static_behavior_linear_eq, static_behavior_nonlinear_eq, directions, static_require_kinematic, name)