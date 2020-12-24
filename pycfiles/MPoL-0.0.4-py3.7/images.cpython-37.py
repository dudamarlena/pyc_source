# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mpol/images.py
# Compiled at: 2020-02-03 01:02:18
# Size of source mod 2**32: 12343 bytes
"""
The ``images`` module provides the core functionality of MPoL via :class:`mpol.images.ImageCube`.
"""
import numpy as np, torch
from torch import nn
from mpol import gridding
from mpol.constants import *
import mpol.utils

class ImageCube(nn.Module):
    __doc__ = '\n    A PyTorch layer that provides a parameter set and transformations to model interferometric visibilities.\n\n    The parameter set is the pixel values of the image cube itself. The transformations are the real fast Fourier transform (RFFT) and band-limited interpolation routines. The pixels are assumed to represent samples of the specific intensity and are given in units of [:math:`\\mathrm{Jy}\\,\\mathrm{arcsec}^{-2}`].\n\n    All keyword arguments are required unless noted.\n\n    Args:\n        npix (int): the number of pixels per image side\n        nchan (int): the number of channels in the image\n        cell_size (float): the width of a pixel [arcseconds]\n        cube (torch.double tensor, optional): an image cube to initialize the model with. If None, assumes starting ``cube`` is ``torch.zeros``. \n    '

    def __init__(self, npix=None, nchan=None, cell_size=None, cube=None, **kwargs):
        super().__init__()
        if not npix % 2 == 0:
            raise AssertionError('npix must be even (for now)')
        else:
            self.npix = int(npix)
            assert cell_size > 0.0, 'cell_size must be positive (arcseconds)'
            self.cell_size = cell_size * arcsec
            assert nchan > 0, 'must have a positive number of channels'
            self.nchan = int(nchan)
            img_radius = self.cell_size * (self.npix // 2)
            self.us = np.fft.rfftfreq((self.npix), d=(self.cell_size)) * 0.001
            self.vs = np.fft.fftfreq((self.npix), d=(self.cell_size)) * 0.001
            self._us_2D, self._vs_2D = np.meshgrid((self.us), (self.vs), indexing='xy')
            self._qs_2D = np.sqrt(self._us_2D ** 2 + self._vs_2D ** 2)
            self.us_2D = np.fft.fftshift((self._us_2D), axes=0)
            self.vs_2D = np.fft.fftshift((self._vs_2D), axes=0)
            self.qs_2D = np.fft.fftshift((self._qs_2D), axes=0)
            if cube is None:
                self._cube = nn.Parameter(torch.zeros((self.nchan),
                  (self.npix),
                  (self.npix),
                  requires_grad=True,
                  dtype=(torch.double)))
            else:
                flipped = torch.flip(cube, (2, ))
            shifted = mpol.utils.fftshift(flipped, axes=(1, 2))
            self._cube = nn.Parameter(shifted)
        self._ll = np.flip(np.fft.ifftshift(gridding.fftspace(img_radius, self.npix)))
        self._mm = np.fft.ifftshift(gridding.fftspace(img_radius, self.npix))
        self.corrfun = torch.tensor(gridding.corrfun_mat(self._ll, self._mm))
        self.precached = False

    def precache_interpolation(self, dataset):
        """
        Cache the interpolation matrices used to interpolate the output from the RFFT to the measured :math:`(u,v)` points. This is only applicable if the dataset has not been pre-gridded, and will be run automatically upon the first call to :meth:`mpol.ImageCube.forward`.

        Stores the attributes ``C_res`` and ``C_ims``, which are lists of sparse interpolation matrices corresponding to each channel.

        Args:
            dataset (UVDataset): a UVDataset containing the :math:`(u,v)` sampling points of the observation.

        Returns:
            None
            
            
        """
        max_baseline = torch.max(torch.abs(torch.cat([dataset.uu, dataset.vv])))
        assert max_baseline < 0.001 / (2 * self.cell_size), 'Image cell size is too coarse to represent the largest spatial frequency sampled by the dataset. Make a finer image by decreasing cell_size. You may also need to increase npix to make sure the image remains wide enough to capture all of the emission and avoid aliasing.'
        uu = dataset.uu.detach().cpu().numpy()
        vv = dataset.vv.detach().cpu().numpy()
        self.C_res = []
        self.C_ims = []
        for i in range(self.nchan):
            C_re, C_im = gridding.calc_matrices(uu[i], vv[i], self.us, self.vs)
            C_shape = C_re.shape
            i_re = torch.LongTensor([C_re.row, C_re.col])
            v_re = torch.DoubleTensor(C_re.data)
            C_re = torch.sparse.DoubleTensor(i_re, v_re, torch.Size(C_shape))
            self.C_res.append(C_re)
            i_im = torch.LongTensor([C_im.row, C_im.col])
            v_im = torch.DoubleTensor(C_im.data)
            C_im = torch.sparse.DoubleTensor(i_im, v_im, torch.Size(C_shape))
            self.C_ims.append(C_im)

        self.precached = True

    def forward(self, dataset):
        r"""
        Compute the model visibilities at the :math:`(u, v)` locations of the dataset. 

        Args:
            dataset (UVDataset): the dataset to forward model.

        Returns:
            (torch.double, torch.double): a 2-tuple of the :math:`\Re` and :math:`\Im` model values.
        """
        if dataset.gridded:
            assert dataset.npix == self.npix, 'Pre-gridded npix is different than model npix'
            assert dataset.cell_size == self.cell_size, 'Pre-gridded cell_size is different than model cell_size.'
            self._vis = self.cell_size ** 2 * torch.rfft((self._cube / arcsec ** 2),
              signal_ndim=2)
            vis_re = self._vis[:, :, :, 0]
            vis_im = self._vis[:, :, :, 1]
            re = vis_re.masked_select(dataset.grid_mask)
            im = vis_im.masked_select(dataset.grid_mask)
        else:
            if not self.precached:
                self.precache_interpolation(dataset)
            self._vis = self.cell_size ** 2 * torch.rfft((self._cube * self.corrfun / arcsec ** 2),
              signal_ndim=2)
            vis_re = self._vis[:, :, :, 0]
            vis_im = self._vis[:, :, :, 1]
            vr = torch.reshape(vis_re, (self.nchan, -1, 1))
            vi = torch.reshape(vis_im, (self.nchan, -1, 1))
            res = []
            ims = []
            for i in range(self.nchan):
                res.append(torch.sparse.mm(self.C_res[i], vr[i]))
                ims.append(torch.sparse.mm(self.C_ims[i], vi[i]))

            re = torch.transpose(torch.cat(res, dim=1), 0, 1)
            im = torch.transpose(torch.cat(ims, dim=1), 0, 1)
        return (re, im)

    @property
    def cube(self):
        """
        The image cube.

        Returns:
            torch.double : image cube of shape ``(nchan, npix, npix)``
            
        """
        shifted = mpol.utils.fftshift((self._cube), axes=(1, 2))
        flipped = torch.flip(shifted, (2, ))
        return flipped

    @property
    def extent(self):
        r"""
        The extent 4-tuple (in arcsec) to assign relative image coordinates (:math:`\Delta \alpha \cos \delta`,  :math:`\Delta \delta`) with matplotlib imshow. Assumes ``origin="lower"``.

        Returns:
            4-tuple: extent
        """
        low = np.min(self._ll) / arcsec - 0.5 * self.cell_size
        high = np.max(self._ll) / arcsec + 0.5 * self.cell_size
        return [
         high, low, low, high]

    @property
    def vis(self):
        """
        The visibility RFFT cube fftshifted for plotting with ``imshow`` (the v coordinate goes from -ve to +ve).

        Returns:
            torch.double: visibility cube
        """
        return mpol.utils.fftshift((self._vis), axes=(1, ))

    @property
    def vis_extent(self):
        """
        The `imshow` ``extent`` argument corresponding to `vis_cube` when plotted with ``origin="lower"``. The :math:`(u, v)` coordinates.

        Returns:
            4-tuple: extent
        """
        du = 1 / (self.npix * self.cell_size) * 0.001
        left = np.min(self.us) - 0.5 * du
        right = np.max(self.us) + 0.5 * du
        bottom = np.min(self.vs) - 0.5 * du
        top = np.max(self.vs) + 0.5 * du
        return [
         left, right, bottom, top]

    def to_FITS(self, fname='cube.fits', overwrite=False, **kwargs):
        """
        Export the image cube to a FITS file. Any extra keyword arguments will be written to the FITS header.

        Args:
            fname (str): the name of the FITS file to export to.
            overwrite (bool): if the file already exists, overwrite?

        Returns:
            None
        """
        try:
            from astropy.io import fits
            from astropy import wcs
        except ImportError:
            print('Please install the astropy package to use FITS export functionality.')

        w = wcs.WCS(naxis=2)
        w.wcs.crpix = np.array([1, 1])
        w.wcs.cdelt = np.array([self.cell_size, self.cell_size]) * 180.0 / np.pi
        w.wcs.ctype = [
         'RA---TAN', 'DEC--TAN']
        header = w.to_header()
        if kwargs is not None:
            for k, v in kwargs.items():
                header[k] = v

        hdu = fits.PrimaryHDU((self.cube.detach().cpu().numpy()), header=header)
        hdul = fits.HDUList([hdu])
        hdul.writeto(fname, overwrite=overwrite)
        hdul.close()