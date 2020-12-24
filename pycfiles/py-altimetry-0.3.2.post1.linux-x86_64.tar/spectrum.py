# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rdussurget/.virtualenvs/compile.octant.UBU64/lib/python2.7/site-packages/altimetry/tools/spectrum.py
# Compiled at: 2016-03-23 12:35:00
import numpy as np, scipy.fftpack as ft
from scipy import stats
from altimetry.tools import detrend as detrend_fun, grid_track, message
import matplotlib.pyplot as plt

def get_kx(N, dx):
    """
    GET_KX
    :summary: Returns the frequencies to be used with FFT analysis
    
    :parameter N: number of samples in data
    :parameter dx: sampling step
    
    :return: Returns
      * k: frequency
      * L: length
      * imx: index of maximum frequency (for separating positive and negative frequencies)
    
    :author: Renaud DUSSURGET (RD) - LER/PAC, Ifremer
    :change: Created by RD, July 2012
    """
    L = N * dx
    odd = N & 1 and True or False
    k = ft.fftfreq(N, d=dx)
    imx = (N - 1) / 2 if odd else N / 2
    return (
     k, L, imx)


def get_spec(dx, Vin, verbose=False, gain=1.0, integration=True):
    """
    GET_SPEC
    :summary: Returns the spectrum of a regularly sampled dataset
    
    :parameter dq: sampling interval (1D)
    :parameter V: data to analyse (1D).
    
    :note: NaN can not be used. 
    
    :return:
    
      * psd: Power Spectral Density
      * esd: Energy Spectral Density
      * fq: frequency
      * p: wavelength (period)
    
    :author: Renaud DUSSURGET (RD) - LER/PAC, Ifremer
    :change: Created by RD, July 2012. Changes
      * 29/08/2012 : Changed the computation of frequencies and the spectral integration (spectrum is averaged at mid-width frequencies)
      * 30/11/2012 : Outstanding changes : corrected the spectral integration for computing psd and corrected the normalisation
    """
    V = Vin.copy()
    N = V.size
    k, L, imx = get_kx(N, dx)
    fft = ft.fft(V) / gain
    if verbose:
        print ('Check parseval theorem 1: SUM|Y(f)|²={0}, SUM|y(t)|²={1}').format((np.abs(fft) ** 2 / N).sum(), (V ** 2).sum())
    a = fft.real
    b = fft.imag
    c = np.sqrt(a ** 2.0 + b ** 2.0)
    d = np.arctan(b / a)
    if verbose:
        print ('Check parseval theorem 2: SUM|Y(f)|²={0}, SUM|y(t)|²={1}').format((c ** 2 / N).sum(), (V ** 2).sum())
    c /= np.float32(N)
    if verbose:
        print ('Check parseval theorem 3: SUM|Y(f)|²={0}, SUM|y(t)|²={1}').format((c ** 2 * N).sum(), (V ** 2).sum())
    c = 2 * c[1:imx - 1]
    d = 2 * d[1:imx - 1]
    if verbose:
        print ('Check parseval theorem 4: SUM|Y(f)|²={0}, SUM|y(t)|²={1}').format((c ** 2 * (N / 2.0)).sum(), ((V - V.mean()) ** 2).sum())
    dk = k[1] - k[0]
    dk_half = dk / 2
    k = k[1:imx - 1]
    k_ = k[:-1] + dk_half
    csquared = c ** 2
    if verbose:
        print ('Check parseval theorem 5: SUM|Y(f)|²={0}, SUM|y(t)|²={1}').format((csquared * (N / 2)).sum(), ((V - V.mean()) ** 2).sum())
    if integration:
        esd = k_ * 0.0
        psd = k_ * 0.0
        for i in np.arange(len(k_)):
            esd[i] = np.sum((csquared * (N / 2.0))[((k > k_[i] - dk) & (k < k_[i] + dk))]) / 2.0
            psd[i] = np.sum(csquared[((k > k_[i] - dk) & (k < k_[i] + dk))]) / 4.0

        fq = k_
    else:
        esd = csquared
        psd = esd.copy() / 2.0
        fq = k.copy()
    psd = psd / dk
    if verbose:
        print ('Check parseval theorem 6: SUM|Y(f)|²={0}, SUM|y(t)|²={1}').format(esd.sum(), ((V - V.mean()) ** 2).sum())
    p = 1 / fq
    return {'psd': psd, 'esd': esd, 'fq': fq, 'p': p, 'gain': gain, 'phase': d}


