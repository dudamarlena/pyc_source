# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mpol/datasets.py
# Compiled at: 2020-02-03 01:02:18
# Size of source mod 2**32: 4355 bytes
import numpy as np, torch
from torch.utils.data import Dataset
import mpol
from mpol.constants import *

class UVDataset(Dataset):
    __doc__ = '\n    Container for interferometric visibilities.\n\n    Args:\n        uu (2d numpy array): (nchan, nvis) length array of u spatial frequency coordinates. Units of [:math:`\\mathrm{k}\\lambda`]  \n        vv (2d numpy array): (nchan, nvis) length array of v spatial frequency coordinates. Units of [:math:`\\mathrm{k}\\lambda`]  \n        data_re (2d numpy array): (nchan, nvis) length array of the real part of the visibility measurements. Units of [:math:`\\mathrm{Jy}`]\n        data_im (2d numpy array): (nchan, nvis) length array of the imaginary part of the visibility measurements. Units of [:math:`\\mathrm{Jy}`]\n        weights (2d numpy array): (nchan, nvis) length array of thermal weights. Units of [:math:`1/\\mathrm{Jy}^2`]\n        cell_size (float): the image pixel size in arcsec. Defaults to None, but if both `cell_size` and `npix` are set, the visibilities will be pre-gridded to the RFFT output dimensions.\n        npix (int): the number of pixels per image side (square images only). Defaults to None, but if both `cell_size` and `npix` are set, the visibilities will be pre-gridded to the RFFT output dimensions.\n        device (torch.device) : the desired device of the dataset. If ``None``, defalts to current device.\n    \n    If both `cell_size` and `npix` are set, the dataset will be automatically pre-gridded to the RFFT output grid. This will greatly speed up performance.\n\n    If you have just a single channel, you can pass 1D numpy arrays for `uu`, `vv`, `weights`, `data_re`, and `data_im` and they will automatically be promoted to 2D with a leading dimension of 1 (i.e., ``nchan=1``).\n    '

    def __init__(self, uu=None, vv=None, data_re=None, data_im=None, weights=None, cell_size=None, npix=None, device=None, **kwargs):
        shape = uu.shape
        for a in [vv, weights, data_re, data_im]:
            assert a.shape == shape, 'All dataset inputs must be the same shape.'

        if len(shape) == 1:
            uu = np.atleast_2d(uu)
            vv = np.atleast_2d(vv)
            data_re = np.atleast_2d(data_re)
            data_im = np.atleast_2d(data_im)
            weights = np.atleast_2d(weights)
        if cell_size is not None and npix is not None:
            self.cell_size = cell_size * arcsec
            self.npix = npix
            uu_grid, vv_grid, grid_mask, g_weights, g_re, g_im = mpol.gridding.grid_dataset(uu,
              vv,
              weights,
              data_re,
              data_im,
              (self.cell_size / arcsec),
              npix=(self.npix))
            self.uu = torch.tensor(uu_grid, device=device)
            self.vv = torch.tensor(vv_grid, device=device)
            self.grid_mask = torch.tensor(grid_mask, dtype=(torch.bool), device=device)
            self.weights = torch.tensor(g_weights, device=device)
            self.re = torch.tensor(g_re, device=device)
            self.im = torch.tensor(g_im, device=device)
            self.gridded = True
        else:
            self.gridded = False
            self.uu = torch.tensor(uu, dtype=(torch.double), device=device)
            self.vv = torch.tensor(vv, dtype=(torch.double), device=device)
            self.weights = torch.tensor(weights,
              dtype=(torch.double), device=device)
            self.re = torch.tensor(data_re, dtype=(torch.double), device=device)
            self.im = torch.tensor(data_im, dtype=(torch.double), device=device)

    def __getitem__(self, index):
        return (
         self.uu[index],
         self.vv[index],
         self.weights[index],
         self.re[index],
         self.im[index])

    def __len__(self):
        return len(self.uu)