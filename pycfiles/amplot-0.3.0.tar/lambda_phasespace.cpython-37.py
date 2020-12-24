# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/amplitf/phasespace/lambda_phasespace.py
# Compiled at: 2020-03-13 07:22:48
# Size of source mod 2**32: 2805 bytes
import math, numpy as np, tensorflow as tf
import amplitf.interface as atfi
import sys, os
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

class LambdaPhaseSpace:
    """LambdaPhaseSpace"""

    def __init__(self, phsp, func):
        self.phsp = phsp
        self.func = func

    def dimensionality(self):
        return self.phsp.dimensionality()

    def inside(self, x):
        return tf.logical_and(self.phsp.inside(x), self.func(x))

    def filter(self, x):
        y = tf.boolean_mask(x, self.func(x))
        return tf.boolean_mask(y, self.phsp.inside(y))

    def unfiltered_sample(self, size, maximum=None):
        """
          Generate uniform sample of point within phase space. 
            size     : number of _initial_ points to generate. Not all of them will fall into phase space, 
                       so the number of points in the output will be <size. 
            maximum  : if majorant>0, add 3rd dimension to the generated tensor which is
                       uniform number from 0 to majorant. Useful for accept-reject toy MC. 
        """
        return self.phsp.unfiltered_sample(size, maximum)

    def uniform_sample(self, size, maximum=None):
        """
          Generate uniform sample of point within phase space. 
            size     : number of _initial_ points to generate. Not all of them will fall into phase space, 
                       so the number of points in the output will be <size. 
            maximum  : if majorant>0, add 3rd dimension to the generated tensor which is
                       uniform number from 0 to majorant. Useful for accept-reject toy MC. 
          Note it does not actually generate the sample, but returns the data flow graph for generation, 
          which has to be run within TF session. 
        """
        return self.filter(self.unfiltered_sample(size, maximum))

    def bounds(self):
        return self.phsp.bounds()