def spectral_analysis(dx, Ain, tapering=None, overlap=None, wsize=None, alpha=3.0, detrend=False, normalise=False, integration=True, average=True, ARspec=None):
    """
    Spectral_Analysis :
    This function performs a spatial spectral analysis with different options on a time series of SLA profiles.
    
    :parameter dx: sampling distance
    :parameter Ain: 2D table of sla data with time along 2nd axis (NXxNT with NX the spatial length and NT the time length)
    :keyword tapering: apply tapering to the data
    
      * If this keyword is of type bool : apply hamming window.
      * If this keyword is a string : apply a hamming ('hamm'), hann ('hann'), kaiser-bessel ('kaiser'), kaiser-bessel ('blackman') or no ('none') tapering function.
      * If this keyword is an :class:`numpy.array` object : apply this array as taper.
       
    :keyword overlap: overlap coefficient of the windows (0.75 means 75% overlap).
    :keyword wsize: size of the sub-segments.
    :keyword normalise: If True, normalise the spectrum by its overall energy content.
    :keyword detrend: If True, removes a linear trend to the segmented signal (if tapered) or to the whole signal (if not tapered).
    :keyword integration: If True, integrate the spectrum between 2 frequencies.
    :keyword alpha: used to compute the input (beta) of the kaiser-bessel taper.
    :keyword ARspec: Applies an Auto-Regression model of the order provided as value of this parameter. 
    
    :return: a spectrum structure
    
       .. code-block:: python
       
          {'esd':esd,       #Energy Spectral Density
           'psd':psd,       #Power Spectral Density
           'fq':fq,         #frequency
           'p':p,           #wavelength
           'params':params} #tapering parameters.
    
    :author: Renaud DUSSURGET (RD) - LER/PAC, Ifremer
    :change: Created by RD, December 2012
    """
    A = Ain.copy()
    sh = A.shape
    ndims = len(sh)
    N = sh[0]
    if ndims == 1:
        A = A.reshape((N, 1))
        sh = A.shape
        ndims = len(sh)
    nr = sh[1]
    nt = nr
    if tapering is not None:
        overlap = 0 if overlap is None else overlap
        wsize = N if wsize is None else wsize
        a = np.float32(wsize)
        b = np.float32(overlap)
        c = np.float32(N)
        nn = np.floor((c - a * b) / (a - a * b))
        print ('Number of windows :{0}\nTotal windowed points : {1} ({2} missing)\nTotal points : {3}').format(nn, nn * wsize, N - nn * wsize * overlap, N)
        ix = np.arange(nn) * ((1.0 - b) * a)
        dum = np.zeros((wsize, nn, nr), dtype=np.float64)
        for j in np.arange(nr):
            for i in np.arange(nn):
                dum[:, i, j] = detrend_fun(np.arange(wsize), A[ix[i]:ix[i] + wsize, j]) if detrend else A[ix[i]:ix[i] + wsize, j]

        beta = np.pi * alpha
        hamm = np.hamming(wsize)
        hann = np.hanning(wsize)
        kbess = np.kaiser(wsize, beta)
        blackman = np.blackman(wsize)
        notaper = np.ones(wsize)
        gain = 1.0
        if isinstance(tapering, bool):
            which = 'hamm'
        elif isinstance(tapering, str):
            if tapering.upper() == 'HAMMING':
                which = 'hamm'
                gain = np.sum(hamm) / wsize
            elif tapering.upper() == 'HANNING':
                which = 'hann'
                gain = np.sum(hann) / wsize
            elif tapering.upper() == 'KAISER':
                which = 'kbess'
                gain = np.sum(kbess) / wsize
            elif tapering.upper() == 'NONE':
                which = 'notaper'
                gain = 1.0
            elif tapering.upper() == 'BLACKMAN':
                which = 'blackman'
                gain = np.sum(blackman) / wsize
            else:
                raise Exception(('Unknown taper {0}').format(tapering))
        elif isinstance(tapering, np.ndarray):
            which = 'tapering'
            gain = np.sum(tapering) / wsize
        else:
            raise Exception('Bad value for tapering keyword')
        exec 'window=' + which
        window = np.repeat(window, nn * nr).reshape((wsize, nn, nr))
        A = dum.copy() * window
        A = A.reshape(wsize, nr * nn)
        nr = nn * nr
    else:
        if detrend:
            for i in np.arange(nr):
                A[:, i] = detrend_fun(np.arange(N), A[:, i]) if detrend else A[:, i]

        gain = 1.0
    for i in np.arange(nr):
        if ARspec is not None:
            spec = yule_walker_regression(dx, A[:, i], ARspec)
        else:
            spec = get_spec(dx, A[:, i], integration=integration, gain=gain)
        if i == 0:
            esd = spec['esd']
            psd = spec['psd']
            fq = spec['fq']
            phase = spec['phase']
            if ARspec:
                model = spec['psd'].model
        else:
            esd = np.append(esd, spec['esd'])
            psd = np.append(psd, spec['psd'])
            phase = spec['phase']
            if ARspec:
                model = np.append(model, spec['psd'].model)

    nf = len(fq)
    p = 1.0 / fq
    esd = esd.reshape(nr, nf)
    psd = psd.reshape(nr, nf)
    if average:
        esd = np.sum(esd, axis=0) / nr
        psd = np.sum(psd, axis=0) / nr
    psd = psd * gain ** 0.5
    if ARspec:
        mparam, msig = zip(*tuple([ (el['parameters'], el['sig']) for el in model ]))
        deg = ARspec
        mparam = np.concatenate(mparam).reshape((len(model), deg))
        msig = np.array(msig)
        if average:
            mparam = mparam.mean(axis=0)
            msig = np.nansum(msig) / msig.size
        mstr = {'parameters': mparam, 'sig': msig, 'n': N, 'deg': ARspec}
        setattr(esd, 'model', mstr)
        setattr(psd, 'model', mstr)
    Scaling_Factor = len(fq) / esd.sum()
    if normalise:
        esd *= Scaling_Factor
        psd *= Scaling_Factor
    if tapering is not None:
        return {'params': {'tapering': tapering is not None, 'which': which, 'wsize': int(wsize), 'nwind': int(nn), 'overlap': int(100.0 * overlap), 'gain': gain}, 'psd': psd, 'esd': esd, 'fq': fq, 'p': p, 'phase': phase}
    else:
        return {'params': {'tapering': tapering is not None}, 'psd': psd, 'esd': esd, 'fq': fq, 'p': p, 'phase': phase}
        return


