# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tal/Dropbox/Code/neurosynth/neurosynth/base/transformations.py
# Compiled at: 2015-08-10 12:21:28
# Size of source mod 2**32: 2645 bytes
""" Various transformations between coordinate frames, atlas spaces, etc. """
import numpy as np
from numpy import linalg
import logging
logger = logging.getLogger('neurosynth.transformations')

def transform(foci, mat):
    """ Convert coordinates from one space to another using provided
    transformation matrix. """
    t = linalg.pinv(mat)
    foci = np.hstack((foci, np.ones((foci.shape[0], 1))))
    return np.dot(foci, t)[:, 0:3]


def xyz_to_mat(foci, xyz_dims=None, mat_dims=None):
    """ Convert an N x 3 array of XYZ coordinates to matrix indices. """
    foci = np.hstack((foci, np.ones((foci.shape[0], 1))))
    mat = np.array([[-0.5, 0, 0, 45], [0, 0.5, 0, 63], [0, 0, 0.5, 36]]).T
    result = np.dot(foci, mat)[:, ::-1]
    return np.round_(result).astype(int)


def mat_to_xyz(foci, mat_dims=None, xyz_dims=None):
    """ Convert an N x 3 array of matrix indices to XYZ coordinates. """
    foci = np.hstack((foci, np.ones((foci.shape[0], 1))))
    mat = np.array([[-2, 0, 0, 90], [0, 2, 0, -126], [0, 0, 2, -72]]).T
    result = np.dot(foci, mat)[:, ::-1]
    return np.round_(result).astype(int)


def t88_to_mni():
    """ Convert Talairach to MNI coordinates using the Lancaster transform.
    Adapted from BrainMap scripts; see http://brainmap.org/icbm2tal/
    Details are described in Lancaster et al. (2007)
    (http://brainmap.org/new/pubs/LancasterHBM07.pdf). """
    return np.array([[0.9254, 0.0024, -0.0118, -1.0207],
     [
      -0.0048, 0.9316, -0.0871, -1.7667],
     [
      0.0152, 0.0883, 0.8924, 4.0926],
     [
      0.0, 0.0, 0.0, 1.0]]).T


class Transformer(object):
    __doc__ = ' The Transformer class supports transformations between different\n    image spaces. '

    def __init__(self, transforms=None, target='MNI'):
        """ Initialize a transformer instance. """
        self.target = target
        self.transformations = transforms

    def add(self, name, mat):
        """ Add a named linear transformation. """
        self.transformations[name] = mat

    def apply(self, name, foci):
        """ Apply a named transformation to a set of foci.

        If the named transformation doesn't exist, return foci untransformed.
        """
        if name in self.transformations:
            return transform(foci, self.transformations[name])
        else:
            logger.info("No transformation named '%s' found; coordinates left untransformed." % name)
            return foci