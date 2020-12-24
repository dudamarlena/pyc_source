# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rdussurget/.virtualenvs/compile.octant.UBU64/lib/python2.7/site-packages/altimetry/tools/altimetry_tools.py
# Compiled at: 2016-03-23 12:35:00
import numpy as np
try:
    import seawater.gibbs
except ImportError as e:
    pass

from altimetry.tools import deriv, calcul_distance, interp1d, loess
import matplotlib.pyplot as plt

def track_orient(x, y, orient=False):
    getorient = orient
    dxy = deriv(x, y)
    dx = np.median(deriv(x))
    dy = np.median(deriv(y))
    orient = np.arctan(dxy) if dx > 0 else np.arctan(dxy) + np.pi
    orient = np.remainder(orient, 2.0 * np.pi)
    sense = True if np.median(orient) < np.pi else False
    if getorient:
        return (sense, orient)
    else:
        return sense


def genweights(p, q, dt, error=None, n=False):
    """
    ;+
    ;   GENWEIGTHS : return optimal weigthing coefficients from Powell and Leben 2004<br />
    ;   translated from Matlab genweigths.m program to IDL<br /><br />
    ;  
    ;   Reference : Powell, B. S., et R. R. Leben (2004), An Optimal Filter for <br />
    ;   Geostrophic Mesoscale Currents from Along-Track Satellite Altimetry, <br />
    ;   Journal of Atmospheric and Oceanic Technology, 21(10), 1633-1642.
    ;   
    ; @author Renaud DUSSURGET, LEGOS/CTOH
    ; @history Created Sep. 2009 from genweights.m (Brian Powell (c) 2004, <br />
    ;   University of Colorado, Boulder)<br />
    ;-
    """
    p = np.abs(p)
    q = np.abs(q)
    if -p > q:
        raise 'genweights : P must be lesser than q'
    N = p + q
    T = N + 1
    A = np.matrix(np.zeros((T, T)))
    A[T - 1, :] = np.append(np.repeat(1.0, N), 0)
    sn = np.arange(T) - p
    sn = sn.compress(sn != 0)
    for i in np.arange(len(sn)):
        A[i, :] = np.append(1.0 / sn * (-sn[i] / 2.0), sn[i] ** 2.0 * dt ** 2.0 / 4.0)
        A[(i, i)] = -1.0

    B = np.zeros(T)
    B[N] = 1.0
    cn = np.dot(A.I, B)
    cn = np.array([ i for i in cn.flat ])
    cn = cn[0:N]
    error = np.sqrt(np.sum(cn.transpose() / (sn * dt)) ** 2.0 + np.sum((cn.transpose() / (sn * dt)) ** 2.0))
    return (
     cn, sn if n else cn)


def optimal_slope(cn, n, dt, z, i):
    """
    ;+
    ;
    ;   OPTIMAL_SLOPE : Function to compute the slope using a Powell et Leben (2004) <br />
    ;   filter with given characteristics.<br /><br />
    ;   
    ;   Reference : Powell, B. S., et R. R. Leben (2004), An Optimal Filter for <br />
    ;   Geostrophic Mesoscale Currents from Along-Track Satellite Altimetry, <br />
    ;   Journal of Atmospheric and Oceanic Technology, 21(10), 1633-1642.
    ;
    ; @param cn {in}{required}{type:NUMERIC} Filter coefficients
    ; @param n {in}{required}{type:NUMERIC} Filter indices reffered to central point<br />
    ;          (from -p to q - 0 is the center)
    ; @param dt {in}{required}{type:NUMERIC} Mean along-track grid step
    ; @param z {in}{required}{type:NUMERIC}{default:12} Along-track data of height<br />
    ;          anomalies (all dataset for current track)
    ; @param i {in}{required}{type:NUMERIC}{default:12} Index of points to use with<br />
    ;          current computation wihtin track.
    ;          
    ; @returns Optimal slope. Unit depends on distance and height anomalies units.
    ;
    ;
    ;
    ; @author Renaud DUSSURGET, LEGOS/CTOH
    ; @history Created Sep. 2009 from genweights.m (Brian Powell (c) 2004, <br />
    ;   University of Colorado, Boulder)
    ;
    ;
    ; @example dh = optimal_slope(cn,n,dt,z,id) : Compute the Optimal Slope using <br />
    ;   points in z[id], with a dt step, coefficients cn (of indices n).
    ;
    ;-
    """
    dh = np.nansum(-cn / (n * dt)) * z[i] + np.nansum(cn / (n * dt) * z[(i + n)])
    return dh


