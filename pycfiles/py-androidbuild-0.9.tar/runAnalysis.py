# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rdussurget/.virtualenvs/essai/lib/python2.7/site-packages/kernel/runAnalysis.py
# Compiled at: 2016-03-24 07:06:55
__doc__ = '\nkernel.runAnalysis module\n@since: Created on 9 nov. 2012\n@author: rdussurg\n@copyright: Renaud Dussurget 2012.\n@license: GNU Lesser General Public License\n    \n    This file is part of PyAltiWAVES.\n    \n    PyAltiWAVES is free software: you can redistribute it and/or modify it under\n    the terms of the GNU Lesser General Public License as published by the Free\n    Software Foundation, either version 3 of the License, or (at your option)\n    any later version.\n    PyAltiWAVES is distributed in the hope that it will be useful, but WITHOUT\n    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or\n    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License\n    for more details.\n    \n    You should have received a copy of the GNU Lesser General Public License along\n    with PyAltiWAVES.  If not, see <http://www.gnu.org/licenses/>.\n'
from __future__ import print_function
import sys, numpy as np, altimetry.tools as AT, kernel, matplotlib.pyplot as plt
curper = 0

def process(i, N, step=10):
    """
    process : 
    @summary: counter bar
    """
    global curper
    per = np.int16(100.0 * i / N)
    if per >= curper + 10 or i == 0:
        print('o', end='')
        curper = per