def preprocess(lat, lon, sla, N_min=None, per_min=15.0, max_gap=None, leave_gaps=False, remove_edges=True, interp_over_continents=False, truncate_if_continents=True, discard_continental_gaps=True, flag_interp=False, return_lonlat=False, return_interpolated=False, last=True, mid=None, first=None, verbose=1):
    """   
    Preprocessing of the SLA data ::
       * process positions :
          * interpolate over gaps
          * find continents (extend the positions over continents to get the discontinuity)
          * find track edges
          * find gap lengths

       * clean SLA data::
          * Remove gaps greater than maximum allowed length over which interpolate is OK.
          * Remove time steps with not enough coverage
          * get sub-segments of valid data of a given length
          
    :parameter lon: longitude
    :parameter lat: longitude
    :parameter sla: data
    
    :keyword N_min: Length of subsegments (cf :func:`altimetry.tools.spectrum.get_segments`)
    :keyword per_min: Minimum percentage of valid data to allow.
    :keyword max_gap: Maximum gap length to interpolate over (interpolation is done 1st, THEN long gaps are eliminated)
    :keyword leave_gaps: Leave gaps (equivalent to setting max_gap to number of points in track).
    
    :keyword remove_edges: discard data at track edges.
    :keyword truncate_if_continents: Force truncating data if a continent is found within a segment of data.
    :keyword last: Get segments of data sticked to the last point in track (cf :func:`altimetry.tools.spectrum.get_segments`)
    :keyword first: Get segments of data sticked to the first point in track (cf :func:`altimetry.tools.spectrum.get_segments`)
    :keyword mid: Get segments of data sticked to the middle point in track (cf :func:`altimetry.tools.spectrum.get_segments`)
    
    """
    sh = sla.shape
    nt = sh[0]
    nx = sh[1]
    dumsla = sla.copy()
    ok = np.where(sla.mask.sum(axis=1) < nx - 3)[0]
    if nt != len(ok):
        message(2, '%i time steps on %i removed: contain less than 3 valid data points' % (nt - len(ok), nt), verbose=verbose)
    dumsla = dumsla[ok, :]
    ntinit = nt
    nt = len(ok)
    fg_dumlon = nx
    for i in np.arange(nt):
        fg = ~dumsla.mask[i, :]
        dst, dumlon, dumlat, dsla, lgaps, n, edges, inter = grid_track(lat[fg], lon[fg], dumsla[i, :][fg], remove_edges=False, backbone=[lon, lat], interp_over_continents=interp_over_continents)
        if isinstance(dumlon, np.ma.masked_array):
            fg_dumlon_new = dumlon.mask.sum()
        else:
            fg_dumlon_new = np.isfinite(dumlon).sum()
        if fg_dumlon_new < fg_dumlon:
            fg_dumlon = fg_dumlon_new
            lonout = dumlon
            latout = dumlat
        if (len(dumlon) > len(lon)) & (i == 0):
            lendiff = len(dumlon) - len(lon)
            print ('[WARNING] : Pass goes over a land mass, changing the track size from {0} to {1}').format(nx, nx + lendiff)
            nx += lendiff
        dumint = inter.reshape((1, len(dsla))) if i == 0 else np.ma.concatenate([dumint, inter.reshape((1, len(dsla)))], axis=0)
        dumslaout = dsla.reshape((1, len(dsla))) if i == 0 else np.ma.concatenate([dumslaout, dsla.reshape((1, len(dsla)))], axis=0)
        if i == 0:
            gaplen = [
             lgaps]
            gapedges = [edges]
        else:
            gaplen.append(lgaps)
            gapedges.append(edges)
        ngaps = n if i == 0 else np.append(ngaps, n)

    dumsla = dumslaout.copy()
    dumint = dumint.astype(bool)
    continent = dumsla.mask & dumint
    flagged = dumint.astype(bool) & ~continent
    iscont = np.sum(continent, axis=0) == nt
    indcont = np.arange(nx)[iscont]
    cont_gap = [ [ len(set(indcont).intersection(range(gapedges[j][0][jj], gapedges[j][1][jj]))) > 0 for jj in xrange(ngaps[j]) ] for j in xrange(nt) ]
    if discard_continental_gaps:
        gaplen = [ np.array([ g[jj] for jj in xrange(len(g)) if not cont_gap[j][jj] ]) for j, g in enumerate(gaplen) ]
    if max_gap is not None:
        gapmax = np.array([ np.max(g) if len(g) > 0 else 0 for g in gaplen ])
        id1 = (leave_gaps or np.where(gapmax <= max_gap))[0] if 1 else ok
        if len(id1) == 0:
            raise Exception('[ERROR] : All gaps in current track are greater than the maximum specified gap')
        if len(id1) != nt:
            message(2, '%i time steps on %i removed: gaps > %i point' % (nt - len(id1), ntinit, int(max_gap)), verbose=verbose)
        dumsla = dumsla[id1, :]
        per = 100.0 * flagged[id1, :].sum(axis=1) / np.float(nx)
        if N_min is None:
            N_min = nx
        id2 = np.where(per <= per_min)[0]
        if len(id2) == 0:
            raise Exception('[ERROR] : All time steps in current track have a percentage of invalid data > than the maximum allowed (%i)' % int(per_min))
        if len(id2) != len(id1):
            message(2, '%i time steps on %i removed: exceed maximum allowed percentage of invalid data (%i)' % (len(id1) - len(id2), ntinit, int(per_min)), verbose=verbose)
        dumsla = dumsla[id2, :]
        dumsla, id3 = get_segment(dumsla, N_min, remove_edges=remove_edges, truncate_if_continents=truncate_if_continents, last=last, mid=mid, first=first)
        if len(id3) == 0:
            raise Exception('[ERROR] : Remaining time steps do not reach the minimum length of %i points' % int(N_min))
        if len(id3) != len(id2):
            message(2, '%i time steps no reaching rhe minimum length of %i points have been removed)' % (len(id2) - len(id3), int(N_min)), verbose=verbose)
        res = (
         dumsla, ok[id1[id2[id3]]])
    else:
        res = (dumsla, ngaps, gaplen)
    nt = res[0].shape[0]
    if nt != ntinit:
        message(1, '%i time steps on %i removed by data pre-processing' % (ntinit - nt, ntinit), verbose=verbose)
    if return_lonlat:
        res += (lonout, latout)
    if return_interpolated:
        res += (dumint,)
    return res