def powell_leben_filter_km(*args, **kwargs):
    """
    ;+
    ;
    ;   POWEL_LEBEN_FILTER_KM : Compute geostrophic speeds from a sea level dataset <br />
    ;   using a Powell et Leben (2004) along-track filtering to maintain measurement<br />
    ;    noise constant.<br /><br />
    ;
    ;   Reference : Powell, B. S., et R. R. Leben (2004), An Optimal Filter for <br />
    ;   Geostrophic Mesoscale Currents from Along-Track Satellite Altimetry, <br />
    ;   Journal of Atmospheric and Oceanic Technology, 21(10), 1633-1642.
    ;
    ; @param lon {in}{optional}{type:NUMERIC} longitude in degrees
    ; @param lat {in}{optional}{type:NUMERIC} latitude in degrees
    ; @param z {in}{required}{type:NUMERIC} sea level surface. Can either be absolute<br />
    ;          values (SSH) or relative values (SLA). This MUST be given in METERS.
    ; @param p {in}{optional}{type:NUMERIC}{default:12} Filter half-width BEFORE<br />
    ;          center of filtering window in KILOMETERS.
    ; @param q {in}{optional}{type:NUMERIC}{default:12} Filter half-width AFTER <br />
    ;          center of filtering window in KILOMETERS.
    ;          
    ; @returns Geostrophic velocity component, positive eastward
    ;
    ;
    ;
    ; @author Renaud DUSSURGET, LEGOS/CTOH
    ; @history Created Sep. 2009 from genweights.m (Brian Powell (c) 2004, <br />
    ;   University of Colorado, Boulder)<br />
    ;   Modified May 2010 to be compliant with 20Hz datasets (p & n can vary).<br />
    ;     Warining may also be issued for data with holes within the width of the<br />
    ;     window.<br />
    ;   Modified June 2010 to include filtering window width in KM instead of nb. of<br />
    ;     points (Equivalent btw. 1Hz and 20Hz data).<br />
    ;
    ; @uses CALCUL_DISTANCE, EXIST, GENWEIGTHS, SETINTERSECTION, SETUNION, <br />
    ;   OPTIMAL_SLOPE, GRAVITY, CORIOLIS, TRACK_ORIENT
    ;
    ; @example dummy1=powell_leben_filter_KM(lon,lat,sla,p=11,q=11) :<br />
    ;   Return along-track velocity anomalies using a 11km by 11km filter window.
    ;
    ;-
    """
    lon = args[0]
    lat = args[1]
    nu = args[2]
    dst = calcul_distance(lat, lon) * 1000.0
    n = nu.size
    p = kwargs.pop('p', 12.0)
    q = kwargs.pop('q', 12.0)
    verbose = kwargs.pop('verbose', False)
    dt = np.median(dst[1:] - dst[:-1])
    pn = np.round(p * 1000.0 / dt).astype(int)
    qn = np.round(q * 1000.0 / dt).astype(int)
    if pn + qn > n:
        raise 'Filtering window is too large wrt array length'
    cn = []
    nout = []
    pout = np.ndarray(pn + qn + 1)
    qout = np.ndarray(pn + qn + 1)
    for i in np.arange(pn):
        w, n = genweights(i, qn, dt, n=True)
        cn.append(w)
        nout.append(n)
        pout[i] = i
        qout[i] = qn

    w, n = genweights(pn, qn, dt, n=True)
    cn.append(w)
    nout.append(n)
    pout[pn] = pn
    qout[pn] = qn
    for i in np.arange(pn + 1, pn + 1 + qn):
        w, n = genweights(pn, pn + qn - i, dt, n=True)
        cn.append(w)
        nout.append(n)
        pout[i] = pn
        qout[i] = pn + qn - i

    empty = np.where(np.isnan(nu))[0]
    ok = np.where(~np.isnan(nu))[0]
    emptycnt = empty.size
    okcnt = ok.size
    st = np.min(ok)
    en = np.max(ok)
    dh = np.repeat(np.nan, nu.size)
    for i in np.arange(okcnt):
        cur = np.arange(pn + qn + 1) + ok[i] - pn
        cur = np.sort(list(set(cur).intersection(set(ok))))
        curcnt = cur.size
        if curcnt > 1:
            a = np.where(np.append(0, cur[1:] - cur[:-1]) == 1)[0]
            b = np.where(np.append(cur[:-1] - cur[1:], 0) == -1)[0]
            aftcnt = a.size
            befcnt = b.size
            if (aftcnt != 0) & (befcnt != 0):
                cur = cur[np.sort(list(set(a).union(b)))]
                curcnt = cur.size
            else:
                curcnt = 0
        else:
            curcnt = 0
        if curcnt != 0:
            nbef = ok[i] - cur[0]
            naft = cur[(curcnt - 1)] - ok[i]
            if (naft > nbef) & (naft + nbef > qn):
                naft = pn
            if (naft < nbef) & (naft + nbef > pn):
                nbef = qn
            which = np.where((nbef == pout) & (naft == qout))[0]
            nwhich = which.size
            if nwhich > 0:
                dh[ok[i]] = optimal_slope(cn[which], nout[which], dt, nu, ok[i])
            else:
                if verbose:
                    print ('[WARNING] No available filter for point no.{0}').format(ok[i])
                dh[ok[i]] = np.NaN

    g = gravity(lat)
    f = coriolis(lat)
    try:
        ug = -(g * dh) / f
    except ValueError:
        print 'error'

    if not track_orient(lon, lat):
        ug *= -1
    return ug