def runAnalysis(lon, lat, time, sla, mother='dog', m=None, len_range=[
 60.0, 450.0], dj_factor=1.0, detrend=True, demean=False, verbose=True):
    u"""
    run_analysis :  
    @summary: Run wavelet analysis on along-track altimetry sea level data as in Dussurget et al., 2011.
    @note: Details of the wavelet analysis is found in :
             o Dussurget, R, F Birol, R.A. Morrow, et P. De Mey. 2011. «\xa0Fine Resolution<br />
               Altimetry Data for a Regional Application in the Bay of Biscay\xa0». Marine<br />
               Geodesy 2 (34): 1‑30. doi:10.1080/01490419.2011.584835.
             o Torrence, C., et G.P. Compo. 1998. «\xa0A Practical Guide to Wavelet Analysis\xa0».<br />
             Bulletin of the American Meteorological Society 79 (1): 61‑78.
    @param lon, lat: Longitude/latitude arrays.
    @param time: time vector.
    @param sla: along-track matrice of sea level anomaly data (time,*pts)
    @keyword mother {string}{default:'dog'}: Name of the mother wavelet, as specified in wavelet.py.
    @keyword m {default: 2 for 'dog', 6 for 'morlet'}: Order of the wavelet.
    @keyword len_range {default:[60,450]}: Range of scale integration (in km). Scales outside this<br />
             range will be cancelled.
    @keyword detrend {boolean}{default:True}: apply linear detrending before computing the transform.
    @keyword demean  {boolean}{default:True}: Demean SLA data before computing the transform.
    @return diameter, symmetric : Diameter (km) of detected eddies, and symmetric flag to<br />
            check whether symmetry assumption was used or not.
    @author: Renaud DUSSURGET, LER/PAC IFREMER.
    @since : November 2012.
    @change: Create in November 2012 by RD.
    """
    km2cm = 100000.0
    cm2km = km2cm ** (-1.0)
    nx = len(lon)
    nt = len(time)
    dst = AT.calcul_distance(lat, lon)
    dstcm = dst * km2cm
    dt = np.median(AT.deriv(dstcm))
    m = 6 if mother == 'morlet' else 2 if m is None else m
    len2scale = np.sqrt(m + 0.5) / (2 * np.pi)
    scale2len = 2 * np.pi / np.sqrt(m + 0.5)
    T = max(dstcm)
    s0 = 2.0 * dt if mother == 'morlet' else 2 * dt * len2scale
    dj = dj_factor * (dt / T) * len2scale
    J = np.fix(np.log(T * len2scale / s0) / np.log(2.0) / dj).astype(int)
    avg1, avg2 = len_range
    slevel = 0.95
    alpha = 0.0
    exec ('mother_obj=kernel.wavelet.{0}({1})').format(mother, m)
    if verbose:
        str_header = ('\t===Wavelet analysis parameters===\n\twavelet:{0}, degree:{1}, scale range {2} {3} km\n\toptions : ').format(mother, m, len_range[0], len_range[1])
        str_opt = (',').join([ x for x in np.array(['demean', 'detrend', 'filter'])[(np.array([demean, detrend, filter]) == True)] ])
        print(str_header + str_opt)
        print('\tstatus : ', end='')
    acov = np.nansum(np.isfinite(sla), axis=1)
    per = 100.0 * acov.astype(float) / nx
    fg = (per.data >= 0.15) & (acov.data > 10)
    count = fg.sum()
    if count == nt:
        enough = np.arange(nt)
    else:
        enough = np.where(fg)[0]
    if detrend:
        sla[enough, :] = AT.detrend(dst, sla[enough, :])
    if demean:
        sla -= np.repeat(np.nansum(sla, axis=1) / nx, nx).reshape((nt, nx))
    sa_spectrum = np.ma.array(np.zeros((nt, nx)), mask=np.ones((nt, nx), dtype=bool))
    wvsla = np.ma.array(np.zeros((nt, nx)), mask=np.ones((nt, nx), dtype=bool))
    sa_lscales = np.ma.array(np.zeros((nt, nx)), mask=np.ones((nt, nx), dtype=bool))
    daughtout = np.ma.array(np.zeros((nt, nx)), mask=np.ones((nt, nx), dtype=bool))
    avg_sig = np.arange(nt, dtype=np.float32)
    Cpsi = np.arange(nt, dtype=np.float32)
    lenscale = np.ma.array(np.zeros(nt), mask=np.ones(nt, dtype=bool))
    outsla = np.ma.array(np.zeros((nt, nx)), mask=np.ones((nt, nx), dtype=bool))
    WPower = np.ma.array(np.zeros((J + 1, nx), dtype=np.float32), mask=np.ones((J + 1, nx), dtype=bool))
    W = WPower.copy()
    daughter = np.ma.array(np.ones((J + 1, nx)) * np.complex128(0), mask=np.ones((J + 1, nx), dtype=bool))
    for i, valid in enumerate(enough):
        process(i, count)
        fg = (isinstance(sla, np.ma.masked_array) or np.isfinite)(sla[valid, :]) if 1 else ~sla[valid, :].mask
        fgcnt = (~fg).sum()
        if fgcnt > 0:
            dum = sla[valid, :]
            dum, dumlon, dumlat, dumind, ngaps, gapedges, gaplen, interpolated = AT.fill_gaps(lat, lon, sla[valid, :], ~fg, remove_edges=True)
        else:
            dum = sla[valid, :]
            dumind = np.arange(len(dum))
            ngaps = 0
            gaplen = []
            gapedges = []
        ndum = len(dum)
        std = dum.std()
        std2 = std ** 2
        scale = 0
        per = 0
        wave, scale, wavenb, coi_temp, daughter_temp, fft, fftfreqs = kernel.wavelet.cwt(dum, dt, dj, s0, J, mother_obj)
        signif, fft_theor = kernel.wavelet.significance(1.0, dt, scale, 0, alpha, significance_level=slevel, wavelet=mother_obj)
        Cd = mother_obj.cdelta
        length = 1.0 / wavenb
        WPower[:] = np.ma.array(0, mask=True)
        W[:] = np.ma.array(0, mask=True)
        daughter[:] = np.ma.array(np.complex128(0), mask=True)
        WPower[:, dumind] = abs(wave) ** 2
        W[:, dumind] = np.real(wave)
        daughter[:, dumind] = daughter_temp
        sig95 = WPower / (signif * np.ones((nx, 1))).transpose()
        coi = np.repeat(s0 * scale2len, nx)
        coi[dumind] = coi_temp
        coi[~fg[dumind]] = s0 * scale2len
        lengthkm = length * cm2km
        scalekm = scale * cm2km
        coikm = coi * cm2km
        coimask = np.repeat(coi, J + 1).reshape((nx, J + 1)).transpose() <= np.repeat(length, nx).reshape((J + 1, nx))
        data_mask = np.ones((J + 1, nx), dtype=bool)
        data_mask[:, fg] = False
        mask = coimask | data_mask
        WPower.mask[:] = mask
        W.mask[:] = mask
        scale_fg = (lengthkm >= avg1) & (lengthkm <= avg2)
        dum_sa_spec = WPower / (scale * np.ones((nx, 1))).transpose()
        sa_spectrum[valid, :] = dj * dt / Cd * dum_sa_spec.sum(axis=0)
        dum_wvsla = W / (np.sqrt(scale) * np.ones((nx, 1))).transpose()
        wvsla[valid, :] = dj * np.sqrt(dt) / (Cd * 1.0) * dum_wvsla.sum(axis=0)
        scale_avg_signif, tmp = kernel.wavelet.significance(std2, dt, scale, 2, alpha, significance_level=slevel, dof=[scale[scale_fg][0],
         scale[scale_fg][(-1)]], wavelet=mother_obj)
        masked_pts = ~(np.fix(~mask).sum(axis=0) > 0)
        mxid = sa_spectrum[valid, :].argmax()
        lenscale[valid] = sa_lscales[valid, :][mxid]
        scid = np.ma.array(WPower[scale_fg, :].argmax(axis=0), mask=masked_pts)
        sa_lscales[valid, :] = np.ma.array(lengthkm[scid], mask=scid.mask)
        ddum = np.real(daughter.data[scid[mxid], :]) / np.real(daughter.data[scid[mxid], :]).max() * np.abs(np.sqrt(sa_spectrum[(valid, mxid)])) * (np.abs(sla[(valid, mxid)]) / sla[(valid, mxid)])
        daughtout[valid, :] = ddum

    mx = np.ma.array(np.zeros((nt, nx)), mask=np.ones((nt, nx), dtype=bool), dtype=np.float)
    idmx = np.ma.array(np.zeros(nt), mask=np.ones(nt, dtype=bool), dtype=np.float)
    for i in np.arange(nt):
        ind = sa_spectrum[i, :].argmax()
        mx[(i, ind)] = sa_spectrum[(i, ind)]
        idmx[i] = ind

    if verbose:
        print('o done\n\t=================================')
    return (
     sa_spectrum, sa_lscales, wvsla, daughtout, {'m': m, 'mother': mother, 'demean': int(demean), 'detrend': int(detrend), 'range': len_range, 'len2scale': len2scale, 'dj': dj, 's0': s0, 'J': J, 'dt': dt, 'T': T, 'N': nx, 'cm2km': cm2km})