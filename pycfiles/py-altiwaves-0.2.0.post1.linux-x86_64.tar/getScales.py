# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rdussurget/.virtualenvs/essai/lib/python2.7/site-packages/kernel/getScales.py
# Compiled at: 2016-03-24 07:05:25
"""
kernel.getScales module
:change: Created on 12 nov. 2012 by RD
:author: rdussurg
:copyright: Renaud Dussurget 2012.
:license: GNU Lesser General Public License
=======
@since: Created on 12 nov. 2012 by RD
@author: rdussurg
@copyright: Renaud Dussurget 2012.
@license: GNU Lesser General Public License
    
    This file is part of PyAltiWAVES.
    
    PyAltiWAVES is free software: you can redistribute it and/or modify it under
    the terms of the GNU Lesser General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.
    PyAltiWAVES is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
    for more details.
    
    You should have received a copy of the GNU Lesser General Public License along
    with PyAltiWAVES.  If not, see <http://www.gnu.org/licenses/>.
"""
import numpy as np
from scipy.ndimage.filters import maximum_filter1d
from scipy.special import gamma
from scipy import optimize
from altimetry.tools import grid_track, geost_1d, deriv
from altimetry.tools.spatial_tools import calcul_distance
from scipy.optimize.minpack import curve_fit
from altimetry.tools.others import nearest
import matplotlib.pyplot as plt, warnings

def leastsq_bounds(func, x0, bounds, boundsweight=10, **kwargs):
    """
    run leastsq with bound conatraints lo <= p <= hi
    leastsq with additional constraints to minimize the sum of squares of
        [func(p) ...] + boundsweight * [max( lo_i - p_i, 0, p_i - hi_i ) ...]
 
    Parameters
    ----------
    func() : a function of parameters `p`
    bounds : an n x 2 list or array `[[lo_0,hi_0], [lo_1, hi_1] ...]`.
        Use e.g. [0, inf]; do not use NaNs.
        A bound e.g. [2,2] pins that x_j == 2.
    boundsweight : weights the bounds constraints
    kwargs : keyword args passed on to leastsq
 
    Returns
    -------
    exactly as for leastsq,
    http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.leastsq.html
 
    Notes
    -----
    The bounds may not be met if boundsweight is too small;
    check that with e.g. check_bounds( p, bounds ) below.
 
    To access `x` in `func(p)`, `def func( p, x=xouter )`
    or make it global, or `self.x` in a class.
 
    There are quite a few methods for box constraints;
    you'll maybe sing a longer song ...
    Comments are welcome, test cases most welcome.
 
"""
    if bounds is not None and boundsweight > 0:
        funcbox = lambda p, u, r: np.hstack((func(p, u, r), _inbox(p, bounds, boundsweight)))
    else:
        funcbox = func
    return optimize.leastsq(funcbox, x0, **kwargs)


def _inbox(X, box, weight=1):
    """ -> [tub( Xj, loj, hij ) ... ]
        all 0  <=>  X in box, lo <= X <= hi
    """
    assert len(X) == len(box), 'len X %d != len box %d' % (len(X), len(box))
    return weight * np.array([ np.fmax(lo - x, 0) + np.fmax(0, x - hi) for x, (lo, hi) in zip(X, box)
                             ])


def check_bounds(X, box):
    """ print Xj not in box, loj <= Xj <= hij
        return nr not in
    """
    nX, nbox = len(X), len(box)
    assert nX == nbox, 'len X %d != len box %d' % (nX, nbox)
    nnotin = 0
    for j, x, (lo, hi) in zip(range(nX), X, box):
        if not lo <= x <= hi:
            print 'check_bounds: x[%d] %g is not in box %g .. %g' % (j, x, lo, hi)
            nnotin += 1

    return nnotin


def rankine_model(r, R, V):
    vout = r.copy()
    for i, rr in enumerate(vout):
        if np.abs(rr) < np.abs(R):
            vout[i] = V * rr / R
        elif rr == 0.0:
            vout[i] = 0.0
        else:
            vout[i] = V * R / rr

    return vout


