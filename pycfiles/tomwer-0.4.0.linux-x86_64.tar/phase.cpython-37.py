# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/third_party/nabu/preproc/phase.py
# Compiled at: 2020-02-04 10:42:25
# Size of source mod 2**32: 14374 bytes
import numpy as np
from math import pi
from bisect import bisect
from ..utils import generate_powers
try:
    import silx.utils.enum as _Enum
except ImportError:
    from ...enum import Enum as _Enum

def lmicron_to_db(Lmicron, energy, distance):
    """
    Utility to convert the "Lmicron" parameter of PyHST
    to a value of delta/beta.

    Parameters
    ----------
    Lmicron: float
        Length in microns, values of the parameter "PAGANIN_Lmicron"
        in PyHST2 parameter file.
    energy: float
        Energy in keV.
    distance: float
        Sample-detector distance in microns

    Formula
    -------
    The conversion is done using the formula

    $$
    L^2 = \\pi \\lambda D \x0crac{\\delta}{\x08eta}
    $$
    The PyHST2 normalization differs from the one used by other softwares
    like tomopy by a factor $1/(4\\pi^2)$
    """
    L2 = Lmicron ** 2
    wavelength = 0.00123984199 / energy
    return L2 / (pi * wavelength * distance)


class PaddingMode(_Enum):
    ZEROS = 'zeros'
    MEAN = 'mean'
    EDGE = 'edge'
    SYMMETRIC = 'symmetric'
    REFLECT = 'reflect'