def get_segment(sla, N, last=True, mid=None, first=None, remove_edges=True, truncate_if_continents=True):
    """
    Intelligent segmentation of data.
    
    :keyword remove_edges: discard data at track edges.
    :keyword truncate_if_continents: Force truncating data if a continent is found within a segment of data.
    
    :keyword last: Get segments of data sticked to the last point in track
    :keyword first: Get segments of data sticked to the first point in track
    :keyword mid: Get segments of data sticked to the middle point in track

    """
    if first is not None:
        last = None
        mid = None
    else:
        if mid is not None:
            last = None
            first = None
        dumsla = sla.copy()
        nx = sla.shape[1]
        nt = sla.shape[0]
        dumsla.data[dumsla.mask] = dumsla.fill_value
        if len(dumsla.mask.shape) > 0:
            mask = np.ma.array(dumsla.mask.copy(), mask=np.zeros(sla.shape, dtype=bool))
        else:
            mask = np.array([dumsla.mask] * sla.size).reshape(sla.shape)
            mask = np.ma.array(mask, mask=np.zeros(sla.shape, dtype=bool))
            dumsla.mask = mask
        if remove_edges:
            xid = np.ma.array(np.repeat(np.arange(nx), nt).reshape(nx, nt).transpose(), mask=mask.data)
        else:
            xid = np.ma.array(np.repeat(np.arange(nx), nt).reshape(nx, nt).transpose(), mask=np.zeros(sla.shape, dtype=bool))
        left = xid.min(axis=1)
        right = xid.max(axis=1)
        if last:
            st = (right - N).astype(int) + 1
            en = right.astype(int) + 1
        elif mid:
            midpt = nx / 2
            rlag = right - midpt
            llag = midpt - left
            odd = np.int(N) & 1 and True or False
            if not odd:
                nr = nl = np.int(N) / 2
            else:
                nr = np.int(N) / 2 + 1
                nl = np.int(N) / 2
            st = np.repeat(midpt - nl, nt)
            en = np.repeat(midpt + nr, nt)
        elif first:
            st = left.astype(int)
            en = (left + N).astype(int)
        if not remove_edges:
            st[st < 0] = 0
            en[en > nx] = nx
        for i in np.arange(nt):
            dumsla.mask[i, :st[i]] = True
            dumsla.mask[i, en[i]:] = True
            mask.mask[i, :st[i]] = True
            mask.mask[i, en[i]:] = True

    cycempty = dumsla.mask.sum(axis=1) == N
    ind = np.arange(nt)[(~cycempty)]
    nt = (~cycempty).sum()
    dumsla = dumsla.compressed().reshape(nt, N)
    mask = mask.compressed().reshape(nt, N)
    if truncate_if_continents:
        empty = mask.sum(axis=0) == nt
        if empty.sum() > 0:
            dumsla = dumsla[:, ~empty]
            mask = mask[:, ~empty]
            print ('[WARNING] Points over land mass - removed {} pts').format(empty.sum())
    return (
     np.ma.array(dumsla, mask=mask), ind)


