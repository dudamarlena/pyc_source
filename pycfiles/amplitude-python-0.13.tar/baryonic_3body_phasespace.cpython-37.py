# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/amplitf/phasespace/baryonic_3body_phasespace.py
# Compiled at: 2020-03-13 07:22:48
# Size of source mod 2**32: 7195 bytes
import math, numpy as np, tensorflow as tf
import amplitf.interface as atfi
import amplitf.kinematics as atfk
from amplitf.phasespace.dalitz_phasespace import DalitzPhaseSpace
import sys, os
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

class Baryonic3BodyPhaseSpace(DalitzPhaseSpace):
    """Baryonic3BodyPhaseSpace"""

    @atfi.function
    def cos_theta_a(self, sample):
        """
          Return thetaa variable (vector) for the input sample
        """
        return sample[(Ellipsis, 2)]

    @atfi.function
    def phi_a(self, sample):
        """
          Return phia variable (vector) for the input sample
        """
        return sample[(Ellipsis, 3)]

    @atfi.function
    def phi_bc(self, sample):
        """
          Return phibc variable (vector) for the input sample
        """
        return sample[(Ellipsis, 4)]

    @atfi.function
    def inside(self, x):
        """
          Check if the point x=(m2ab, m2bc, cos_theta_a, phi_a, phi_bc) is inside the phase space
        """
        m2ab = self.m2ab(x)
        m2bc = self.m2bc(x)
        mab = atfi.sqrt(m2ab)
        costhetaa = self.cos_theta_a(x)
        phia = self.phi_a(x)
        phibc = self.phi_bc(x)
        inside = tf.logical_and(tf.logical_and(tf.greater(m2ab, self.minab), tf.less(m2ab, self.maxab)), tf.logical_and(tf.greater(m2bc, self.minbc), tf.less(m2bc, self.maxbc)))
        if self.macrange:
            m2ac = self.msqsum - m2ab - m2bc
            inside = tf.logical_and(inside, tf.logical_and(tf.greater(m2ac, self.macrange[0] ** 2), tf.less(m2ac, self.macrange[1] ** 2)))
        if self.symmetric:
            inside = tf.logical_and(inside, tf.greater(m2bc, m2ab))
        eb = (m2ab - self.ma2 + self.mb2) / 2.0 / mab
        ec = (self.md2 - m2ab - self.mc2) / 2.0 / mab
        p2b = eb ** 2 - self.mb2
        p2c = ec ** 2 - self.mc2
        inside = tf.logical_and(inside, tf.logical_and(tf.greater(p2c, 0), tf.greater(p2b, 0)))
        pb = atfi.sqrt(p2b)
        pc = atfi.sqrt(p2c)
        e2bc = (eb + ec) ** 2
        m2bc_max = e2bc - (pb - pc) ** 2
        m2bc_min = e2bc - (pb + pc) ** 2
        inside_phsp = tf.logical_and(inside, tf.logical_and(tf.greater(m2bc, m2bc_min), tf.less(m2bc, m2bc_max)))
        inside_theta = tf.logical_and(tf.greater(costhetaa, -1.0), tf.less(costhetaa, 1.0))
        inside_phi = tf.logical_and(tf.logical_and(tf.greater(phia, -1.0 * math.pi), tf.less(phia, math.pi)), tf.logical_and(tf.greater(phibc, -1.0 * math.pi), tf.less(phibc, math.pi)))
        inside_ang = tf.logical_and(inside_theta, inside_phi)
        return tf.logical_and(inside_phsp, inside_ang)

    @atfi.function
    def filter(self, x):
        return tf.boolean_mask(x, self.inside(x))

    @atfi.function
    def unfiltered_sample(self, size, maximum=None):
        """
          Generate uniform sample of point within phase space.
            size     : number of _initial_ points to generate. Not all of them will fall into phase space,
                       so the number of points in the output will be <size.
            majorant : if majorant>0, add 3rd dimension to the generated tensor which is
                       uniform number from 0 to majorant. Useful for accept-reject toy MC.
        """
        v = [
         tf.random.uniform([size], (self.minab), (self.maxab), dtype=(atfi.fptype())),
         tf.random.uniform([size], (self.minbc), (self.maxbc), dtype=(atfi.fptype())),
         tf.random.uniform([size], (-1.0), 1.0, dtype=(atfi.fptype())),
         tf.random.uniform([size], (-1.0 * math.pi), (math.pi), dtype=(atfi.fptype())),
         tf.random.uniform([size], (-1.0 * math.pi), (math.pi), dtype=(atfi.fptype()))]
        if maximum is not None:
            v += [tf.random.uniform([size], 0.0, maximum, dtype=(atfi.fptype()))]
        return tf.stack(v, axis=1)

    @atfi.function
    def final_state_momenta(self, m2ab, m2bc, costhetaa, phia, phibc):
        """
          Calculate 4-momenta of final state tracks in the 5D phase space
            m2ab, m2bc : invariant masses of AB and BC combinations
            (cos)thetaa, phia : direction angles of the particle A in the D reference frame
            phibc : angle of BC plane wrt. polarisation plane z x p_a
        """
        thetaa = atfi.acos(costhetaa)
        m2ac = self.msqsum - m2ab - m2bc
        p_a = atfk.two_body_momentum(self.md, self.ma, atfi.sqrt(m2bc))
        p_b = atfk.two_body_momentum(self.md, self.mb, atfi.sqrt(m2ac))
        p_c = atfk.two_body_momentum(self.md, self.mc, atfi.sqrt(m2ab))
        cos_theta_b = (p_a * p_a + p_b * p_b - p_c * p_c) / (2.0 * p_a * p_b)
        cos_theta_c = (p_a * p_a + p_c * p_c - p_b * p_b) / (2.0 * p_a * p_c)
        p3a = atfk.vector(atfi.zeros(p_a), atfi.zeros(p_a), p_a)
        p3b = atfk.vector(p_b * Sqrt(1.0 - cos_theta_b ** 2), atfi.zeros(p_b), -p_b * cos_theta_b)
        p3c = atfk.vector(-p_c * Sqrt(1.0 - cos_theta_c ** 2), atfi.zeros(p_c), -p_c * cos_theta_c)
        p3a = atfk.rotate_euler(p3a, atfi.const(0.0), thetaa, atfi.const(0.0))
        p3b = atfk.rotate_euler(p3b, atfi.const(0.0), thetaa, atfi.const(0.0))
        p3c = atfk.rotate_euler(p3c, atfi.const(0.0), thetaa, atfi.const(0.0))
        p3a = atfk.rotate_euler(p3a, phia, atfi.const(0.0), atfi.const(0.0))
        p3b = atfk.rotate_euler(p3b, phia, atfi.const(0.0), atfi.const(0.0))
        p3c = atfk.rotate_euler(p3c, phia, atfi.const(0.0), atfi.const(0.0))
        p3b = atfk.rotate(p3b, phibc, p3a)
        p3c = atfk.rotate(p3c, phibc, p3a)
        p4a = atfk.lorentz_vector(p3a, atfi.sqrt(p_a ** 2 + self.ma2))
        p4b = atfk.lorentz_vector(p3b, atfi.sqrt(p_b ** 2 + self.mb2))
        p4c = atfk.lorentz_vector(p3c, atfi.sqrt(p_c ** 2 + self.mc2))
        return (
         p4a, p4b, p4c)

    def dimensionality(self):
        return 5