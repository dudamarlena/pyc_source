# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rdussurget/.virtualenvs/essai/lib/python2.7/site-packages/kernel/detectEddies.py
# Compiled at: 2016-03-24 06:20:11
__doc__ = '\nkernel.detectEddies module\n@summary: functions for detection of eddy-like features after wavelet analysis  \n@author: Renaud DUSSURGET, LER/PAC IFREMER.\n@since: Created on 9 nov. 2012\n@copyright: Renaud Dussurget 2012.\n@license: GNU Lesser General Public License\n    \n    This file is part of PyAltiWAVES.\n    \n    PyAltiWAVES is free software: you can redistribute it and/or modify it under\n    the terms of the GNU Lesser General Public License as published by the Free\n    Software Foundation, either version 3 of the License, or (at your option)\n    any later version.\n    PyAltiWAVES is distributed in the hope that it will be useful, but WITHOUT\n    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or\n    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License\n    for more details.\n    \n    You should have received a copy of the GNU Lesser General Public License along\n    with PyAltiWAVES.  If not, see <http://www.gnu.org/licenses/>.\n'
import numpy as np, scipy.ndimage as ndimage, scipy.ndimage.filters as filters, scipy.interpolate, matplotlib.pyplot as plt
from kernel.getScales import cyclone, decorrelation_scale, solid_body_scale, eddy_amplitude

def _2D(sa_spectrum, amplim=0.04, kernel=None, verbose=1):
    u"""
    _2D
    @summary: Eddy detection on both axes of the scale-averaged spectrum.
    @note: This technique was first applied in Le Hénaff et al., 2012. Cyclonic<br />
           activity in the eastern Gulf of Mexico: characterization. Submitted to <br />
           Progress in Oceanography.
    @param sa_spectrum: scale-avergaed spectrum returned by runAnalysis().
    @param sa_lscales: Lengthscale (in km) of the most energetic wavelet returned<br />
           by the wavelet analysis.
    @keyword amplim: Amplitude threshold for eddy detection.
    @keyword kernel: Kernel to pass to maximum_filter1d(). Default is a cross-shaped<br / >
                     kernel.
    @return x, y: Detection locations along X and Y axis of the SA spectrum.
    @author: Renaud DUSSURGET, LER/PAC IFREMER.
    @since : November 2012.
    @change: Create in November 2012 by RD.
    """
    sas = sa_spectrum.copy()
    shape = sas.shape
    nt = shape[0]
    npts = shape[1]
    if isinstance(sas, np.ma.masked_array):
        xx = np.arange(npts)
        yy = np.arange(nt)
        xout, yout = np.meshgrid(xx, yy)
        points = zip(*(xout[(~sa_spectrum.mask)].flatten(), yout[(~sa_spectrum.mask)].flatten()))
        values = sas.data[(~sa_spectrum.mask)].flatten()
        if len(points) > 0:
            xi = zip(*(xout[sa_spectrum.mask].flatten(), yout[sa_spectrum.mask].flatten()))
            sas[sa_spectrum.mask] = scipy.interpolate.griddata(points, values, xi, method='linear', fill_value=sas.fill_value)
            sas.mask[sas.data == sas.fill_value] = True
    if kernel is None:
        xs = 2
        ys = 2
        kernel = np.zeros((2 * ys + 1, 2 * xs + 1), dtype=bool)
        kernel[:, xs] = True
        kernel[:, xs - 1] = True
        kernel[:, xs + 1] = True
        kernel[ys, :] = True
    if verbose >= 1:
        print ('\tkernel shape :\t{0}').format(kernel.shape)
    if verbose > 1:
        for i in np.arange(kernel.shape[0]):
            print '\tkernel:\t\t' + str(kernel[i]) if i == 0 else '\t\t\t' + str(kernel[i])

    data_max = filters.maximum_filter(sas, footprint=kernel)
    maxima = (sas == data_max) & (data_max > amplim ** 2) & ~sa_spectrum.mask
    labeled, num_objects = ndimage.label(maxima)
    slices = ndimage.find_objects(labeled)
    x, y = [], []
    for dy, dx in slices:
        nx = dx.stop - dx.start
        x_center = (dx.start + dx.stop - 1) / 2
        if nx == 1:
            x.append(x_center)
        ny = dy.stop - dy.start
        y_center = (dy.start + dy.stop - 1) / 2
        if ny == 1:
            y.append(y_center)

    if isinstance(sas, np.ma.masked_array):
        inter = np.array(list(set(zip(*(x, y))).difference(set(zip(*(xout[sa_spectrum.mask].flatten(), yout[sa_spectrum.mask].flatten()))))))
        if len(inter.shape) == 2:
            x, y = inter[:, 0], inter[:, 1]
        else:
            x, y = [], []
    return (
     x, y)