def get_slope(fq, spec, degree=1, frange=None, threshold=0.0):
    """
    
    GET_SLOPE
    :summary: This function returns the spectral slope of a spectrum using a least-square regression 
    
    :parameter fq: frequency
    :parameter spec: spectrum data
    
    :keyword degree: Degree of the least-square regression model 
    
    :return:
      * slope : spectral slope (or model coefficients for a higher order model)
      * intercept : Energy at unit frequency (1 cpkm)
    
    :author: Renaud DUSSURGET (RD) - LER/PAC, Ifremer
    :change: Created by RD, August 2012
    """
    sh = spec.shape
    ndims = len(sh)
    if ndims == 1:
        x = np.log10(fq).flatten()
        y = np.log10(spec).flatten()
        if degree == 1:
            slope, intercept, rval, pval, err = stats.linregress(x, y)
        else:
            A = np.vander(x, degree + 1)
            coeffs, residuals, rank, sing_vals = np.linalg.lstsq(A, y)
            slope[:(-1)], intercept = coeffs
        return (
         slope, intercept)
    else:
        x = np.log10(fq[((fq > np.min(frange)) & (fq <= np.max(frange)))]).flatten()
        y = np.log10(spec[(fq > np.min(frange)) & (fq <= np.max(frange)), :])
        nx = len(x)
        nt = sh[1]
        degree = 1
        out = []
        for i in np.arange(nt):
            slope, intercept, rval, pval, err = stats.linregress(x, y[:, i])
            flag = y.mask[:, i].sum(dtype=float) / nx <= threshold
            if i == 0:
                out.append((slope, intercept, flag))
            else:
                out.append((slope, intercept, flag))

        return out