def coriolis(lat):
    sideral_day = 86164.1
    omega = 2.0 * np.pi / sideral_day
    return 2.0 * omega * np.sin(np.deg2rad(lat))


def gravity(*args):
    try:
        return seawater.gibbs.grav(*args)
    except:
        return np.repeat(6.67384, len(args[0]))


def geost_1d(*args, **kwargs):
    """
    ;+
    ;
    ;   GEOST_1D : Compute geostrophic speeds from a sea level dataset <br />
    ;
    ;   Reference : Powell, B. S., et R. R. Leben (2004), An Optimal Filter for <br />
    ;   Geostrophic Mesoscale Currents from Along-Track Satellite Altimetry, <br />
    ;   Journal of Atmospheric and Oceanic Technology, 21(10), 1633-1642.
    ;
    ; @param lon {in}{optional}{type:NUMERIC} longitude in degrees
    ; @param lat {in}{optional}{type:NUMERIC} latitude in degrees
    ; @param dst {in}{optional}{type:NUMERIC} along-track distance.
    ; @param z {in}{required}{type:NUMERIC} sea level surface. Can either be absolute<br />
    ;          values (SSH) or relative values (SLA). This MUST be given in METERS.
    ; @keyword strict {in}{optional}{type:BOOLEAN} If True, compute gradient at mid-distance.
    ; @keyword pl04 {in}{optional}{type:BOOLEAN} If True, use the Powell & Leben 2004 method.
    ;          
    ; @returns Geostrophic velocity component, positive eastward
    ;
    ;
    ;
    ; @author Renaud DUSSURGET, LEGOS/CTOH
    ; @history Created Sep. 2009 from genweights.m (Brian Powell (c) 2004, <br />
    ;   University of Colorado, Boulder)<br />
    ;   Modified May 2010 to be compliant with 20Hz datasets (p & n can vary).<br />
    ;     Warining may also be issued for data with holes within the width of the<br />
    ;     window.<br />
    ;   Modified June 2010 to include filtering window width in KM instead of nb. of<br />
    ;     points (Equivalent btw. 1Hz and 20Hz data).<br />
    ;
    ; @uses CALCUL_DISTANCE, EXIST, GENWEIGTHS, SETINTERSECTION, SETUNION, <br />
    ;   OPTIMAL_SLOPE, GRAVITY, CORIOLIS, TRACK_ORIENT
    ;
    ; @example dummy1=geost_1D(lon,lat,sla,pl04=True,p=11,q=11) :<br />
    ;   Return along-track velocity anomalies using a 11km by 11km Powell & Leben 2004 filter window <br />
    ;          dummy2=geost_1D(dst,sla,strict=True) :<br />
    ;   Return along-track velocity anomalies computed at mid-distance <br />
    ;
    ;-
    """
    lon = args[0]
    lat = args[1]
    dst = args[2] if len(args) == 4 else calcul_distance(lat, lon) * 1000.0
    nu = args[3] if len(args) == 4 else args[2]
    isVector = len(np.shape(nu)) == 1
    if isVector:
        nu = np.reshape(nu, (len(nu), 1))
    if not isVector:
        nt = np.shape(nu)[1] if 1 else 1
        sh = nu.shape
        nufilt = np.ma.array(np.empty(sh), mask=True, dtype=nu.dtype)
        pl04 = kwargs.pop('pl04', False)
        filter = kwargs.pop('filter', None)
        strict = kwargs.pop('strict', False)
        verbose = kwargs.pop('verbose', False)
        if filter is not None:
            for t in np.arange(nt):
                nufilt[:, t] = loess(nu[:, t], dst, filter * 1000.0)

            nu = nufilt
        if pl04:
            ug = np.ma.array(np.empty(sh), mask=True, dtype=nu.dtype)
            for t in np.arange(nt):
                ug[:, t] = powell_leben_filter_km(lon, lat, nu[:, t], verbose=verbose, **kwargs)

            if isVector:
                ug = ug.flatten()
            return ug
        if strict:
            lon = (lon[1:] - lon[:-1]) / 2.0 + lon[0:-1]
            lat = (lat[1:] - lat[:-1]) / 2.0 + lat[0:-1]
        if strict:
            sh = (sh[0] - 1, sh[1])
        g = np.repeat(gravity(lat), nt).reshape(sh)
        f = np.repeat(coriolis(lat), nt).reshape(sh)
        dh = np.ma.array(np.empty(sh), mask=True, dtype=nu.dtype)
        for t in np.arange(nt):
            dh[:, t] = (nu[1:, t] - nu[:-1, t]) / (dst[1:] - dst[:-1]) if strict else deriv(dst, nu[:, t])

        ug = -(g * dh) / f
        track_orient(lon, lat) or ug *= -1
    if isVector:
        ug = ug.flatten()
    if strict:
        return (lon, lat, ug)
    else:
        return ug