def _1D(sa_spectrum, sa_lscales, win_width=5.0, amplim=3.0, len_range=[60.0, 450.0]):
    u"""
    _1D
    @summary: Detection of the most energetic eddy along the time axis of the <br />
              scale-averaged spectrum.
    @note: This is the original technique applied in :
           Dussurget, R, F Birol, R.A. Morrow, et P. De Mey. 2011. «\xa0Fine Resolution<br />
           Altimetry Data for a Regional Application in the Bay of Biscay\xa0». Marine<br />
           Geodesy 2 (34): 1‑30. doi:10.1080/01490419.2011.584835.
    @warning: This function is currently deprecated. Use _2D instead.
    @param sa_spectrum: scale-avergaed spectrum returned by runAnalysis().
    @param sa_lscales: Lengthscale (in km) of the most energetic wavelet returned<br />
           by the wavelet analysis.
    @keyword amplim: Amplitude threshold for eddy detection.
    @keyword win_width: Window size of the maximum filter.
    @keyword len_range: Range of admitted lengthscales (km). 
    @return x, y: Detection locations along X and Y axis of the SA spectrum.
    @author: Renaud DUSSURGET, LER/PAC IFREMER.
    @since : November 2012.
    @change: Create in November 2012 by RD.
    """
    raise Exception('[ERROR] This function is not available yet and/or deprecated.')


def clean_indices(sa_spectrum, sa_lscales, eind, params):
    """
    @summary: Removes not valid indices (masked point within 4 points or other point within lenghtscale)
    @author: Renaud DUSSURGET
    """
    xind = eind[0, :]
    yind = eind[1, :]
    toRm = np.array([])
    timescale_width = np.sqrt(4 - np.log(2) - np.log(np.pi))
    spectral_width = np.sqrt(4 - 0.5 * np.log(np.pi))
    N = params['N']
    dj = params['dj']
    s0 = params['s0']
    l2s = params['len2scale']
    dt = params['dt'] * 1e-05
    for i, x in enumerate(xind):
        s = sa_lscales[(yind[i], x)] * l2s
        j = np.log(s * 100000.0 / s0) / (dj * np.log(2))
        ets = timescale_width * s / dt
        e = np.ceil(1.25 * ets)
        pks = xind[((yind == yind[i]) & (xind != x))]
        pks = np.array(list(set(pks).difference(set(toRm))))
        dst = np.abs(pks - x)
        for s in pks[(dst < e)]:
            if sa_spectrum[(yind[i], s)] > sa_spectrum[(yind[i], x)]:
                toRm = np.append(toRm, i)
            else:
                toRm = np.append(toRm, s)

        if sa_spectrum.mask[yind[i], :].sum() > 0:
            if np.min(np.abs(np.arange(sa_spectrum.shape[1])[sa_spectrum.mask[yind[i], :]] - x)) < 3:
                toRm = np.append(toRm, i)

    eindin = eind.copy()
    eind = np.squeeze([np.delete(xind, toRm), np.delete(yind, toRm)])
    return eind


def detection(sa_spectrum, sa_lscales, params, amplim=0.03, twoD=True, clean=True, verbose=1, **kwargs):
    if verbose >= 1:
        str_header = ('\t===Eddy detection parameters===\n\tthreshold:{0}cm, clean:{1}, 2D:{2} ').format(np.int(amplim * 100), clean, twoD)
        print str_header
    eind = _2D(sa_spectrum, amplim=amplim, verbose=verbose, **kwargs) if twoD else _1D(sa_spectrum, amplim=amplim, verbose=verbose, **kwargs)
    eind = np.squeeze(eind)
    n_noclean = eind.shape[1]
    if clean:
        eind = clean_indices(sa_spectrum, sa_lscales, eind, params)
    n_clean = eind.shape[1]
    if verbose >= 1:
        if n_clean != 0:
            print ('\tDone : {0} peaks found ({1} of {3} ({2}%) rejected)').format(n_clean, n_noclean - n_clean, np.round(100 * np.float(n_noclean - n_clean) / n_noclean).astype(int), n_noclean)
        else:
            print '[WARNING] No peaks found!'
    return eind