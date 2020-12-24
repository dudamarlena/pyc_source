# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/amplitf/phasespace/four_body_angular_phasespace.py
# Compiled at: 2020-03-13 07:22:48
# Size of source mod 2**32: 5014 bytes
import math, numpy as np, tensorflow as tf
import amplitf.interface as atfi
import sys, os
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

class FourBodyAngularPhaseSpace:
    """FourBodyAngularPhaseSpace"""

    def __init__(self):
        """
        Constructor
        """
        pass

    @atfi.function
    def inside(self, x):
        """
          Check if the point x=(cos_theta_1, cos_theta_2, phi) is inside the phase space
        """
        cos1 = self.cos_theta1(x)
        cos2 = self.cos_theta2(x)
        phi = self.phi(x)
        inside = tf.logical_and(tf.logical_and(tf.greater(cos1, -1.0), tf.less(cos1, 1.0)), tf.logical_and(tf.greater(cos2, -1.0), tf.less(cos2, 1.0)))
        inside = tf.logical_and(inside, tf.logical_and(tf.greater(phi, 0.0), tf.less(phi, 2.0 * math.pi)))
        return inside

    @atfi.function
    def filter(self, x):
        return tf.boolean_mask(x, self.inside(x))

    @atfi.function
    def unfiltered_sample(self, size, maximum=None):
        """
          Return TF graph for uniform sample of point within phase space.
            size     : number of _initial_ points to generate. Not all of them will fall into phase space,
                       so the number of points in the output will be <size.
            majorant : if majorant>0, add 3rd dimension to the generated tensor which is
                       uniform number from 0 to majorant. Useful for accept-reject toy MC.
        """
        v = [
         tf.random.uniform([size], (-1.0), 1.0, dtype=(atfi.fptype())),
         tf.random.uniform([size], (-1.0), 1.0, dtype=(atfi.fptype())),
         tf.random.uniform([size], 0.0, (2.0 * math.pi), dtype=(atfi.fptype()))]
        if maximum is not None:
            v += [tf.random.uniform([size], 0.0, maximum, dtype=(atfi.fptype()))]
        return tf.stack(v, axis=1)

    @atfi.function
    def uniform_sample(self, size, maximum=None):
        """
          Generate uniform sample of point within phase space.
            size     : number of _initial_ points to generate. Not all of them will fall into phase space,
                       so the number of points in the output will be <size.
            majorant : if majorant>0, add 3rd dimension to the generated tensor which is
                       uniform number from 0 to majorant. Useful for accept-reject toy MC.
          Note it does not actually generate the sample, but returns the data flow graph for generation,
          which has to be run within TF session.
        """
        return self.filter(self.unfiltered_sample(size, maximum))

    @atfi.function
    def rectangular_grid_sample(self, size_cos_theta1, size_cos_theta2, size_phi):
        """
          Create a data sample in the form of rectangular grid of points within the phase space.
          Useful for normalisation.
        """
        size = size_cos_theta1 * size_cos_theta2 * size_phi
        mgrid = np.lib.index_tricks.nd_grid()
        v1 = mgrid[0:size_cos_theta1, 0:size_cos_theta2, 0:size_phi][0] * 2.0 / float(size_cos_theta1) - 1.0
        v2 = mgrid[0:size_cos_theta1, 0:size_cos_theta2, 0:size_phi][1] * 2.0 / float(size_cos_theta2) - 1.0
        v3 = mgrid[0:size_cos_theta1, 0:size_cos_theta2, 0:size_phi][2] * 2.0 * math.pi / float(size_phi)
        v = [v1.reshape(size).astype('d'),
         v2.reshape(size).astype('d'), v3.reshape(size).astype('d')]
        x = tf.stack(v, axis=1)
        return tf.boolean_mask(x, self.inside(x))

    @atfi.function
    def cos_theta1(self, sample):
        """
          Return cos_theta1 variable (vector) for the input sample
        """
        return sample[(Ellipsis, 0)]

    @atfi.function
    def cos_theta2(self, sample):
        """
          Return cos_theta2 variable (vector) for the input sample
        """
        return sample[(Ellipsis, 1)]

    @atfi.function
    def phi(self, sample):
        """
          Return phi variable (vector) for the input sample
        """
        return sample[(Ellipsis, 2)]

    def dimensionality(self):
        return 3