def grid_track(lat, lon, sla, remove_edges=None, backbone=None, interp_over_continents=True):
    """
    # GRID_TRACK
    # @summary: This function allow detecting gaps in a set of altimetry data and rebin this data regularly, with informations on gaps.
    # @param lat {type:numeric} : latitude
    # @param lon {type:numeric} : longitude
    # @param sla {type:numeric} : data
    # @return:
    #    outdst : resampled distance
    #    outlon : resampled longitude
    #    outlat : resampled latitude
    #    outsla : resampled data
    #    gaplen : length of the longest gap in data
    #    dx : average spatial sampling
    #    interpolated : True when data was interpolated (empty bin)
    #
    # @author: Renaud DUSSURGET (RD) - LER/PAC, Ifremer
    # @change: Created by RD, July 2012
    #    29/08/2012 : Major change -> number of output variables changes (added INTERPOLATED), and rebinning modified
    #    06/11/2012 : Included in alti_tools lib
    #    19/12/2012 : Added backbone option (reproject along the backbone grid)
    """
    if backbone is not None:
        backlon = backbone[0]
        backlat = backbone[1]
        ascending = track_orient(lon, lat)
        dst = calcul_distance(backlat[0], backlon[0], lat, lon)
        if ascending:
            dst[(lat < backlat[0])] *= -1
        if not ascending:
            dst[(lat > backlat[0])] *= -1
        dstback = calcul_distance(backlat, backlon)
        dx = dstback[1:] - dstback[:-1]
        mn_dx = np.median(dx)
        bins = np.round(dstback.max() / mn_dx) + 1
        range = (0 / 2.0, mn_dx * bins) - mn_dx / 2
        bhist, bbin_edges = np.histogram(dstback, bins=bins, range=range)
        continent = np.where(bhist == 0)[0]
        if remove_edges is None:
            remove_edges = False
    else:
        dst = calcul_distance(lat, lon)
        dx = dst[1:] - dst[:-1]
        mn_dx = np.median(dx)
        bins = np.ceil(dst.max() / mn_dx) + 1
        range = (0 / 2.0, mn_dx * bins) - mn_dx / 2
        if remove_edges is None:
            remove_edges = True
    hist, bin_edges = np.histogram(dst, bins=bins, range=range)
    if remove_edges == True:
        while hist[0] == 0:
            hist = np.delete(hist, [0])
            bin_edges = np.delete(bin_edges, [0])

        while hist[(-1)] == 0:
            hist = np.delete(hist, [len(hist) - 1])
            bin_edges = np.delete(bin_edges, [len(bin_edges) - 1])

    nH = len(hist)
    ok = np.arange(len(hist)).compress(np.logical_and(hist, True or False))
    empty = np.arange(len(hist)).compress(~np.logical_and(hist, True or False))
    if isinstance(sla, np.ma.masked_array):
        outsla = np.ma.masked_array(np.repeat(sla.fill_value, nH), mask=np.ones(nH, dtype=bool), dtype=sla.dtype)
    else:
        outsla = np.ma.masked_array(np.repeat(np.ma.default_fill_value(1.0), nH), mask=np.ones(nH, dtype=bool), dtype=np.float32)
    if isinstance(sla, np.ma.masked_array):
        outlon = np.ma.masked_array(np.repeat(lon.fill_value, nH), mask=np.ones(nH, dtype=bool), dtype=lon.dtype)
    else:
        outlon = np.ma.masked_array(np.repeat(np.ma.default_fill_value(1.0), nH), mask=np.ones(nH, dtype=bool), dtype=np.float32)
    if isinstance(sla, np.ma.masked_array):
        outlat = np.ma.masked_array(np.repeat(lat.fill_value, nH), mask=np.ones(nH, dtype=bool), dtype=lat.dtype)
    else:
        outlat = np.ma.masked_array(np.repeat(np.ma.default_fill_value(1.0), nH), mask=np.ones(nH, dtype=bool), dtype=np.float32)
    outdst = bin_edges[:-1] + mn_dx / 2
    outsla[ok] = sla
    outlon[ok] = lon
    outlat[ok] = lat
    if not interp_over_continents:
        sempty = np.sort(np.array(list(set(empty).difference(set(continent)))))
    else:
        sempty = empty.copy()
    if len(empty) > 0:
        outlon[empty] = interp1d(ok, outlon[ok], empty, kind='cubic', fill_value=lon.fill_value)
        outlat[empty] = interp1d(ok, outlat[ok], empty, kind='cubic', fill_value=lat.fill_value)
    if len(sempty) > 0:
        outsla[sempty] = interp1d(ok, outsla[ok], empty, kind=0, fill_value=sla.fill_value)
    outlon.mask[outlon.data == outlon.fill_value] = outlon.fill_value
    outlat.mask[outlat.data == outlat.fill_value] = outlat.fill_value
    outsla.mask[outsla.data == outsla.fill_value] = outsla.fill_value
    ind = np.arange(len(hist))
    dhist = hist[1:] - hist[:-1]
    if (dhist != 0).sum() > 0:
        if dhist[(dhist != 0)][0] == 1:
            dhist[np.arange(nH)[(dhist != 0)][0]] = 0
    if (dhist != 0).sum() > 0:
        if dhist[(dhist != 0)][(-1)] == -1:
            dhist[np.arange(nH)[(dhist != 0)][(-1)]] = 0
    st = ind[(dhist == -1)] + 1
    en = ind[(dhist == 1)]
    gaplen = en - st + 1
    ngaps = len(st)
    gapedges = np.array([st, en])
    interpolated = ~hist.astype('bool')
    return (
     outdst, outlon, outlat, outsla, gaplen, ngaps, gapedges, interpolated)