def resid(p, r, u):
    R, V = p
    return u - rankine_model(r, R, V)


def cyclone(sla, ind):
    """
    cyclone
    @summary: Test the rotation sense of detected eddies.
    @param sla: Along-track sea level anomalies for detected events.
    @param ind: Indices of the detected events.
    @return {array}: True if detected events are cyclones.
    @author: Renaud DUSSURGET, LER/PAC IFREMER.
    @since : November 2012.
    @change: Create in November 2012 by RD.
    """
    return sla[(ind[1], ind[0])] < 0


def eddy_amplitude(sla, ind):
    """
    eddy_amplitude
    @summary: Get the eddy amplitude of detected eddies.
    @param sla: Along-track sea level anomalies for detected events.
    @param ind: Indices of the detected events.
    @return {array}: Amplitudes.
    @author: Renaud DUSSURGET, LER/PAC IFREMER.
    @since : November 2012.
    @change: Create in November 2012 by RD.
    """
    return np.abs(sla[(ind[1], ind[0])])


def solid_body_scale(var, lat, lon, ind, verbose=1, **kwargs):
    u"""
    solid_body_scale
    @summary: Compute the diameter of eddy core using maxima of geostrophic velocities<br />
              computed on both sides of the eddy, and computes the equivalent Relative<br />
              Vorticity for a solid body rotating eddy.
    @note: This technique was first applied in Le Hénaff et al., 2012. Cyclonic<br />
           activity in the eastern Gulf of Mexico: characterization. Submitted to <br />
           Progress in Oceanography.
    @note: A 2nd order polynomial over 3-4 points around the velocity maximum is<br />
           computed to better detect its position.
    @note: Geostrophic velocities are computed using the Powell and Leben (2004)<br />
           methodology - powell_leben_filter_km() function. Filtering parameters are<br/>
           p=q=12km on each sides of the point.
           Powell, B.S., et R.R. Leben. 2004. «\xa0An Optimal Filter for Geostrophic Mesoscale<br/>
           Currents from Along-Track Satellite Altimetry\xa0». Journal of Atmospheric and<br/>
           Oceanic Technology 21 (10) (octobre 1): 1633‑1642.
    @param var: variable on which to apply the analysis : SLA, wavelet-filtered SLA,<br />
                daughter wavelets, etc...
    @param lon, lat: Longitude/latitude arrays.
    @ind: Indices of detected eddies.
    @return diameter, relvort : Diameter (km) and Relative Vorticity (s-1) of detected eddies.
    @author: Renaud DUSSURGET, LER/PAC IFREMER.
    @since : November 2012.
    @change: Created in November 2012 by RD.
    """
    p = kwargs.pop('p', 20.0)
    q = kwargs.pop('q', p)
    filter = kwargs.pop('filter', 40.0)
    if verbose >= 1:
        print ('\tsolid_body_scale() running: SLA filtering prior computation of velocities:{0} km, Velocity filtering:{1} km').format(np.int(filter) if filter is not None else 'None', np.int(p + q))
    xid = ind[1]
    yid = ind[0]
    ne = np.size(xid)
    diameter = np.zeros(ne, dtype=np.float32)
    amplitude = np.zeros(ne, dtype=np.float32)
    north = np.zeros(ne, dtype=np.float32)
    south = np.zeros(ne, dtype=np.float32)
    relvort = np.zeros(ne, dtype=np.float32)
    rk_diameter = np.zeros(ne, dtype=np.float32)
    rk_relvort = np.zeros(ne, dtype=np.float32)
    rk_center = np.zeros(ne, dtype=int)
    self_advect = np.zeros(ne, dtype=np.float32)
    for j in np.arange(ne):
        cursla = var[xid[j], :]
        fg = ~cursla.mask
        dumy = np.where(np.arange(len(cursla))[fg] == yid[j])[0][0]
        cursla = cursla[fg]
        cursla -= np.median(cursla)
        dst, dumlon, dumlat, dumsla, gaplen, ngaps, gapedges, interpolated = grid_track(lat[fg], lon[fg], cursla)
        ugeo = geost_1d(dumlon, dumlat, dumsla, pl04=True, filter=filter, p=p, q=q)
        ncur = len(dst)
        northward = dumlat[(-1)] > dumlat[0]
        dumy = np.arange(len(dst))[(~interpolated)][dumy]
        dumsla_n = dumsla[dumy:] if northward else dumsla[dumy:0:-1]
        dumsla_s = dumsla[dumy:0:-1] if northward else dumsla[dumy:]
        ugeo_n = ugeo[dumy:] if northward else ugeo[dumy:0:-1]
        ugeo_s = ugeo[dumy:0:-1] if northward else ugeo[dumy:]
        nn = len(dumsla_n)
        ns = len(dumsla_s)
        iscyclone = dumsla[dumy] < 0
        if iscyclone:
            mx_s = np.where(maximum_filter1d(ugeo_s, 3) == ugeo_s)[0]
            mx_n = np.where(maximum_filter1d(-ugeo_n, 3) == -ugeo_n)[0]
        elif not iscyclone:
            mx_s = np.where(maximum_filter1d(-ugeo_s, 3) == -ugeo_s)[0]
            mx_n = np.where(maximum_filter1d(ugeo_n, 3) == ugeo_n)[0]
        else:
            raise Exception('This case is not possible')
        mx_s = mx_s[((mx_s != 0) & (np.abs(dumsla_s[mx_s] - dumsla[dumy]) > 0.01))]
        mx_n = mx_n[((mx_n != 0) & (np.abs(dumsla_n[mx_n] - dumsla[dumy]) > 0.01))]
        if len(mx_n) == 0:
            dumsla_n = dumsla_s.copy()
            ugeo_n = ugeo_s.copy()
            nn = ns
            mx_n = mx_s
        if len(mx_s) == 0:
            dumsla_s = dumsla_n.copy()
            ugeo_s = ugeo_n.copy()
            ns = nn
            mx_s = mx_n
        mx_s = mx_s[0]
        mx_n = mx_n[0]
        amplitude[j] = np.abs(dumsla[dumy] - np.mean([dumsla_n[mx_n], dumsla_s[mx_s]]))
        if mx_s != ns - 1:
            if np.abs(ugeo_s[(mx_s - 1)]) > np.abs(ugeo_s[(mx_s + 1)]):
                fit = np.polyfit(dst[mx_s - 1:mx_s + 3 if mx_s + 3 <= ns else ns], ugeo_s[mx_s - 1:mx_s + 3 if mx_s + 3 <= ns else ns], 2)
            else:
                fit = np.polyfit(dst[mx_s - 2 if mx_s >= 2 else 0:mx_s + 2], ugeo_s[mx_s - 2 if mx_s >= 2 else 0:mx_s + 2], 2)
        else:
            fit = np.polyfit(dst[mx_s - 2 if mx_s >= 2 else 0:mx_s + 1], ugeo_s[mx_s - 2 if mx_s >= 2 else 0:mx_s + 1], 2)
        radius_s = -fit[1] / (2 * fit[0])
        if mx_s > 1 and mx_s < ns - 1 and mx_n > 1 and mx_n < ns - 1:
            if (radius_s > dst[(mx_s - 1)]) & (radius_s < dst[(mx_s + 1)]):
                diameter[j] += radius_s
            else:
                diameter[j] += dst[mx_s]
        else:
            diameter[j] += dst[mx_s]
        if mx_n != nn - 1:
            if np.abs(ugeo_n[(mx_n - 1)]) > np.abs(ugeo_n[(mx_n + 1)]):
                fit = np.polyfit(dst[mx_n - 1:mx_n + 3 if mx_n + 3 <= nn else nn], ugeo_n[mx_n - 1:mx_n + 3 if mx_n + 3 <= nn else nn], 2)
            else:
                fit = np.polyfit(dst[mx_n - 2 if mx_n >= 2 else 0:mx_n + 2], ugeo_n[mx_n - 2 if mx_n >= 2 else 0:mx_n + 2], 2)
        else:
            fit = np.polyfit(dst[mx_n - 2 if mx_n >= 2 else 0:mx_n + 1], ugeo_n[mx_n - 2 if mx_n >= 2 else 0:mx_n + 1], 2)
        radius_n = -fit[1] / (2 * fit[0])
        if mx_s > 1 and mx_s < ns - 1 and mx_n > 1 and mx_n < ns - 1:
            if (radius_n > dst[(mx_n - 1)]) & (radius_n < dst[(mx_n + 1)]):
                diameter[j] += radius_n
            else:
                diameter[j] += dst[mx_n]
        else:
            diameter[j] += dst[mx_n]
        curdst = np.append(-dst[mx_s:0:-1] * 1000.0, dst[1:mx_n + 1] * 1000.0)
        curugeo = np.append(ugeo_s[mx_s:0:-1], ugeo_n[1:mx_n + 1])
        relvort[j] = -np.polyfit(curdst, curugeo, 1)[0]
        Vanom = np.mean([ugeo_s[mx_s], ugeo_n[mx_n]])
        V = ugeo_n[mx_n] - Vanom
        R = diameter[j] / 2.0 if northward else -(diameter[j] / 2.0)
        dx = np.median(deriv(dst))
        rid = np.arange(ncur)[(np.abs(dst - dst[dumy]) < np.abs(R))][np.argmin(np.abs(ugeo - Vanom)[(np.abs(dst - dst[dumy]) < np.abs(R))])]
        r = (dst - dst[dumy])[rid]
        pn = np.ceil(R / dx)
        u1 = ugeo_s[:pn * 4][::-1]
        u2 = ugeo_n[1:pn * 4]
        d1 = dst[0:len(u1)]
        d2 = dst[1:len(u2) + 1]
        (Rout, Vout), flag = leastsq_bounds(resid, [R, V], [[0, 1.5 * R], [0, 2 * V]], args=(dst - dst[dumy] - r, ugeo - Vanom))
        rk_diameter[j] = Rout * 2.0
        rk_relvort[j] = Vout / (Rout * 1000.0)
        if northward:
            rk_relvort[j] *= -1.0
        self_advect[j] = Vanom
        rid_input = nearest(lon, dumlon[np.arange(ncur)[rid]])
        if calcul_distance(lat[rid_input], lon[rid_input], dumlat[rid], dumlon[rid]) < dx:
            rk_center[j] = rid_input
        else:
            rk_center[j] = rid
            print '[kernel.getScales()]WARNING:center has not been offsetted due to its distance to original location'

    return (
     diameter, relvort, amplitude, rk_relvort, rk_center, rk_diameter, self_advect)


