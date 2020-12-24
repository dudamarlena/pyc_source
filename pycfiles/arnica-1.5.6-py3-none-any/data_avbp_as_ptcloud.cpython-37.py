# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/duranton/Documents/CERFACS/CODES/arnica/src/arnica/utils/data_avbp_as_ptcloud.py
# Compiled at: 2020-03-30 05:30:51
# Size of source mod 2**32: 4304 bytes
""" module loading avbp h5py into numpy arrays,
limited to point cloud (connectivity sucks, mark my word, really) """
import warnings, h5py, numpy as np
from .vector_actions import renormalize

class AVBPAsPointCloud:
    __doc__ = ' class handling mesh and solutions as point cloud\n    *no connectivity asked* '
    warnings.warn('This tool is deprecated, see the mesh_utils.py tools in pyavbp', DeprecationWarning)

    def __init__(self, meshfile):
        """ startup class"""
        self.mesh = {}
        self.solavg = {}
        self.origins = {}
        self.origins['meshfile'] = meshfile
        self.origins['solavgfile'] = None

    def load_mesh_bulk(self):
        """ load the bulk of the mesh, withound the boundaries """
        with h5py.File(self.origins['meshfile'], 'r') as (fin):
            self.mesh['bulk'] = {}
            self.mesh['bulk']['xyz'] = np.stack((
             fin['/Coordinates/x'][()],
             fin['/Coordinates/y'][()],
             fin['/Coordinates/z'][()]),
              axis=1)

    def load_mesh_bnd(self, patchlist=None):
        """ load only the boundaries. Load all patches,
        unless a subset of patch is provided with opt keyword patchlist """
        with h5py.File(self.origins['meshfile'], 'r') as (fin):
            self.mesh['Patches'] = {}
            patches_readable = fin['/Boundary/PatchLabels'][()]
            bnode_normal = fin['/Boundary/bnode->normal'][()]
            bnode_lidx = fin['/Boundary/bnode_lidx'][()]
            bnode_gnode = fin['/Boundary/bnode->node'][()]
            patches_readable = [pname.decode('UTF-8').strip() for pname in patches_readable if pname is not None]
            if patchlist is None:
                patchlist = patches_readable
            else:
                for patch in patchlist:
                    if patch not in patches_readable:
                        raise IOError('No patch ' + patch + ' among :\n' + '\n'.join(patches_readable))

            for patchlabel in patchlist:
                self.mesh['Patches'][patchlabel] = {}

            for i, patchlabel in enumerate(patches_readable):
                if patchlabel in patchlist:
                    self.mesh['Patches'][patchlabel]['xyz'] = np.stack((
                     fin[('/Patch/' + str(i + 1) + '/Coordinates/x')][()],
                     fin[('/Patch/' + str(i + 1) + '/Coordinates/y')][()],
                     fin[('/Patch/' + str(i + 1) + '/Coordinates/z')][()]),
                      axis=1)
                    shape = self.mesh['Patches'][patchlabel]['xyz'].shape
                    start = 0
                    end = 3 * bnode_lidx[i]
                    if i >= 1:
                        start = 3 * bnode_lidx[(i - 1)]
                    part_bnode_normal = bnode_normal[start:end].reshape(shape)
                    self.mesh['Patches'][patchlabel]['surf'] = np.linalg.norm(part_bnode_normal,
                      axis=(-1))
                    self.mesh['Patches'][patchlabel]['normal'] = renormalize(part_bnode_normal)
                    gnodes = bnode_gnode[int(start / 3):int(end / 3)]
                    self.mesh['Patches'][patchlabel]['gnodes'] = gnodes

    def load_avgsol(self, solavgfile):
        """ load a solution
        AVBP avg for the moment"""
        self.origins['solavgfile'] = solavgfile
        with h5py.File(self.origins['solavgfile'], 'r') as (fin):
            for var in ('T', 'rho', 'u', 'v', 'w'):
                self.solavg[var] = fin[('/Average/' + var)][()]

    def get_skinpts(self, listpatch):
        """ return a dict of numpy array [x, y ,z]
        coordinates of a subset of patches """
        skin = np.concatenate([self.mesh['Patches'][patchlabel]['xyz'] for patchlabel in listpatch])
        return skin