def grid_track_backbone(lat, lon, sla, backlat, backlon, fill=None):
    """
    # GRID_TRACK_BACKBONE
    # @summary: This function allow detecting gaps in a set of altimetry data and rebin this data regularlyy, with informations on gaps.
    # @param dst {type:numeric} : along-track distance.
    # @param lat {type:numeric} : latitude
    # @param lon {type:numeric} : longitude
    # @param sla {type:numeric} : data
    # @return:
    #    outdst : resampled distance
    #    outlon : resampled longitude
    #    outlat : resampled latitude
    #    outsla : resampled data
    #    gaplen : length of the longest gap in data
    #    ngaps : number of detected gaps in data
    #    dx : average spatial sampling
    #    interpolated : True when data was interpolated (empty bin)
    #
    # @author: Renaud DUSSURGET (RD) - LER/PAC, Ifremer
    # @change: Created by RD, July 2012
    #    29/08/2012 : Major change -> number of output variables changes (added INTERPOLATED), and rebinning modified
    """
    dst = calcul_distance(backlat[0], backlon[0], lat, lon)
    dstback = calcul_distance(backlat, backlon)
    dx = dstback[1:] - dstback[:-1]
    mn_dx = np.median(dx)
    bins = np.ceil(dstback.max() / mn_dx) + 1
    range = (0 / 2.0, mn_dx * bins) - mn_dx / 2
    hist, bin_edges = np.histogram(dst, bins=bins, range=range)
    ok = np.arange(len(hist)).compress(np.logical_and(hist, True or False))
    empty = np.arange(len(hist)).compress(~np.logical_and(hist, True or False))
    outsla = np.repeat(np.NaN, len(hist))
    outlon = np.repeat(np.NaN, len(hist))
    outlat = np.repeat(np.NaN, len(hist))
    outdst = bin_edges[:-1] + mn_dx / 2
    outsla[ok] = sla
    outlon[ok] = lon
    outlat[ok] = lat
    if (fill is not None) & (len(empty) > fill):
        outlon[empty] = interp1d(ok, outlon[ok], empty, kind='cubic')
        outlat[empty] = interp1d(ok, outlat[ok], empty, kind='cubic')
        outsla[empty] = interp1d(ok, outsla[ok], empty, spline=True)
    interpolated = ~hist.astype('bool')
    return (
     outdst, outlon, outlat, outsla, dx, interpolated)