def yule_walker(acf, orden):
    """
    Program to solve Yule-Walker equations for AutoRegressive Models
    
    :author: XAVI LLORT (llort(at)grahi.upc.edu)
    :created: MAY 2007
    :changes: adapted to python by R.Dussurget

    :parameter acf: AutoCorrelation Function
    :parameter orden: Order of the AutoRegressive Model
    :return:
      * parameters : Parameters
      * sigma_e : Standard deviation of the noise term
    """
    if len(acf) + 1 <= orden:
        raise Exception('ACF too short for the solicited order!')
    bb = acf[1:orden + 1]
    aa = np.zeros((orden, orden))
    for ii in np.arange(0, orden):
        for jj in np.arange(0, orden):
            aa[(ii, jj)] = acf[np.int(np.abs(ii - jj))]

    aa_1 = np.linalg.inv(aa)
    parameters = np.ma.dot(bb, aa_1)
    import warnings
    warnings.filterwarnings('error')
    try:
        s = acf[0] - np.sum(parameters * bb)
        sigma_e = np.sqrt(s)
    except RuntimeWarning:
        print 'Warning : bad parameters - spectrum not computed'
        sigma_e = np.nan

    return (
     parameters, sigma_e)


def ARspec(F, deg, a, sig):
    sh = F.shape
    if len(sh) == 1:
        NF, nt = sh, 1
        F.reshape(NF, nt)
        a.reshape(NF, nt)
    else:
        NF, nt = sh
    p = np.arange(1, deg + 1)
    arspec = np.ma.masked_array(np.ones((NF, nt)), mask=False)
    sig = np.ma.array(sig, mask=np.isnan(sig))
    for ii in xrange(nt):
        for f in np.arange(NF, dtype=int):
            arspec[(f, ii)] = sig[ii] ** 2 / np.abs(1.0 - np.sum(a[(ii, p - 1)] * np.exp(-2.0 * np.pi * complex(0.0, 1.0) * p * F[(f, ii)]))) ** 2

    if len(sh) == 1:
        arspec = np.squeeze(arspec)
    return arspec