class PaganinPhaseRetrieval(object):
    __doc__ = '\n    Paganin Phase Retrieval for an infinitely distant point source.\n    Formula (10) in [1].\n\n    Parameters\n    ----------\n    shape: int or tuple\n        Shape of each radio, in the format (num_rows, num_columns), i.e\n        (size_vertical, size_horizontal).\n        If an integer is provided, the shape is assumed to be square.\n    distance : float, optional\n        Propagation distance in cm.\n    energy : float, optional\n        Energy in keV.\n    delta_beta: float, optional\n        delta/beta ratio, where n = (1 - delta) + i*beta is the complex\n        refractive index of the sample.\n    pixel_size : float, optional\n        Detector pixel size in microns.\n    padding : str, optional\n        Padding method. Available are "zeros", "mean", "edge", "sym",\n        "reflect". Default is "edge".\n        Please refer to the "Padding" section below for more details.\n    margin: tuple, optional\n        The user may provide integers values U, D, L, R as a tuple under the\n        form ((U, D), (L, R)) (same syntax as numpy.pad()).\n        The resulting filtered radio will have a size equal to\n        (size_vertic - U - D, size_horiz - L - R).\n        These values serve to create a "margin" for the filtering process,\n        where U, D, L R are the margin of the Up, Down, Left and Right part,\n        respectively.\n        The filtering is done on a subset of the input radio. The subset\n        size is (Nrows - U - D, Ncols - R - L).\n        The margins is used to do the padding for the rest of the padded\n        array.\n\n        For example in one dimension, where padding="edge":\n\n        <------------------------------ padded_size --------------------------->\n        [padding=edge | padding=data | radio data | padding=data | padding=edge]\n        <------ N2 ---><----- L -----><- (N-L-R)--><----- R -----><----- N2 --->\n\n        Some or all the values U, D, L, R can be 0. In this case,\n        the padding of the parts related to the zero values will\n        fall back to the one of "padding" parameter.\n        For example, if padding="edge" and L, R are 0, then\n        the left and right parts will be padded with the edges, while\n        the Up and Down parts will be padded using the the user-provided\n        margins of the radio, and the final data will have shape\n        (Nrows - U - D, Ncols).\n        Some or all the values U, D, L, R can be the string "auto".\n        In this case, the values of U, D, L, R are automatically computed\n        as a function of the Paganin filter width.\n    use_R2C: bool, optional\n        Whether to use Real-to-Complex (R2C) transform instead of\n        standard Complex-to-Complex transform, providing better performances\n\n    Padding methods\n    ---------------\n    The phase retrieval is a convolution done in Fourier domain using FFT,\n    so the Fourier transform size has to be at least twice the size of\n    the original data. Mathematically, the data should be padded with zeros\n    before being Fourier transformed. However, in practice, this can lead\n    to artefacts at the edges (Gibbs effect) if the data does not go to\n    zero at the edges.\n    Apart from applying an apodization (Hamming, Blackman, etc), a common\n    strategy to avoid these artefacts is to pad the data.\n    In tomography reconstruction, this is usually done by replicating the\n    last(s) value(s) of the edges ; but one can think of other methods:\n\n       - "zeros": the data is simply padded with zeros.\n       - "mean": the upper side of extended data is padded with the mean of\n         the first row, the lower side with the mean of the last row, etc.\n       - "edge": the data is padded by replicating the edges.\n         This is the default mode.\n       - "sym": the data is padded by mirroring the data with respect\n         to its edges. See numpy.pad().\n       - "reflect": the data is padded by reflecting the data with respect\n         to its edges, including the edges. See numpy.pad().\n\n\n    Formulas\n    --------\n    The radio is divided, in the Fourier domain, by the original\n    "Paganin filter" [1]\n\n    $$\n    F + 1 + \x0crac{\\delta}{\x08eta} \\lambda D \rho |k|^2\n    $$\n    where $k$ is the wave vector, computed as\n\n    $$\n    k_l = \x0crac{1}{P} (\x0crac{-1}{2} + \x0crac{l}{N-1})\n    $$\n    where $P$ is the pixel size, $N$ the number of pixels in one direction,\n    and $l \\in [0, N-1]$.\n    The factor $\rho$ is either $\\pi$ or $1/(4\\pi^2)$\n    depending on the convention (default is the former).\n\n\n    References\n    -----------\n    [1] D. Paganin Et Al, "Simultaneous phase and amplitude extraction\n        from a single defocused image of a homogeneous object",\n        Journal of Microscopy, Vol 206, Part 1, 2002\n    '
    powers = generate_powers()

    def __init__(self, shape, distance=50, energy=20, delta_beta=250.0, pixel_size=1, padding='edge', margin=None, use_R2C=True):
        self._init_parameters(distance, energy, pixel_size, delta_beta, padding, use_R2C)
        self._calc_shape(shape, margin)
        self.compute_filter()

    def _init_parameters(self, distance, energy, pixel_size, delta_beta, padding, use_R2C):
        self.distance_cm = distance
        self.distance_micron = distance * 10000.0
        self.energy_kev = energy
        self.pixel_size_micron = pixel_size
        self.delta_beta = delta_beta
        self.wavelength_micron = 0.00123984199 / self.energy_kev
        self.padding = padding
        self.padding_methods = {PaddingMode.ZEROS: self._pad_zeros, 
         PaddingMode.MEAN: self._pad_mean, 
         PaddingMode.EDGE: self._pad_edge, 
         PaddingMode.SYMMETRIC: self._pad_sym, 
         PaddingMode.REFLECT: self._pad_reflect}
        self.use_R2C = use_R2C
        if use_R2C:
            self.fft_func = np.fft.rfft2
            self.ifft_func = np.fft.irfft2
        else:
            self.fft_func = np.fft.fft2
            self.ifft_func = np.fft.ifft2

    def _calc_shape(self, shape, margin):
        if np.isscalar(shape):
            shape = (
             shape, shape)
        else:
            assert len(shape) == 2
        self.shape = shape
        self._set_margin_value(margin)
        self._calc_padded_shape()

    def _set_margin_value(self, margin):
        self.margin = margin
        if margin is None:
            self.shape_inner = self.shape
            self.use_margin = False
            self.margin = ((0, 0), (0, 0))
            return
        self.use_margin = True
        try:
            (U, D), (L, R) = margin
        except ValueError:
            raise ValueError('Expected margin in the format ((U, D), (L, R))')

        for val in [U, D, L, R]:
            if type(val) == str:
                if val != 'auto':
                    raise ValueError("Expected either an integer, or 'auto'")
            if int(val) != val or val < 0:
                raise ValueError('Expected positive integers for margin values')

        self.shape_inner = (
         self.shape[0] - U - D, self.shape[1] - L - R)

    def _calc_padded_shape(self):
        """
        Compute the padded shape.
        If margin = 0, length_padded = next_power(2*length).
        Otherwise : length_padded = next_power(2*(length - margins))

        Principle
        ----------

        <--------------------- nx_p --------------------->
        |         |        original data       |         |
        < -- Pl - ><-- L -->< -- nx --><-- R --><-- Pr -->
                   <----------- nx0 ----------->

        Pl, Pr : left/right padding length
        L, R : left/right margin
        nx : length of inner data (and length of final result)
        nx0 : length of original data
        nx_p : total length of padded data
        """
        n_y, n_x = self.shape_inner
        n_y_p = self._get_next_power(2 * n_y)
        n_x_p = self._get_next_power(2 * n_x)
        self.shape_padded = (n_y_p, n_x_p)
        self.data_padded = np.zeros((n_y_p, n_x_p), dtype=(np.float64))
        (U, D), (L, R) = self.margin
        n_y0, n_x0 = self.shape
        self.pad_top_len = (n_y_p - n_y0) // 2
        self.pad_bottom_len = n_y_p - n_y0 - self.pad_top_len
        self.pad_left_len = (n_x_p - n_x0) // 2
        self.pad_right_len = n_x_p - n_x0 - self.pad_left_len

    def _get_next_power(self, n):
        """
        Given a number, get the closest (upper) number p such that
        p is a power of 2, 3, 5 and 7.
        """
        idx = bisect(self.powers, n)
        if self.powers[(idx - 1)] == n:
            return n
        return self.powers[idx]

    def compute_filter(self):
        nyp, nxp = self.shape_padded
        fftfreq = np.fft.rfftfreq if self.use_R2C else np.fft.fftfreq
        fy = np.fft.fftfreq(nyp, d=(self.pixel_size_micron))
        fx = fftfreq(nxp, d=(self.pixel_size_micron))
        self._coords_grid = np.add.outer(fy ** 2, fx ** 2)
        k2 = self._coords_grid
        D = self.distance_micron
        L = self.wavelength_micron
        db = self.delta_beta
        self.paganin_filter = 1.0 / (1 + db * L * D * pi * k2)

    def pad_with_values(self, data, top_val=0, bottom_val=0, left_val=0, right_val=0):
        """
        Pad the data into `self.padded_data` with values.

        Parameters
        ----------
        data: numpy.ndarray
            data (radio)
        top_val: float or numpy.ndarray, optional
            Value(s) to fill the top of the padded data with.
        bottom_val: float or numpy.ndarray, optional
            Value(s) to fill the bottom of the padded data with.
        left_val: float or numpy.ndarray, optional
            Value(s) to fill the left of the padded data with.
        right_val: float or numpy.ndarray, optional
            Value(s) to fill the right of the padded data with.
        """
        self.data_padded.fill(0)
        Pu, Pd = self.pad_top_len, self.pad_bottom_len
        Pl, Pr = self.pad_left_len, self.pad_right_len
        self.data_padded[:Pu, :] = top_val
        self.data_padded[-Pd:, :] = bottom_val
        self.data_padded[:, :Pl] = left_val
        self.data_padded[:, -Pr:] = right_val
        self.data_padded[Pu:-Pd, Pl:-Pr] = data
        self.data_padded = np.roll((self.data_padded), (-Pu, -Pl), axis=(0, 1))

    def _pad_zeros(self, data):
        return self.pad_with_values(data, top_val=0, bottom_val=0, left_val=0, right_val=0)

    def _pad_mean(self, data):
        """
        Pad the data at each border with a different constant value.
        The value depends on the padding size:
          - On the left, value = mean(first data column)
          - On the right, value = mean(last data column)
          - On the top, value = mean(first data row)
          - On the bottom, value = mean(last data row)
        """
        return self.pad_with_values(data,
          top_val=(np.mean(data[0, :])),
          bottom_val=(np.mean(data[-1, :])),
          left_val=(np.mean(data[:, 0])),
          right_val=(np.mean(data[:, -1])))

    def _pad_numpy(self, data, mode):
        data_padded = np.pad(data,
          (
         (
          self.pad_top_len, self.pad_bottom_len), (self.pad_left_len, self.pad_right_len)),
          mode=(mode.value))
        Pu, Pl = self.pad_top_len, self.pad_left_len
        return np.roll(data_padded, (-Pu, -Pl), axis=(0, 1))

    def _pad_edge(self, data):
        self.data_padded = self._pad_numpy(data, mode=(PaddingMode.EDGE))

    def _pad_sym(self, data):
        self.data_padded = self._pad_numpy(data, mode=(PaddingMode.SYMMETRIC))

    def _pad_reflect(self, data):
        self.data_padded = self._pad_numpy(data, mode=(PaddingMode.REFLECT))

    def pad_data(self, data, padding_method=None):
        padding_method = padding_method or self.padding
        padding_method = PaddingMode.from_value(padding_method)
        if padding_method not in self.padding_methods:
            raise ValueError('Unknown padding method %s. Available are: %s' % (
             padding_method, str(list(self.padding_methods.keys()))))
        pad_func = self.padding_methods[padding_method]
        pad_func(data)
        return self.data_padded

    def apply_filter(self, radio, padding_method=None):
        self.pad_data(radio, padding_method=padding_method)
        radio_f = self.fft_func(self.data_padded)
        radio_f *= self.paganin_filter
        radio_filtered = self.ifft_func(radio_f).real
        s0, s1 = self.shape_inner
        (U, _), (L, _) = self.margin
        return radio_filtered[U:U + s0, L:L + s1]

    def lmicron_to_db(self, Lmicron):
        """
        Utility to convert the "Lmicron" parameter of PyHST
        to a value of delta/beta.
        Please see the doc of nabu.preproc.phase.lmicron_to_db()
        """
        return lmicron_to_db(Lmicron, self.energy_kev, self.distance_micron)

    __call__ = apply_filter