def grid_time(time, remove_edges=False):
    """
    # GRID_TIME
    # @summary: This function allow to regularly resample time as an array in an altimetry dataset
    # @param time {type:numeric} : time
    # @return:
    #    outtime : resampled time
    #    gaplen : length of the longest gap in data
    #    ngaps : number of detected gaps in data
    #    dx : average spatial sampling
    #    interpolated : True when data was interpolated (empty bin)
    #
    # @author: Renaud DUSSURGET (RD) - LER/PAC, Ifremer
    # @change: Created by RD, July 2012
    #    29/08/2012 : Major change -> number of output variables changes (added INTERPOLATED), and rebinning modified
    #    06/11/2012 : Included in alti_tools lib
    """
    nt = time.shape[0]
    nx = time.shape[1]
    xnt = np.isfinite(time).sum(axis=0)
    xid = np.argmax(xnt)
    w = np.linalg.lstsq(np.array([np.arange(nt)[(~time.mask[:, xid])], np.ones(nt)[(~time.mask[:, xid])]]).T, time[:, xid][(~time.mask[:, xid])])[0]
    t = w[0] * np.arange(nt) + w[1]
    return t


def fill_gaps(lat, lon, sla, mask, remove_edges=False):
    """
    # FILL_GAPS
    # @summary: This function allow interpolating data in gaps, depending on gap size. Data must be regularly gridded
    # @param lat {type:numeric} : latitude
    # @param lon {type:numeric} : longitude
    # @param sla {type:numeric} : data
    # @return:
    #    outdst : resampled distance
    #    outlon : resampled longitude
    #    outlat : resampled latitude
    #    outsla : resampled data
    #    gaplen : length of the longest gap in data
    #    ngaps : number of detected gaps in data
    #    dx : average spatial sampling
    #    interpolated : True when data was interpolated (empty bin)
    #
    # @author: Renaud DUSSURGET (RD) - LER/PAC, Ifremer
    # @change: Created by RD, July 2012
    #    29/08/2012 : Major change -> number of output variables changes (added INTERPOLATED), and rebinning modified
    #    06/11/2012 : Included in alti_tools lib
    """
    dst = calcul_distance(lat, lon)
    dx = dst[1:] - dst[:-1]
    mn_dx = np.median(dx)
    nx = len(sla)
    flag = ~mask
    outsla = sla.copy()
    outlon = lon.copy()
    outlat = lat.copy()
    outind = np.arange(nx)
    first = np.where(flag)[0].min()
    last = np.where(flag)[0].max()
    if remove_edges:
        outsla = outsla[first:last + 1]
        outlon = outlon[first:last + 1]
        outlat = outlat[first:last + 1]
        outind = outind[first:last + 1]
        mask = mask[first:last + 1]
        flag = flag[first:last + 1]
    else:
        outsla[0:first] = outsla[first]
        outsla[last:] = outsla[last]
    hist = np.ones(nx, dtype=int)
    hist[outsla.mask] = 0
    while hist[0] == 0:
        hist = np.delete(hist, [0])

    while hist[(-1)] == 0:
        hist = np.delete(hist, [len(hist) - 1])

    ind = np.arange(len(hist))
    dhist = hist[1:] - hist[:-1]
    st = ind.compress(dhist == -1) + 1
    en = ind.compress(dhist == 1)
    gaplen = en - st + 1
    ngaps = len(st)
    gapedges = np.array([st, en])
    ok = np.where(flag)[0]
    empty = np.where(mask)[0]
    if len(empty) > 0:
        outsla[empty] = interp1d(ok, outsla[ok], empty)
    interpolated = ~hist.astype('bool')
    return (
     outsla, outlon, outlat, outind, ngaps, gapedges, gaplen, interpolated)


def detrend(X, Z, deg=1):
    ndims = len(Z.shape)
    isVector = False
    if ndims == 1:
        Z = np.reshape(Z, (1, Z.size))
        isVector = True
    notMa = False
    if not isinstance(Z, np.ma.masked_array):
        notMa = True
        Z = np.ma.array(Z, mask=np.zeros(Z.shape))
    nt = Z.shape[0]
    valid = (~Z.mask).sum(axis=1)
    a = np.arange(deg + 1)
    for t in np.arange(nt)[(valid > 0)]:
        fit = np.polyfit(X[(~Z[t, :].mask)], Z[t, :][(~Z[t, :].mask)], deg)
        for d in a:
            Z[t, :] -= np.power(X, a[::-1][d]) * fit[d]

    if isVector:
        Z = Z.reshape(Z.size)
    if notMa:
        return Z.data
    return Z