def decorrelation_scale(var, lat, lon, ind, verbose=1):
    u"""
    solid_body_scale
    @summary: Compute the decorrelation length-scale of detected eddies.
    @note: This is the original technique applied in :
           Dussurget, R, F Birol, R.A. Morrow, et P. De Mey. 2011. «\xa0Fine Resolution<br />
           Altimetry Data for a Regional Application in the Bay of Biscay\xa0». Marine<br />
           Geodesy 2 (34): 1‑30. doi:10.1080/01490419.2011.584835.
    @note: A linear regression is applied between the two points around the decorrelation<br />
           scale to better detect its position.
    @note: If no sufficient data is found on one of both sides, eddy is considered as<br />
           symmetric and scales are thus only computed from one side.
    @param var: variable on which to apply the analysis : SLA, wavelet-filtered SLA,<br />
                daughter wavelets, etc...
    @param lon, lat: Longitude/latitude arrays.
    @ind: Indices of detected eddies.
    @return diameter, symmetric : Diameter (km) of detected eddies, and symmetric flag to<br />
            check whether symmetry assumption was used or not.
    @author: Renaud DUSSURGET, LER/PAC IFREMER.
    @since : November 2012.
    @change: Create in November 2012 by RD.

    """
    xid = ind[1]
    yid = ind[0]
    ne = np.size(xid)
    diameter = np.zeros(ne, dtype=np.float64)
    symmetric = np.zeros(ne, dtype=bool)
    if verbose >= 1:
        print '\tdecorrelation_scale() running'
    for j in np.arange(ne):
        cursla = var[xid[j], :]
        fg = ~cursla.mask
        dumy = np.where(np.arange(len(cursla))[fg] == yid[j])[0][0]
        cursla = cursla[fg]
        cursla -= np.median(cursla)
        dst, dumlon, dumlat, dumsla, gaplen, ngaps, gapedges, interpolated = grid_track(lat[fg], lon[fg], cursla)
        dumy = np.arange(len(dst))[(~interpolated)][dumy]
        dumsla_r = dumsla[dumy:]
        dumsla_l = dumsla[dumy:0:-1]
        nr = len(dumsla_r)
        nl = len(dumsla_l)
        acorr_l = np.zeros(nl)
        acorr_r = np.zeros(nr)
        lag_r = np.arange(nr)
        lag_l = np.arange(nl)
        for i, l in enumerate(lag_l):
            acorr_l[i] = np.corrcoef(dumsla_l, np.roll(dumsla_l, l))[0][1]

        for i, l in enumerate(lag_r):
            acorr_r[i] = np.corrcoef(dumsla_r, np.roll(dumsla_r, l))[0][1]

        zc_l = np.where(deriv(np.abs(acorr_l)) > acorr_l)[0] if nl >= 3 else []
        zc_r = np.where(deriv(np.abs(acorr_r)) > acorr_r)[0] if nr >= 3 else []
        zer_cross = []
        if len(zc_l) != 0:
            zer_cross = np.append(zer_cross, zc_l[0])
        if len(zc_r) != 0:
            zer_cross = np.append(zer_cross, zc_r[0])
        fit = np.ma.array(np.zeros((2, 2)), mask=np.ones((2, 2), dtype=bool))
        if len(zc_l) != 0:
            fit[0, :] = np.ma.array(np.polyfit(dst[zc_l[0] - 1:zc_l[0] + 1], acorr_l[zc_l[0] - 1:zc_l[0] + 1], 1), mask=np.zeros(2, dtype=bool))
        if len(zc_r) != 0:
            fit[1, :] = np.ma.array(np.polyfit(dst[zc_r[0] - 1:zc_r[0] + 1], acorr_r[zc_r[0] - 1:zc_r[0] + 1], 1), mask=np.zeros(2, dtype=bool))
        if fit.mask.sum() == 2:
            fit[fit.mask] = fit[(~fit.mask)]
            symmetric[j] = True
        diameter[j] = -(fit[0][1] / fit[0][0] + fit[1][1] / fit[1][0])

    return (diameter, symmetric)


def get_characteristics(eind, lon, lat, time, sla, wvsla, sa_spectrum, filter=40.0, p=12.0, verbose=1):
    if verbose >= 1:
        str_header = '\t===Eddy characteristics==='
        print str_header
    isort = np.argsort(time[eind[1]])
    eind[0][:] = eind[0][isort]
    eind[1][:] = eind[1][isort]
    if verbose < 2:
        warnings.simplefilter('ignore', np.RankWarning)
    amplitude = eddy_amplitude(np.sqrt(sa_spectrum), eind) * 100.0
    diameter, symmetric = decorrelation_scale(wvsla, lat, lon, eind, verbose=verbose)
    ugdiameter, relvort, ugamplitude, rk_relvort, rk_center, rk_diameter, self_advect = solid_body_scale(wvsla, lat, lon, eind, filter=filter, p=p, verbose=verbose)
    ugamplitude = ugamplitude * 100.0
    return (
     amplitude, diameter, relvort, ugdiameter, ugamplitude, rk_relvort, rk_center, rk_diameter, self_advect)