def yule_walker_regression(dx, Y, deg, res=None):
    """
    :parameter X: time vector (disabled)
    :parameter Y: stationary time series
    :parameter deg: AR model degree
    :return:
      * a : Yule Walker parameters
      * sig : Standard deviation of the noise term
      * aicc : corrected Akaike Information Criterion
      * gamma : Autocorrelation function
      * ar : Fitted function
      * argamma : Fitted autocorrelation function
      * arspec : Fitted spectral model
      * F : Relative frequency

    .. note:: To know more about yule-walker and autoregressive methods, see
    
      * `Example of AR(p) model auto-regression using yule-walker equations <http://www-ssc.igpp.ucla.edu/personnel/russell/ESS265/Ch9/autoreg/node7.html>`_
      * `Other notes on the autoregressive method <http://www.ee.lamar.edu/gleb/adsp/Lecture%2009%20-%20Parametric%20SE.pdf>`_

    :example: IDL example :
       
       .. code-block:: IDL
      
          #Define an n-element vector of time-series samples  
          X = [6.63, 6.59, 6.46, 6.49, 6.45, 6.41, 6.38, 6.26, 6.09, 5.99, $  
              5.92, 5.93, 5.83, 5.82, 5.95, 5.91, 5.81, 5.64, 5.51, 5.31, $  
              5.36, 5.17, 5.07, 4.97, 5.00, 5.01, 4.85, 4.79, 4.73, 4.76]  
          
          #Compute auto_correlation function
          acorr=A_CORRELATE(X,INDGEN(30))
          
          #Solve YW equation to get auto-regression coefficients for AR(2) model
          YULE_WALKER, acorr, 2, a, sig
          
          #Process auto-regression model
          ar=DBLARR(28)
          FOR i = 2, 29 DO ar[i-2] = SQRT(a[0]*X[i-1]*X[i] + a[1]*x[i-2]*x[i]+sig*x[i])
          
          #Compute spectrum
          spec=spectrogram(TRANSPOSE(X), INDGEN(N), WSIZE=N, OVERLAY=1.0, DISPLAY_IMAGE=0)
          
          #Compute AR(2) model spectrum
          ar2=spectrogram(TRANSPOSE(ar), INDGEN(28), WSIZE=28, OVERLAY=1.0, DISPLAY_IMAGE=0)
          
    """
    a = 0
    sig = 0
    if res is None:
        res = 1.0
    Y -= np.mean(Y)
    N = len(Y)
    gamma = np.zeros(N)
    lag = np.arange(N)
    for i, l in enumerate(lag):
        gamma[i] = np.corrcoef(Y, np.roll(Y, l))[0][1]

    odd = N & 1 and True or False
    F, L, imx = get_kx(N, 1)
    Fout, L, imx = get_kx(N, dx)
    F = F[1:imx - 1]
    Fout = Fout[1:imx - 1]
    NF = len(F)
    df = F[1] - F[0]
    dfout = Fout[1] - Fout[0]
    a, sig = yule_walker(gamma, deg)
    ar = np.ma.masked_array(np.zeros(N), mask=np.zeros(N, dtype=bool))
    argamma = np.ma.masked_array(np.zeros(N), mask=np.zeros(N, dtype=bool))
    arspec = np.ma.masked_array(np.ones(NF), mask=np.zeros(NF, dtype=bool))
    ar[0:deg].mask = True
    argamma[0:deg].mask = True
    p = np.arange(1, deg + 1)
    for t in np.arange(deg, N, dtype=int):
        ar[t] = np.sum(a * Y[(t - p)])
        argamma[t] = np.sum(a * gamma[(t - p)])

    for t in np.arange(NF, dtype=int):
        try:
            arspec[t] = sig ** 2 / np.abs(1.0 - np.sum(a[(p - 1)] * np.exp(-2.0 * np.pi * complex(0.0, 1.0) * p * F[t]))) ** 2
        except ValueError:
            pass

    arspec = arspec
    fac = np.ma.array(len(F)) / arspec.sum()
    arspec /= fac
    esd = arspec
    psd = arspec / dfout
    logf = np.ma.log if isinstance(arspec, np.ma.masked_array) else np.log
    aicc = N * (logf(sig ** 2) + 1) + 2 * (deg + 1) * (N / (N - deg - 2))
    aic = N * (logf(2 * sig ** 2) + 1) + 2 * deg
    bic = N * logf(sig ** 2) + deg * logf(N)
    params = {'description': 'AR model parameters', 'parameters': a, 'sig': sig, 'deg': deg, 'n': N, 'aicc': aicc, 'aic': aic, 'bic': bic}
    setattr(psd, 'model', params)
    setattr(esd, 'model', params)
    setattr(ar, 'model', params)
    outStr = {'_dimensions': {'_ndims': 3, 'N': N, 'NF': NF, 'P': deg}, 'fq': Fout, 
       'ar': ar, 
       'esd': esd, 
       'psd': psd}
    return outStr


def optimal_AR_spectrum(dx, Y, ndegrees=None, return_min=True):
    """
    Get the optimal order AR spectrum by minimizing the BIC.
    """
    if ndegrees is None:
        ndegrees = len(Y) - ndegrees
    aicc = np.arange(ndegrees)
    aic = aicc.copy()
    bic = aicc.copy()
    tmpStr = []
    for i in np.arange(1, ndegrees):
        dum = yule_walker_regression(dx, Y, i)
        tmpStr.append(dum)
        aicc[i - 1] = tmpStr[(i - 1)]['esd'].model['aicc']
        aic[i - 1] = tmpStr[(i - 1)]['esd'].model['aic']
        bic[i - 1] = tmpStr[(i - 1)]['esd'].model['bic']

    if return_min:
        return np.argmin(bic) + 1
    else:
        return {'aicc': aicc, 'aic': aic, 'bic': bic}
        return