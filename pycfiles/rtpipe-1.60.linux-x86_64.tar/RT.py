# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbe-master/realfast/anaconda/envs/deployment/lib/python2.7/site-packages/rtpipe/RT.py
# Compiled at: 2017-06-21 14:37:45
import os, glob, logging, cPickle as pickle
from functools import partial
import random, math, multiprocessing as mp, multiprocessing.sharedctypes as mps
from contextlib import closing
import numpy as n
from scipy.special import erf
import scipy.stats.mstats as mstats, rtpipe.parsems as pm, rtpipe.parsecal as pc, rtpipe.parsesdm as ps
from rtpipe.version import __version__
import rtlib_cython as rtlib, pyfftw
try:
    import casautil
except ImportError:
    import pwkit.environments.casa.util as casautil

qa = casautil.tools.quanta()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.captureWarnings(True)
logger = logging.getLogger('rtpipe')

def pipeline(d, segments):
    """ Transient search pipeline running on single node.
    Processes one or more segments of data (in which a single bgsub, (u,v,w), etc. can be used).
    Can search completely, independently, and saves candidates.
    If segments is a list of segments, then it will parallelize read/search processes.

    Stages:
    0) Take dictionary that defines metadata and search params
    -- This defines state of pipeline, including times, uv extent, pipeline search parameters, etc.
    1) Read data
    -- Overlapping reads needed to maintain sensitivity to all DMs at all times
    2) Prepare data
    -- Reads/applies telcal/CASA solutions, flags, bg time subtraction
    3) Search using all threads
    -- Option for plug-and-play detection algorithm and multiple filters
    4) Save candidate and noise info, if requested
    """
    if type(segments) == int:
        segments = [
         segments]
    logger.info('Starting search of %s, scan %d, segments %s' % (d['filename'], d['scan'], str(segments)))
    assert os.path.exists(d['gainfile']), ('Calibration file autodetection failed for gainfile {0}').format(d['gainfile'])
    random.seed()
    data_read_mem = mps.Array(mps.ctypes.c_float, datasize(d) * 2)
    data_mem = mps.Array(mps.ctypes.c_float, datasize(d) * 2)
    u_read_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    u_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    v_read_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    v_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    w_read_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    w_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    data = numpyview(data_mem, 'complex64', datashape(d))
    data_read = numpyview(data_read_mem, 'complex64', datashape(d))
    u = numpyview(u_mem, 'float32', d['nbl'], raw=False)
    v = numpyview(v_mem, 'float32', d['nbl'], raw=False)
    w = numpyview(w_mem, 'float32', d['nbl'], raw=False)
    logger.debug('Planning FFT...')
    arr = pyfftw.empty_aligned((d['npixx'], d['npixy']), dtype='complex64', n=16)
    arr[:] = n.random.randn(*arr.shape) + complex(0.0, 1.0) * n.random.randn(*arr.shape)
    fft_arr = pyfftw.interfaces.numpy_fft.ifft2(arr)
    results = {}
    with closing(mp.Pool(1, initializer=initread, initargs=(data_read_mem, u_read_mem, v_read_mem, w_read_mem, data_mem, u_mem, v_mem, w_mem))) as (readpool):
        try:
            for segment in segments:
                assert segment in range(d['nsegments']), 'Segment %d not in range of %d nsegments' % (segment, d['nsegments'])
                candsfile = getcandsfile(d, segment)
                if d['savecands'] and os.path.exists(candsfile):
                    logger.error('candsfile %s already exists. Ending processing...' % candsfile)
                else:
                    results[segment] = readpool.apply_async(pipeline_dataprep, (d, segment))

            while results.keys():
                for segment in results.keys():
                    if results[segment].ready():
                        job = results.pop(segment)
                        d = job.get()
                    else:
                        continue
                    with data_mem.get_lock():
                        cands = search(d, data_mem, u_mem, v_mem, w_mem)
                    if d['savecands']:
                        logger.info('Saving %d candidates for segment %d...' % (
                         len(cands), segment))
                        savecands(d, cands)

        except KeyboardInterrupt:
            logger.error('Caught Ctrl-C. Closing processing pool.')
            readpool.terminate()
            readpool.join()
            raise


def pipeline_dataprep(d, segment):
    """ Single-threaded pipeline for data prep that can be started in a pool.
    """
    logger.debug('dataprep starting for segment %d' % segment)
    d['segment'] = segment
    data_read = numpyview(data_read_mem, 'complex64', datashape(d), raw=False)
    data = numpyview(data_mem, 'complex64', datashape(d), raw=False)
    u_read = numpyview(u_read_mem, 'float32', d['nbl'], raw=False)
    u = numpyview(u_mem, 'float32', d['nbl'], raw=False)
    v_read = numpyview(v_read_mem, 'float32', d['nbl'], raw=False)
    v = numpyview(v_mem, 'float32', d['nbl'], raw=False)
    w_read = numpyview(w_read_mem, 'float32', d['nbl'], raw=False)
    w = numpyview(w_mem, 'float32', d['nbl'], raw=False)
    with data_read_mem.get_lock():
        if d['dataformat'] == 'ms':
            segread = pm.readsegment(d, segment)
            data_read[:] = segread[0]
            u_read[:], v_read[:], w_read[:] = segread[1][(d['readints'] / 2)], segread[2][(d['readints'] / 2)], segread[3][(d['readints'] / 2)]
            del segread
        else:
            if d['dataformat'] == 'sdm':
                data_read[:] = ps.read_bdf_segment(d, segment)
                u_read[:], v_read[:], w_read[:] = ps.get_uvw_segment(d, segment)
            if os.path.exists(d['gainfile']):
                try:
                    radec = ()
                    spwind = []
                    calname = ''
                    if '.GN' in d['gainfile']:
                        if d.has_key('calname'):
                            calname = d['calname']
                        sols = pc.telcal_sol(d['gainfile'])
                    else:
                        if d.has_key('calradec'):
                            radec = d['calradec']
                        spwind = d['spw']
                        sols = pc.casa_sol(d['gainfile'], flagants=d['flagantsol'])
                        sols.parsebp(d['bpfile'])
                    sols.set_selection(d['segmenttimes'][segment].mean(), d['freq'] * 1000000000.0, rtlib.calc_blarr(d), calname=calname, pols=d['pols'], radec=radec, spwind=spwind)
                    sols.apply(data_read)
                except:
                    logger.warning('Could not parse or apply gainfile %s.' % d['gainfile'])
                    raise

            else:
                logger.warn('Calibration file not found. Proceeding with no calibration applied.')
            if len(d['flaglist']):
                logger.info('Flagging with flaglist: %s' % d['flaglist'])
                dataflag(d, data_read)
            else:
                logger.warn('No real-time flagging.')
            if d['timesub'] == 'mean':
                logger.info('Subtracting mean visibility in time...')
                rtlib.meantsub(data_read, [0, d['nbl']])
            else:
                logger.warn('No mean time subtraction.')
            if d['savenoise']:
                noisepickle(d, data_read, u_read, v_read, w_read, chunk=200)
            try:
                if any([d['l1'], d['m1']]):
                    logger.info('Rephasing data to (l, m)=(%.4f, %.4f).' % (d['l1'], d['m1']))
                    rtlib.phaseshift_threaded(data_read, d, d['l1'], d['m1'], u_read, v_read)
                    d['l0'] = d['l1']
                    d['m0'] = d['m1']
                else:
                    logger.debug('Not rephasing.')
            except KeyError:
                pass

        if d['mock']:
            falsecands = {}
            datamid = n.ma.masked_equal(data_read[(d['readints'] / 2)].real, 0, copy=True)
            madstd = 1.4826 * n.ma.median(n.abs(datamid - n.ma.median(datamid))) / n.sqrt(d['npol'] * d['nbl'] * d['nchan'])
            std = datamid.std() / n.sqrt(d['npol'] * d['nbl'] * d['nchan'])
            logger.debug(('Noise per vis in central int: madstd {}, std {}').format(madstd, std))
            dt = 1
            if isinstance(d['mock'], int):
                for i in n.random.randint(d['datadelay'][(-1)], d['readints'], d['mock']):
                    loff, moff, A, DM = make_transient(madstd, max(d['dmarr']), Amin=1.2 * d['sigma_image1'])
                    candid = (int(segment), int(i), DM, int(dt), int(0))
                    falsecands[candid] = [A / madstd, A, loff, moff]

            else:
                if isinstance(d['mock'], list):
                    for mock in d['mock']:
                        try:
                            i, DM, loff, moff, SNR = mock
                            candid = (int(segment), int(i), DM, int(dt), int(0))
                            falsecands[candid] = [SNR, SNR * madstd, loff, moff]
                        except:
                            logger.warn(('Could not parse mock parameters: {}').format(mock))

                else:
                    logger.warn('Not a recognized type for mock.')
                for candid in falsecands:
                    segment, i, DM, dt, beamnum = candid
                    SNR, A, loff, moff = falsecands[candid]
                    logger.info('Adding mock transient at int %d, DM %.1f, (l, m) = (%f, %f) at est SNR %.1f' % (i, DM, loff, moff, SNR))
                    add_transient(d, data_read, u_read, v_read, w_read, loff, moff, i, A, DM, dt)

            if d['savecands']:
                savecands(d, falsecands, domock=True)
        with data_mem.get_lock():
            data[:] = data_read[:]
            u[:] = u_read[:]
            v[:] = v_read[:]
            w[:] = w_read[:]
    logger.debug('All data unlocked for segment %d' % segment)
    return d


def pipeline_reproduce(d, candloc=[], segment=None, lm=None, product='data'):
    """ Reproduce data and/or candidates with given candloc or lm coordinate.

    d and segment can be given, if only reading data.
    candloc is length 5 or 6 with ([scan], segment, candint, dmind, dtind, beamnum).
    product can be 'data', 'dataph', 'imdata', 'datacorr'.
    lm is tuple of (l,m) coordinates in radians.
    """
    data_reproduce_mem = mps.Array(mps.ctypes.c_float, datasize(d) * 2)
    data_read_mem = mps.Array(mps.ctypes.c_float, datasize(d) * 2)
    data_mem = mps.Array(mps.ctypes.c_float, datasize(d) * 2)
    u_read_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    u_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    v_read_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    v_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    w_read_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    w_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    data = numpyview(data_mem, 'complex64', datashape(d))
    data_read = numpyview(data_read_mem, 'complex64', datashape(d))
    u = numpyview(u_mem, 'float32', d['nbl'], raw=False)
    v = numpyview(v_mem, 'float32', d['nbl'], raw=False)
    w = numpyview(w_mem, 'float32', d['nbl'], raw=False)
    if len(candloc) == 6:
        scan, segment, candint, dmind, dtind, beamnum = candloc
    else:
        if len(candloc) == 5:
            segment, candint, dmind, dtind, beamnum = candloc
        else:
            if isinstance(segment, int):
                assert product == 'data', 'If only providing segment, then only data product can be produced.'
            else:
                logger.error('candloc must be length 5 or 6 or segment provided.')
                return
            with closing(mp.Pool(1, initializer=initread, initargs=(data_read_mem, u_read_mem, v_read_mem, w_read_mem, data_mem, u_mem, v_mem, w_mem))) as (readpool):
                readpool.apply(pipeline_dataprep, (d, segment))
            if product == 'data':
                logger.info('Returning prepared data...')
                return data
            if product == 'dataph':
                logger.info('Reproducing data and phasing...')
                assert lm, 'lm must be tuple with (l, m) coords in radians.'
                data = runreproduce(d, data_mem, data_reproduce_mem, u, v, w, dmind, dtind, lm=lm)
                return data
            if product == 'datacorr':
                logger.info('Reproducing data...')
                data = runreproduce(d, data_mem, data_reproduce_mem, u, v, w, dmind, dtind)
                return data
        if product == 'imdata':
            logger.info('Reproducing candidate...')
            im, data = runreproduce(d, data_mem, data_reproduce_mem, u, v, w, dmind, dtind, candint=candint)
            return (
             im, data)
    logger.error('product must be data, dataph, or imdata.')


def meantsubpool(d, data_read):
    """ Wrapper for mean visibility subtraction in time.
    Doesn't work when called from pipeline using multiprocessing pool.
    """
    logger.info('Subtracting mean visibility in time...')
    data_read = numpyview(data_read_mem, 'complex64', datashape(d))
    tsubpart = partial(rtlib.meantsub, data_read)
    blranges = [ (d['nbl'] * t / d['nthread'], d['nbl'] * (t + 1) / d['nthread']) for t in range(d['nthread']) ]
    with closing(mp.Pool(1, initializer=initreadonly, initargs=(data_read_mem,))) as (tsubpool):
        tsubpool.map(tsubpart, blr)


def dataflag(d, data_read):
    """ Flagging data in single process 
    """
    for flag in d['flaglist']:
        mode, sig, conv = flag
        for ss in d['spw']:
            chans = n.arange(d['spw_chanr_select'][ss][0], d['spw_chanr_select'][ss][1])
            for pol in range(d['npol']):
                status = rtlib.dataflag(data_read, chans, pol, d, sig, mode, conv)
                logger.info(status)

    if 'badspwpol' in d:
        logger.info('Comparing overall power between spw/pol. Removing those with %d times typical value' % d['badspwpol'])
        spwpol = {}
        for spw in d['spw']:
            chans = n.arange(d['spw_chanr_select'][spw][0], d['spw_chanr_select'][spw][1])
            for pol in range(d['npol']):
                spwpol[(spw, pol)] = n.abs(data_read[:, :, chans, pol]).std()

        meanstd = n.mean(spwpol.values())
        for spw, pol in spwpol:
            if spwpol[(spw, pol)] > d['badspwpol'] * meanstd:
                logger.info('Flagging all of (spw %d, pol %d) for excess noise.' % (spw, pol))
                chans = n.arange(d['spw_chanr_select'][spw][0], d['spw_chanr_select'][spw][1])
                data_read[:, :, chans, pol] = complex(0.0, 0.0)


def dataflagatom(chans, pol, d, sig, mode, conv):
    """ Wrapper function to get shared memory as numpy array into pool
    Assumes data_mem is global mps.Array
    """
    data = numpyview(data_mem, 'complex64', datashape(d))
    return rtlib.dataflag(data, chans, pol, d, sig, mode, conv)


def search(d, data_mem, u_mem, v_mem, w_mem):
    """ Search function.
    Queues all trials with multiprocessing.
    Assumes shared memory system with single uvw grid for all images.
    """
    data = numpyview(data_mem, 'complex64', datashape(d))
    u = numpyview(u_mem, 'float32', d['nbl'])
    v = numpyview(v_mem, 'float32', d['nbl'])
    w = numpyview(w_mem, 'float32', d['nbl'])
    data_resamp_mem = mps.Array(mps.ctypes.c_float, datasize(d) * 2)
    data_resamp = numpyview(data_resamp_mem, 'complex64', datashape(d))
    logger.debug('Search of segment %d' % d['segment'])
    beamnum = 0
    cands = {}
    candsfile = getcandsfile(d)
    if d['savecands'] and os.path.exists(candsfile):
        logger.warn('candsfile %s already exists' % candsfile)
        return cands
    if d['searchtype'] == 'image2w':
        wres = 100
        npix = max(d['npixx_full'], d['npixy_full'])
        bls, uvkers = rtlib.genuvkernels(w, wres, npix, d['uvres'], thresh=0.05)
    if n.any(data):
        logger.debug('Searching in %d chunks with %d threads' % (d['nchunk'], d['nthread']))
        logger.info('Dedispering to max (DM, dt) of (%d, %d) ...' % (d['dmarr'][(-1)], d['dtarr'][(-1)]))
        with closing(mp.Pool(d['nthread'], initializer=initresamp, initargs=(data_mem, data_resamp_mem))) as (resamppool):
            blranges = [ (d['nbl'] * t / d['nthread'], d['nbl'] * (t + 1) / d['nthread']) for t in range(d['nthread']) ]
            for dmind in xrange(len(d['dmarr'])):
                dm = d['dmarr'][dmind]
                logger.debug('Dedispersing for %d' % dm)
                dedisppart = partial(correct_dm, d, dm)
                dedispresults = resamppool.map(dedisppart, blranges)
                dtlast = 1
                for dtind in xrange(len(d['dtarr'])):
                    dt = d['dtarr'][dtind]
                    if dt > 1:
                        logger.debug('Resampling for %d' % dt)
                        resample = dt / dtlast
                        resamppart = partial(correct_dt, d, resample)
                        resampresults = resamppool.map(resamppart, blranges)
                        dtlast = dt
                    nskip_dm = (d['datadelay'][(-1)] - d['datadelay'][dmind]) / dt * (d['segment'] != 0)
                    searchints = (d['readints'] - d['datadelay'][dmind]) / dt - nskip_dm
                    logger.debug('Imaging %d ints from %d for (%d,%d)' % (searchints, nskip_dm, dm, dt))
                    image1part = partial(image1, d, u, v, w, dmind, dtind, beamnum)
                    nchunkdt = min(searchints, max(d['nthread'], d['nchunk'] / dt))
                    irange = [ (nskip_dm + searchints * chunk / nchunkdt, nskip_dm + searchints * (chunk + 1) / nchunkdt) for chunk in range(nchunkdt) ]
                    imageresults = resamppool.map(image1part, irange)
                    for imageresult in imageresults:
                        for kk in imageresult.keys():
                            cands[kk] = imageresult[kk]

        if 'sigma_plot' in d:
            from rtpipe.reproduce import make_cand_plot as makecp
            if 'snr2' in d['features']:
                snrcol = d['features'].index('snr2')
            elif 'snr1' in d['features']:
                snrcol = d['features'].index('snr1')
            snrs = n.array([ value[snrcol] for value in cands.itervalues() ])
            maxsnr = max([0] + [ value[snrcol] for value in cands.itervalues() ])
            if maxsnr > d['sigma_plot']:
                segment, candint, dmind, dtind, beamnum = [ key for key, value in cands.iteritems() if value[snrcol] == maxsnr ][0]
                logger.info('Making cand plot for scan %d, segment %d, candint %d, dmind %d, dtint %d with SNR %.1f.' % (d['scan'], segment, candint, dmind, dtind, maxsnr))
                im, data = runreproduce(d, data_mem, data_resamp_mem, u, v, w, dmind, dtind, candint)
                loclabel = [d['scan'], segment, candint, dmind, dtind, beamnum]
                makecp(d, im, data, loclabel, version=2, snrs=snrs)
            else:
                logger.info('No candidate in segment %d above sigma_plot %.1f' % (d['segment'], d['sigma_plot']))
    else:
        logger.warn('Data for processing is zeros. Moving on...')
    logger.info('Found %d cands in scan %d segment %d of %s. ' % (len(cands), d['scan'], d['segment'], d['filename']))
    return cands


def runreproduce(d, data_mem, data_resamp_mem, u, v, w, dmind, dtind, candint=-1, lm=None, twindow=30):
    """ Reproduce function, much like search.

    Returns image and rephased data for given candint.
    If no candint is given, it returns resampled data by default. Optionally rephases to lm=(l, m) coordinates.
    """
    data_resamp = numpyview(data_resamp_mem, 'complex64', datashape(d))
    with closing(mp.Pool(1, initializer=initresamp, initargs=(data_mem, data_resamp_mem))) as (repropool):
        logger.info('Dedispersing with DM=%.1f, dt=%d...' % (d['dmarr'][dmind], d['dtarr'][dtind]))
        repropool.apply(correct_dmdt, [d, dmind, dtind, (0, d['nbl'])])
        if 'image1' in d['searchtype']:
            npixx = d['npixx']
            npixy = d['npixy']
        else:
            if 'image2' in d['searchtype']:
                npixx = d['npixx_full']
                npixy = d['npixy_full']
            if candint > -1:
                if lm:
                    logger.warn('Using candint image to get l,m. Not using provided l,m.')
                logger.info('Imaging int %d with %d %d pixels...' % (candint, npixx, npixy))
                im = repropool.apply(image1wrap, [d, u, v, w, npixx, npixy, candint / d['dtarr'][dtind]])
                snrmin = im.min() / im.std()
                snrmax = im.max() / im.std()
                logger.info('Made image with SNR min, max: %.1f, %.1f' % (snrmin, snrmax))
                if snrmax > -1 * snrmin:
                    l1, m1 = calc_lm(d, im, minmax='max')
                else:
                    l1, m1 = calc_lm(d, im, minmax='min')
                repropool.apply(move_phasecenter, [d, l1, m1, u, v])
                minint = max(candint / d['dtarr'][dtind] - twindow / 2, 0)
                maxint = min(candint / d['dtarr'][dtind] + twindow / 2, len(data_resamp) / d['dtarr'][dtind])
                return (
                 im, data_resamp[minint:maxint].mean(axis=1))
        if lm:
            l1, m1 = lm
            repropool.apply(move_phasecenter, [d, l1, m1, u, v])
        return data_resamp


def add_transient(d, data, u, v, w, l1, m1, i, s, dm=0, dt=1):
    """ Add a transient to data.
    l1, m1 are relative direction cosines (location) of transient
    added at integration i (at highest freq) with brightness s (per int/chan/bl/pol in data units)
    dm/dt are dispersion (in pc/cm3) and pulse width (in s).
    """
    ang = lambda ch: l1 * u * d['freq'][ch] / d['freq_orig'][0] + m1 * v * d['freq'][ch] / d['freq_orig'][0]
    delay = lambda ch: n.round(0.0041488 * dm * (d['freq'][ch] ** (-2) - d['freq'][(-1)] ** (-2)) / d['inttime'], 0).astype(int)
    for ch in range(d['nchan']):
        data[i + delay(ch):i + delay(ch) + dt, :, ch] += s * n.exp(complex(0.0, 2.0) * n.pi * ang(ch)[None, :, None])

    return


def make_transient(std, DMmax, Amin=6.0, Amax=20.0, rmax=20.0, rmin=0.0, DMmin=0.0):
    """ Produce a mock transient pulse source for the purposes of characterizing the
    detection success of the current pipeline.
    
    Assumes
    - Code to inject the transients does so by inserting at an array index 
    - Noise level at the center of the data array is characteristic of the
      noise level throughout

    Input
    std   - noise level in visibilities(?) at mid-point of segment
    DMmax - maximum DM at which mock transient can be inserted [pc/cm^3]
    Amin/Amax is amplitude in units of the std (calculated below)
    rmax/rmin is radius range in arcmin
    DMmin is min DM

    Returns
    loff - direction cosine offset of mock transient from phase center [radians]
    moff - direction cosine offset of mock transient from phase center [radians]
    A  - amplitude of transient [std units]
    DM - dispersion measure of mock transient [pc/cm^3]
    """
    rad_arcmin = math.pi / 10800
    phimin = 0.0
    phimax = 2 * math.pi
    A = random.uniform(Amin, Amax) * std
    r = random.uniform(rmin, rmax)
    phi = random.uniform(phimin, phimax)
    loff = r * math.cos(phi) * rad_arcmin
    moff = r * math.sin(phi) * rad_arcmin
    DM = random.uniform(DMmin, DMmax)
    return (loff, moff, A, DM)


def pipeline_refine(d0, candloc, scaledm=2.1, scalepix=2, scaleuv=1.0, chans=[], returndata=False):
    """ 
    Reproduces candidate and potentially improves sensitivity through better DM and imaging parameters.
    scale* parameters enhance sensitivity by making refining dmgrid and images.
    Other options include: 
      d0['selectpol'] = ['RR']
      d0['flaglist'] = [('blstd', 2.5, 0.05)]
    """
    import rtpipe.parseparams as pp
    if not len(candloc) == 6:
        raise AssertionError('candloc should be (scan, segment, candint, dmind, dtind, beamnum).')
        scan, segment, candint, dmind, dtind, beamnum = candloc
        d1 = d0.copy()
        segmenttimes = d1['segmenttimesdict'][scan]
        workdir = os.path.exists(d1['filename']) or os.getcwd()
        filename = os.path.join(workdir, os.path.basename(d1['filename']))
    else:
        filename = d1['filename']
    params = pp.Params()
    for key in d1.keys():
        if not hasattr(params, key):
            _ = d1.pop(key)

    d1['npix'] = 0
    d1['uvres'] = 0
    d1['savecands'] = False
    d1['savenoise'] = False
    d1['logfile'] = False
    d = set_pipeline(filename, scan, **d1)
    if chans:
        d['chans'] = chans
    d['segmenttimes'] = segmenttimes
    d['nsegments'] = len(segmenttimes)
    data_mem = mps.Array(mps.ctypes.c_float, datasize(d) * 2)
    u_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    v_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    w_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    data = numpyview(data_mem, 'complex64', datashape(d))
    u = numpyview(u_mem, 'float32', d['nbl'])
    v = numpyview(v_mem, 'float32', d['nbl'])
    w = numpyview(w_mem, 'float32', d['nbl'])
    data[:] = pipeline_reproduce(d, segment=segment, product='data')
    d['segment'] = segment
    u[:], v[:], w[:] = ps.get_uvw_segment(d, segment)
    dmcand = d['dmarr'][dmind]
    if scaledm > 1.0:
        try:
            dmdelta = d['dmarr'][(dmind + 1)] - d['dmarr'][dmind]
        except IndexError:
            try:
                dmdelta = d['dmarr'][dmind] - d['dmarr'][(dmind - 1)]
            except IndexError:
                dmdelta = 0.1 * dmcand

        d['dmarr'] = list(n.arange(dmcand - dmdelta, dmcand + dmdelta, dmdelta / scaledm))
    elif scaledm == 1.0:
        d['dmarr'] = [
         dmcand]
    d['datadelay'] = [ rtlib.calc_delay(d['freq'], d['inttime'], dm).max() for dm in d['dmarr'] ] + [d['datadelay'][(-1)]]
    d['dtarr'] = [d['dtarr'][dtind]]
    d['npixx'] = scalepix * d['npixx']
    d['npixy'] = scalepix * d['npixy']
    d['uvres'] = scaleuv * d['uvres']
    logger.info('Refining DM grid to %s and expanding images to (%d, %d) pix with uvres %d' % (str(d['dmarr']), d['npixx'], d['npixy'], d['uvres']))
    cands = search(d, data_mem, u_mem, v_mem, w_mem)
    cands = {tuple([scan] + list(loc)):list(prop) for loc, prop in cands.iteritems()}
    d['featureind'].insert(0, 'scan')
    if returndata:
        return data
    else:
        return (
         d, cands)


def pipeline_lightcurve(d, l1=0, m1=0, segments=[], scan=-1):
    """ Makes lightcurve at given (l1, m1)
    l1, m1 define phase center. if not set, then image max is used.
    """
    if scan == -1:
        scan = d['scan']
    if segments == []:
        segments = range(d['nsegments'])
    d = set_pipeline(d['filename'], scan, fileroot=d['fileroot'], dmarr=[0], dtarr=[1], savenoise=False, timesub='', logfile=False, nsegments=d['nsegments'])
    data_mem = mps.Array(mps.ctypes.c_float, datasize(d) * 2)
    data_read_mem = mps.Array(mps.ctypes.c_float, datasize(d) * 2)
    data_resamp_mem = mps.Array(mps.ctypes.c_float, datasize(d) * 2)
    u_read_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    u_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    v_read_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    v_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    w_read_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    w_mem = mps.Array(mps.ctypes.c_float, d['nbl'])
    data_read = numpyview(data_read_mem, 'complex64', datashape(d))
    u_read = numpyview(u_read_mem, 'float32', d['nbl'], raw=False)
    v_read = numpyview(v_read_mem, 'float32', d['nbl'], raw=False)
    w_read = numpyview(w_read_mem, 'float32', d['nbl'], raw=False)
    lightcurve = n.zeros(shape=(d['nints'], d['nchan'], d['npol']), dtype='complex64')
    phasecenters = []
    with closing(mp.Pool(1, initializer=initread, initargs=(data_read_mem, u_read_mem, v_read_mem, w_read_mem, data_mem, u_mem, v_mem, w_mem))) as (readpool):
        for segment in segments:
            logger.info('Reading data...')
            readpool.apply(pipeline_dataprep, (d, segment))
            if not any([l1, m1]):
                im = sample_image(d, data_read, u_read, v_read, w_read, i=-1, verbose=1, imager='xy')
                l2, m2 = calc_lm(d, im)
            else:
                l2 = l1
                m2 = m1
            logger.info('Rephasing data to (l, m)=(%.4f, %.4f).' % (l2, m2))
            rtlib.phaseshift_threaded(data_read, d, l2, m2, u_read, v_read)
            phasecenters.append((l2, m2))
            nskip = (86400 * (d['segmenttimes'][(segment, 0)] - d['starttime_mjd']) / d['inttime']).astype(int)
            lightcurve[nskip:(nskip + d['readints'])] = data_read.mean(axis=1)

    return (
     phasecenters, lightcurve)


def set_pipeline(filename, scan, fileroot='', paramfile='', **kwargs):
    """ Function defines pipeline state for search. Takes data/scan as input.
    fileroot is base name for associated products (cal files, noise, cands). if blank, it is set to filename.
    paramfile is name of file that defines all pipeline parameters (python-like syntax).
    kwargs used to overload paramfile definitions.
    Many parameters take 0 as default, which auto-defines ideal parameters. 
    This definition does not yet consider memory/cpu/time limitations.
    nsegments defines how to break jobs in time. nchunk defines how many jobs are sent to nthreads.
    """
    workdir = os.path.dirname(os.path.abspath(filename))
    filename = filename.rstrip('/')
    if not os.path.exists(filename):
        raise AssertionError
        if os.path.exists(os.path.join(filename, 'Main.xml')):
            d = ps.get_metadata(filename, scan, paramfile=paramfile, **kwargs)
            d['dataformat'] = 'sdm'
        else:
            d = pm.get_metadata(filename, scan, paramfile=paramfile, **kwargs)
            d['dataformat'] = 'ms'
        d['rtpipe_version'] = __version__
        if fileroot:
            d['fileroot'] = fileroot
        else:
            d['fileroot'] = os.path.basename(os.path.abspath(filename))
        if not d['gainfile'] or not os.path.exists(d['gainfile']):
            gainfilelist = glob.glob(os.path.join(d['workdir'], d['fileroot'] + '.g?'))
            bpfilelist = glob.glob(os.path.join(d['workdir'], d['fileroot'] + '.b?'))
            if not gainfilelist or not bpfilelist:
                gainfilelist = glob.glob(d['fileroot'] + '.g?')
                bpfilelist = glob.glob(d['fileroot'] + '.b?')
            if gainfilelist and bpfilelist:
                gainfilelist.sort()
                d['gainfile'] = gainfilelist[(-1)]
                logger.info('Autodetected CASA gainfile %s' % d['gainfile'])
                bpfilelist.sort()
                d['bpfile'] = bpfilelist[(-1)]
                logger.info('Autodetected CASA bpfile %s' % d['bpfile'])
            filelist = glob.glob(os.path.join(d['workdir'], filename + '.GN'))
            if not filelist:
                filelist = glob.glob(filename + '.GN')
            if filelist:
                d['gainfile'] = filelist[0]
                logger.info('Autodetected telcal file %s' % d['gainfile'])
            if not os.path.exists(d['gainfile']):
                logger.warn(('Calibration file autodetection failed for gainfile {0}').format(d['gainfile']))
        d['featureind'] = ['segment', 'int', 'dmind', 'dtind', 'beamnum']
        if 'features' not in d:
            if d['searchtype'] == 'image1':
                d['features'] = [
                 'snr1', 'immax1', 'l1', 'm1']
            elif d['searchtype'] == 'image1snip':
                d['features'] = [
                 'snr1', 'immax1', 'l1', 'm1', 'im40', 'spec20']
            elif d['searchtype'] == 'image1stats':
                d['features'] = [
                 'snr1', 'immax1', 'l1', 'm1', 'specstd', 'specskew', 'speckurtosis', 'imskew', 'imkurtosis']
            elif 'image2' in d['searchtype']:
                d['features'] = [
                 'snr1', 'immax1', 'l1', 'm1', 'snr2', 'immax2', 'l2', 'm2']
        if d['uvres'] == 0:
            d['uvres'] = d['uvres_full']
        else:
            urange = d['urange'][scan] * (d['freq'].max() / d['freq_orig'][0])
            vrange = d['vrange'][scan] * (d['freq'].max() / d['freq_orig'][0])
            powers = n.fromfunction(lambda i, j: 2 ** i * 3 ** j, (14, 10), dtype='int')
            rangex = n.round(d['uvoversample'] * urange).astype('int')
            rangey = n.round(d['uvoversample'] * vrange).astype('int')
            largerx = n.where(powers - rangex / d['uvres'] > 0, powers, powers[(-1,
                                                                                -1)])
            p2x, p3x = n.where(largerx == largerx.min())
            largery = n.where(powers - rangey / d['uvres'] > 0, powers, powers[(-1,
                                                                                -1)])
            p2y, p3y = n.where(largery == largery.min())
            d['npixx_full'] = (2 ** p2x * 3 ** p3x)[0]
            d['npixy_full'] = (2 ** p2y * 3 ** p3y)[0]
        d['npixx'] = d['npixx_full']
        d['npixy'] = d['npixy_full']
        if 'npix_max' in d:
            if d['npix_max']:
                d['npixx'] = min(d['npix_max'], d['npixx_full'])
                d['npixy'] = min(d['npix_max'], d['npixy_full'])
        if d['npix']:
            d['npixx'] = d['npix']
            d['npixy'] = d['npix']
        else:
            d['npix'] = max(d['npixx'], d['npixy'])
        if len(d['dmarr']) == 0 and d.has_key('dm_maxloss') and d.has_key('maxdm') and d.has_key('dm_pulsewidth'):
            d['dmarr'] = calc_dmgrid(d, maxloss=d['dm_maxloss'], maxdm=d['maxdm'], dt=d['dm_pulsewidth'])
            if d['maxdm'] > 0:
                logger.info('Calculated %d dms for max sensitivity loss %.2f, maxdm %d pc/cm3, and pulse width %d ms' % (len(d['dmarr']), d['dm_maxloss'], d['maxdm'], d['dm_pulsewidth'] / 1000))
        else:
            d['dmarr'] = [
             0]
            logger.info("Can't calculate dm grid without dm_maxloss, maxdm, and dm_pulsewidth defined. Setting to [0].")
    d['t_overlap'] = rtlib.calc_delay(d['freq'], d['inttime'], max(d['dmarr'])).max() * d['inttime']
    d['datadelay'] = [ rtlib.calc_delay(d['freq'], d['inttime'], dm).max() for dm in d['dmarr'] ]
    d['nints'] = d['nints'] - d['nskip']
    if d.has_key('selectpol'):
        d['pols'] = [ pol for pol in d['pols_orig'] if pol in d['selectpol'] ]
    else:
        d['pols'] = d['pols_orig']
    d['npol'] = len(d['pols'])
    if d['nchunk'] == 0:
        d['nchunk'] = d['nthread']
    fringetime = d['nsegments'] or calc_fringetime(d)
    d['nsegments'] = max(1, min(d['nints'], int(d['scale_nsegments'] * d['inttime'] * d['nints'] / (fringetime - d['t_overlap']))))
    calc_segment_times(d)
    if d.has_key('memory_limit'):
        vismem0, immem0 = calc_memory_footprint(d, limit=True)
        if not vismem0 + immem0 < d['memory_limit']:
            raise AssertionError(('memory_limit of {0} is smaller than best solution of {1}. Try forcing nsegments/nchunk larger than {2}/{3} or reducing maxdm/npix').format(d['memory_limit'], vismem0 + immem0, d['nsegments'], max(d['dtarr']) / min(d['dtarr'])))
            vismem, immem = calc_memory_footprint(d)
            if vismem + immem > d['memory_limit']:
                logger.info(('Over memory limit of {4} when reading {0} segments with {1} chunks ({2}/{3} GB for visibilities/imaging). Searching for solution down to {5}/{6} GB...').format(d['nsegments'], d['nchunk'], vismem, immem, d['memory_limit'], vismem0, immem0))
            while vismem + immem > d['memory_limit']:
                vismem, immem = calc_memory_footprint(d)
                logger.debug(('Using {0} segments with {1} chunks ({2}/{3} GB for visibilities/imaging). Searching for better solution...').format(d['nchunk'], vismem, immem, d['memory_limit']))
                d['scale_nsegments'] = d['scale_nsegments'] * (vismem + immem) / float(d['memory_limit'])
                d['nsegments'] = max(1, min(d['nints'], int(d['scale_nsegments'] * d['inttime'] * d['nints'] / (fringetime - d['t_overlap']))))
                calc_segment_times(d)
                vismem, immem = calc_memory_footprint(d)
                while vismem + immem > d['memory_limit']:
                    logger.debug('Doubling nchunk from %d to fit in %d GB memory limit.' % (d['nchunk'], d['memory_limit']))
                    d['nchunk'] = 2 * d['nchunk']
                    vismem, immem = calc_memory_footprint(d)
                    if d['nchunk'] >= max(d['dtarr']) / min(d['dtarr']) * d['nthread']:
                        d['nchunk'] = d['nthread']
                        break

                vismem, immem = calc_memory_footprint(d)

    calc_segment_times(d)
    vismem, immem = calc_memory_footprint(d)
    assert all(d['dtarr']) and d['dtarr'] == sorted(d['dtarr']), 'dtarr must be larger than 0 and in increasing order'
    nfalse = calc_nfalse(d)
    logger.info('')
    logger.info('Pipeline summary:')
    if '.GN' in d['gainfile']:
        logger.info('\t Products saved with %s. telcal calibration with %s' % (d['fileroot'], os.path.basename(d['gainfile'])))
    else:
        logger.info('\t Products saved with %s. CASA calibration files (%s, %s)' % (d['fileroot'], os.path.basename(d['gainfile']), os.path.basename(d['bpfile'])))
    logger.info('\t Using %d segment%s of %d ints (%.1f s) with overlap of %.1f s' % (d['nsegments'], 's'[not d['nsegments'] - 1:], d['readints'], d['t_segment'], d['t_overlap']))
    if d['t_overlap'] > d['t_segment'] / 3.0:
        logger.info('\t\t Lots of segments needed, since Max DM sweep (%.1f s) close to segment size (%.2f s)' % (d['t_overlap'], d['t_segment']))
    logger.info('\t Downsampling in time/freq by %d/%d and skipping %d ints from start of scan.' % (d['read_tdownsample'], d['read_fdownsample'], d['nskip']))
    logger.info('\t Excluding ants %s' % d['excludeants'])
    logger.info('\t Using pols %s' % d['pols'])
    logger.info('')
    logger.info('\t Search with %s and threshold %.1f.' % (d['searchtype'], d['sigma_image1']))
    logger.info('\t Using %d DMs from %.1f to %.1f and dts %s.' % (len(d['dmarr']), min(d['dmarr']), max(d['dmarr']), d['dtarr']))
    logger.info('\t Using uvgrid npix=(%d,%d) and res=%d.' % (d['npixx'], d['npixy'], d['uvres']))
    logger.info('\t Expect %d thermal false positives per segment.' % nfalse)
    logger.info('')
    logger.info('\t Visibility memory usage is %.1f GB/segment' % vismem)
    logger.info('\t Imaging in %d chunk%s using max of %.1f GB/segment' % (d['nchunk'], 's'[not d['nsegments'] - 1:], immem))
    logger.info('\t Grand total memory usage: %.1f GB/segment' % (vismem + immem))
    return d


def getcandsfile(d, segment=-1, domock=False):
    """ Return name of candsfile for a given dictionary. Must have d['segment'] defined.
    domock is option to save simulated cands.
    """
    if domock:
        prefix = 'candsmock_'
    else:
        prefix = 'cands_'
    if d.has_key('segment'):
        return os.path.join(d['workdir'], prefix + d['fileroot'] + '_sc' + str(d['scan']) + 'seg' + str(d['segment']) + '.pkl')
    else:
        if segment >= 0:
            return os.path.join(d['workdir'], prefix + d['fileroot'] + '_sc' + str(d['scan']) + 'seg' + str(segment) + '.pkl')
        return ''


def getnoisefile(d, segment=-1):
    """ Return name of noisefile for a given dictionary. Must have d['segment'] defined.
    """
    if d.has_key('segment'):
        return os.path.join(d['workdir'], 'noise_' + d['fileroot'] + '_sc' + str(d['scan']) + 'seg' + str(d['segment']) + '.pkl')
    else:
        if segment >= 0:
            return os.path.join(d['workdir'], 'noise_' + d['fileroot'] + '_sc' + str(d['scan']) + 'seg' + str(segment) + '.pkl')
        return ''


def calc_nfalse(d):
    """ Calculate the number of thermal-noise false positives per segment.
    """
    dtfactor = n.sum([ 1.0 / i for i in d['dtarr'] ])
    ntrials = d['readints'] * dtfactor * len(d['dmarr']) * d['npixx'] * d['npixy']
    qfrac = 1 - (erf(d['sigma_image1'] / n.sqrt(2)) + 1) / 2.0
    nfalse = int(qfrac * ntrials)
    return nfalse


def calc_segment_times(d):
    """ Helper function for set_pipeline to define segmenttimes list, given nsegments definition
    """
    stopdts = n.linspace(d['nskip'] + d['t_overlap'] / d['inttime'], d['nints'], d['nsegments'] + 1)[1:]
    startdts = n.concatenate(([d['nskip']], stopdts[:-1] - d['t_overlap'] / d['inttime']))
    segmenttimes = []
    for startdt, stopdt in zip(d['inttime'] * startdts, d['inttime'] * stopdts):
        starttime = qa.getvalue(qa.convert(qa.time(qa.quantity(d['starttime_mjd'] + startdt / 86400, 'd'), form=['ymd'], prec=9)[0], 's'))[0] / 86400
        stoptime = qa.getvalue(qa.convert(qa.time(qa.quantity(d['starttime_mjd'] + stopdt / 86400, 'd'), form=['ymd'], prec=9)[0], 's'))[0] / 86400
        segmenttimes.append((starttime, stoptime))

    d['segmenttimes'] = n.array(segmenttimes)
    totaltimeread = 86400 * (d['segmenttimes'][:, 1] - d['segmenttimes'][:, 0]).sum()
    d['readints'] = n.round(totaltimeread / (d['inttime'] * d['nsegments'])).astype(int)
    d['t_segment'] = totaltimeread / d['nsegments']


def calc_memory_footprint(d, headroom=4.0, visonly=False, limit=False):
    """ Given pipeline state dict, this function calculates the memory required
    to store visibilities and make images.
    headroom scales visibility memory size from single data object to all copies (and potential file read needs)
    limit=True returns a the minimum memory configuration
    Returns tuple of (vismem, immem) in units of GB.
    """
    toGB = 8 / 1073741824.0
    d0 = d.copy()
    if limit:
        d0['readints'] = d['t_overlap'] / d['inttime']
        d0['nchunk'] = max(d['dtarr']) / min(d['dtarr']) * d['nthread']
    vismem = headroom * datasize(d0) * toGB
    if visonly:
        return vismem
    else:
        immem = d0['nthread'] * (d0['readints'] / d0['nchunk'] * d0['npixx'] * d0['npixy']) * toGB
        return (vismem, immem)


def calc_fringetime(d):
    """ Estimate largest time span of a "segment".
    A segment is the maximal time span that can be have a single bg fringe subtracted and uv grid definition.
    Max fringe window estimated for 5% amp loss at first null averaged over all baselines. Assumes dec=+90, which is conservative.
    Returns time in seconds that defines good window.
    """
    maxbl = d['uvres'] * d['npix'] / 2
    fringetime = 0.5 * 86400 / (2 * n.pi * maxbl / 25.0)
    return fringetime


def correct_dmdt(d, dmind, dtind, blrange):
    """ Dedisperses and resamples data *in place*.
    Drops edges, since it assumes that data is read with overlapping chunks in time.
    """
    data = numpyview(data_mem, 'complex64', datashape(d))
    data_resamp = numpyview(data_resamp_mem, 'complex64', datashape(d))
    bl0, bl1 = blrange
    data_resamp[:, bl0:bl1] = data[:, bl0:bl1]
    rtlib.dedisperse_resample(data_resamp, d['freq'], d['inttime'], d['dmarr'][dmind], d['dtarr'][dtind], blrange, verbose=0)


def correct_dm(d, dm, blrange):
    """ Dedisperses data into data_resamp
    Drops edges, since it assumes that data is read with overlapping chunks in time.
    """
    data = numpyview(data_mem, 'complex64', datashape(d))
    data_resamp = numpyview(data_resamp_mem, 'complex64', datashape(d))
    bl0, bl1 = blrange
    data_resamp[:, bl0:bl1] = data[:, bl0:bl1]
    rtlib.dedisperse_par(data_resamp, d['freq'], d['inttime'], dm, blrange, verbose=0)


def correct_dt(d, dt, blrange):
    """ Resamples data_resamp
    Drops edges, since it assumes that data is read with overlapping chunks in time.
    """
    data = numpyview(data_mem, 'complex64', datashape(d))
    data_resamp = numpyview(data_resamp_mem, 'complex64', datashape(d))
    bl0, bl1 = blrange
    rtlib.resample_par(data_resamp, d['freq'], d['inttime'], dt, blrange, verbose=0)


def calc_lm(d, im=[], pix=(), minmax='max'):
    """ Helper function to calculate location of image pixel in (l,m) coords.
    Assumes peak pixel, but input can be provided in pixel units.
    minmax defines whether to look for image maximum or minimum.
    """
    if len(pix) == 0:
        if minmax == 'max':
            peakl, peakm = n.where(im == im.max())
        elif minmax == 'min':
            peakl, peakm = n.where(im == im.min())
        peakl = peakl[0]
        peakm = peakm[0]
    elif len(pix) == 2:
        peakl, peakm = pix
    if len(im):
        npixx, npixy = im.shape
    else:
        npixx = d['npixx']
        npixy = d['npixy']
    l1 = (npixx / 2.0 - peakl) / (npixx * d['uvres'])
    m1 = (npixy / 2.0 - peakm) / (npixy * d['uvres'])
    return (
     l1, m1)


def move_phasecenter(d, l1, m1, u, v):
    """ Handler function for phaseshift_threaded
    """
    logger.info('Rephasing data to (l, m)=(%.4f, %.4f).' % (l1, m1))
    data_resamp = numpyview(data_resamp_mem, 'complex64', datashape(d))
    rtlib.phaseshift_threaded(data_resamp, d, l1, m1, u, v)


def calc_dmgrid(d, maxloss=0.05, dt=3000.0, mindm=0.0, maxdm=0.0):
    """ Function to calculate the DM values for a given maximum sensitivity loss.
    maxloss is sensitivity loss tolerated by dm bin width. dt is assumed pulse width in microsec.
    """
    tsamp = d['inttime'] * 1000000.0
    k = 8.3
    freq = d['freq'].mean()
    bw = 1000.0 * (d['freq'][(-1)] - d['freq'][0])
    ch = 1000.0 * (d['freq'][1] - d['freq'][0])
    dt0 = lambda dm: n.sqrt(dt ** 2 + tsamp ** 2 + (k * dm * ch / freq ** 3) ** 2)
    dt1 = lambda dm, ddm: n.sqrt(dt ** 2 + tsamp ** 2 + (k * dm * ch / freq ** 3) ** 2 + (k * ddm * bw / freq ** 3.0) ** 2)
    loss = lambda dm, ddm: 1 - n.sqrt(dt0(dm) / dt1(dm, ddm))
    loss_cordes = lambda ddm, dfreq, dt, freq: 1 - n.sqrt(n.pi) / (0.01382 * ddm * dfreq / (dt * freq ** 3)) * erf(0.00691 * ddm * dfreq / (dt * freq ** 3))
    if maxdm == 0:
        return [0]
    dmgrid = n.arange(mindm, maxdm, 0.05)
    dmgrid_final = [dmgrid[0]]
    for i in range(len(dmgrid)):
        ddm = (dmgrid[i] - dmgrid_final[(-1)]) / 2.0
        ll = loss(dmgrid[i], ddm)
        if ll > maxloss:
            dmgrid_final.append(dmgrid[i])

    return dmgrid_final


def image1(d, u, v, w, dmind, dtind, beamnum, irange):
    """ Parallelizable function for imaging a chunk of data for a single dm.
    Assumes data is dedispersed and resampled, so this just images each integration.
    Simple one-stage imaging that returns dict of params.
    returns dictionary with keys of cand location and values as tuple of features
    """
    i0, i1 = irange
    data_resamp = numpyview(data_resamp_mem, 'complex64', datashape(d))
    ims, snr, candints = rtlib.imgallfullfilterxyflux(n.outer(u, d['freq'] / d['freq_orig'][0]), n.outer(v, d['freq'] / d['freq_orig'][0]), data_resamp[i0:i1], d['npixx'], d['npixy'], d['uvres'], d['sigma_image1'])
    feat = {}
    for i in xrange(len(candints)):
        if snr[i] > 0:
            l1, m1 = calc_lm(d, ims[i], minmax='max')
        else:
            l1, m1 = calc_lm(d, ims[i], minmax='min')
        logger.info('Got one!  Int=%d, DM=%d, dt=%d: SNR_im=%.1f @ (%.2e,%.2e).' % ((i0 + candints[i]) * d['dtarr'][dtind], d['dmarr'][dmind], d['dtarr'][dtind], snr[i], l1, m1))
        candid = (d['segment'], (i0 + candints[i]) * d['dtarr'][dtind], dmind, dtind, beamnum)
        ff = []
        for feature in d['features']:
            if feature == 'snr1':
                ff.append(snr[i])
            elif feature == 'immax1':
                if snr[i] > 0:
                    ff.append(ims[i].max())
                else:
                    ff.append(ims[i].min())
            elif feature == 'l1':
                ff.append(l1)
            elif feature == 'm1':
                ff.append(m1)
            elif feature == 'im40':
                peakx, peaky = n.where(ims[i] == ims[i].max())
                sizex, sizey = ims[i].shape
                xmin = max(0, peakx - 20)
                xmax = min(peakx + 20, sizex)
                ymin = max(0, peaky - 20)
                ymax = min(peaky + 20, sizey)
                ff.append(ims[i][xmin:xmax, ymin:ymax])
            elif feature == 'spec20':
                imin = max(0, (i0 + candints[i]) * d['dtarr'][dtind] - 10)
                imax = min((i0 + candints[i]) * d['dtarr'][dtind] + 10, len(data_resamp))
                data_cut = data_resamp[imin:imax].copy()
                rtlib.phaseshift_threaded(data_cut, d, l1, m1, u, v)
                ff.append(data_cut.mean(axis=1))
            elif feature in ('specstd', 'specskew', 'speckurtosis'):
                if feature == 'specstd':
                    seli = (i0 + candints[i]) * d['dtarr'][dtind]
                    datasel = data_resamp[seli:seli + 1].copy()
                    rtlib.phaseshift_threaded(datasel, d, l1, m1, u, v)
                    data = n.ma.masked_equal(datasel, complex(0.0, 0.0))
                    spec = data.mean(axis=3).mean(axis=1).mean(axis=0).real
                    std = spec.std(axis=0)
                    ff.append(std)
                elif feature == 'specskew':
                    skew = float(mstats.skew(spec))
                    ff.append(skew)
                elif feature == 'speckurtosis':
                    kurtosis = float(mstats.kurtosis(spec))
                    ff.append(kurtosis)
            elif feature == 'imskew':
                skew = float(mstats.skew(ims[i].flatten()))
                ff.append(skew)
            elif feature == 'imkurtosis':
                kurtosis = float(mstats.kurtosis(ims[i].flatten()))
                ff.append(kurtosis)

        feat[candid] = list(ff)

    return feat


def image2(d, i0, i1, u, v, w, dmind, dtind, beamnum):
    """ Parallelizable function for imaging a chunk of data for a single dm.
    Assumes data is dedispersed and resampled, so this just images each integration.
    Two-stage imaging uses ideal uv coverage in second image.
    returns dictionary with keys of cand location and values as tuple of features
    """
    data_resamp = numpyview(data_resamp_mem, 'complex64', datashape(d))
    ims, snr, candints = rtlib.imgallfullfilterxy(n.outer(u, d['freq'] / d['freq_orig'][0]), n.outer(v, d['freq'] / d['freq_orig'][0]), data_resamp[i0:i1], d['npixx'], d['npixy'], d['uvres'], d['sigma_image1'])
    feat = {}
    for i in xrange(len(candints)):
        im2 = rtlib.imgonefullxy(n.outer(u, d['freq'] / d['freq_orig'][0]), n.outer(v, d['freq'] / d['freq_orig'][0]), data_resamp[(i0 + candints[i])], d['npixx_full'], d['npixy_full'], d['uvres'], verbose=0)
        snrmax = im2.max() / im2.std()
        snrmin = im2.min() / im2.std()
        if snrmax >= abs(snrmin):
            snr2 = snrmax
        else:
            snr2 = snrmin
        if abs(snr2) > d['sigma_image2']:
            if snr[i] > 0:
                l1, m1 = calc_lm(d, ims[i], minmax='max')
            else:
                l1, m1 = calc_lm(d, ims[i], minmax='min')
            if snr2 > 0:
                l2, m2 = calc_lm(d, im2, minmax='max')
            else:
                l2, m2 = calc_lm(d, im2, minmax='min')
            logger.info('Got one!  Int=%d, DM=%d, dt=%d: SNR_im1=%.1f, SNR_im2=%.1f @ (%.2e,%.2e).' % ((i0 + candints[i]) * d['dtarr'][dtind], d['dmarr'][dmind], d['dtarr'][dtind], snr[i], snr2, l2, m2))
            candid = (d['segment'], (i0 + candints[i]) * d['dtarr'][dtind], dmind, dtind, beamnum)
            ff = []
            for feature in d['features']:
                if feature == 'snr1':
                    ff.append(snr[i])
                elif feature == 'immax1':
                    if snr[i] > 0:
                        ff.append(ims[i].max())
                    else:
                        ff.append(ims[i].min())
                elif feature == 'l1':
                    ff.append(l1)
                elif feature == 'm1':
                    ff.append(m1)
                elif feature == 'snr2':
                    ff.append(snr2)
                elif feature == 'immax2':
                    if snr2 > 0:
                        ff.append(im2.max())
                    else:
                        ff.append(im2.min())
                elif feature == 'l2':
                    ff.append(l2)
                elif feature == 'm2':
                    ff.append(m2)

            feat[candid] = list(ff)
        else:
            logger.info('Almost...  Int=%d, DM=%d, dt=%d: SNR_im1=%.1f, SNR_im2=%.1f.' % ((i0 + candints[i]) * d['dtarr'][dtind], d['dmarr'][dmind], d['dtarr'][dtind], snr[i], snr2))

    return feat


def image2w(d, i0, i1, u, v, w, dmind, dtind, beamnum, bls, uvkers):
    """ Parallelizable function for imaging a chunk of data for a single dm.
    Assumes data is dedispersed and resampled, so this just images each integration.
    Two-stage imaging uses ideal uv coverage in second image.
    returns dictionary with keys of cand location and values as tuple of features
    """
    data_resamp = numpyview(data_resamp_mem, 'complex64', datashape(d))
    ims, snr, candints = rtlib.imgallfullfilterxy(n.outer(u, d['freq'] / d['freq_orig'][0]), n.outer(v, d['freq'] / d['freq_orig'][0]), data_resamp[i0:i1], d['npixx'], d['npixy'], d['uvres'], d['sigma_image1'])
    feat = {}
    for i in xrange(len(candints)):
        npix = max(d['npixx_full'], d['npixy_full'])
        im2 = rtlib.imgonefullw(n.outer(u, d['freq'] / d['freq_orig'][0]), n.outer(v, d['freq'] / d['freq_orig'][0]), data_resamp[(i0 + candints[i])], npix, d['uvres'], bls, uvkers, verbose=1)
        snrmax = im2.max() / im2.std()
        snrmin = im2.min() / im2.std()
        if snrmax >= abs(snrmin):
            snr2 = snrmax
        else:
            snr2 = snrmin
        if abs(snr2) > d['sigma_image2']:
            if snr[i] > 0:
                l1, m1 = calc_lm(d, ims[i], minmax='max')
            else:
                l1, m1 = calc_lm(d, ims[i], minmax='min')
            if snr2 > 0:
                l2, m2 = calc_lm(d, im2, minmax='max')
            else:
                l2, m2 = calc_lm(d, im2, minmax='min')
            logger.info('Got one!  Int=%d, DM=%d, dt=%d: SNR_im1=%.1f, SNR_im2=%.1f @ (%.2e,%.2e).' % ((i0 + candints[i]) * d['dtarr'][dtind], d['dmarr'][dmind], d['dtarr'][dtind], snr[i], snr2, l2, m2))
            candid = (d['segment'], (i0 + candints[i]) * d['dtarr'][dtind], dmind, dtind, beamnum)
            ff = []
            for feature in d['features']:
                if feature == 'snr1':
                    ff.append(snr[i])
                elif feature == 'immax1':
                    if snr[i] > 0:
                        ff.append(ims[i].max())
                    else:
                        ff.append(ims[i].min())
                elif feature == 'l1':
                    ff.append(l1)
                elif feature == 'm1':
                    ff.append(m1)
                elif feature == 'snr2':
                    ff.append(snr2)
                elif feature == 'immax2':
                    if snr2 > 0:
                        ff.append(im2.max())
                    else:
                        ff.append(im2.min())
                elif feature == 'l2':
                    ff.append(l2)
                elif feature == 'm2':
                    ff.append(m2)

            feat[candid] = list(ff)
        else:
            logger.info('Almost...  Int=%d, DM=%d, dt=%d: SNR_im1=%.1f, SNR_im2=%.1f.' % ((i0 + candints[i]) * d['dtarr'][dtind], d['dmarr'][dmind], d['dtarr'][dtind], snr[i], snr2))

    return feat


def image1wrap(d, u, v, w, npixx, npixy, candint):
    """ Parallelizable function for imaging a chunk of data for a single dm.
    Assumes data is dedispersed and resampled, so this just images each integration.
    Simple one-stage imaging that returns dict of params.
    returns dictionary with keys of cand location and values as tuple of features
    """
    data_resamp = numpyview(data_resamp_mem, 'complex64', datashape(d))
    image = rtlib.imgonefullxy(n.outer(u, d['freq'] / d['freq_orig'][0]), n.outer(v, d['freq'] / d['freq_orig'][0]), data_resamp[candint], npixx, npixy, d['uvres'], verbose=1)
    return image


def imagearm(sdmfile, scan, segment, npix=512, res=50, **kwargs):
    """ Function to do end-to-end 1d, arm-based imaging """
    import sdmpy
    sdm = sdmpy.SDM(sdmfile)
    ants = {ant.stationId:ant.name for ant in sdm['Antenna']}
    stations = {st.stationId:st.name for st in sdm['Station'] if 'X' not in str(st.name) if 'X' not in str(st.name)}
    west = [ int(str(ants[st]).lstrip('ea')) for st in stations if 'W' in str(stations[st]) ]
    east = [ int(str(ants[st]).lstrip('ea')) for st in stations if 'E' in str(stations[st]) ]
    north = [ int(str(ants[st]).lstrip('ea')) for st in stations if 'N' in str(stations[st]) ]
    d = set_pipeline(sdmfile, scan, **kwargs)
    blarr = rtlib.calc_blarr(d)
    selwest = [ i for i in range(len(blarr)) if all([ b in west for b in blarr[i] ]) ]
    seleast = [ i for i in range(len(blarr)) if all([ b in east for b in blarr[i] ]) ]
    selnorth = [ i for i in range(len(blarr)) if all([ b in north for b in blarr[i] ]) ]
    u, v, w = ps.get_uvw_segment(d, segment=segment)
    data = pipeline_reproduce(d, segment=segment, product='data')
    dataw = data[:, selwest].mean(axis=3).mean(axis=2)
    datae = data[:, seleast].mean(axis=3).mean(axis=2)
    datan = data[:, selnorth].mean(axis=3).mean(axis=2)
    uw = u[selwest]
    ue = u[seleast]
    un = u[selnorth]
    vw = v[selwest]
    ve = v[seleast]
    vn = v[selnorth]
    grid = n.zeros((len(data), npix), dtype='complex64')
    grid2 = n.zeros((len(data), npix), dtype='float32')
    datalist = []
    for uu, vv, dd in [(uw, vw, dataw), (ue, ve, datae), (un, vn, datan)]:
        uu = n.mod(uu / res, npix)
        vv = n.mod(vv / res, npix)
        uv = n.sqrt(uu ** 2 + vv ** 2)
        uv = n.round(uv).astype(int)
        for i in range(len(uv)):
            if uv[i] < 512:
                grid[:, uv[i]] = dd[:, i]

        grid2 = n.fft.ifft(grid, axis=1).real
        datalist.append(grid2)

    return datalist


def sample_image(d, data, u, v, w, i=-1, verbose=0, imager='xy', wres=100):
    """ Samples one integration and returns image
    i is integration to image. Default is mid int.
    """
    if i == -1:
        i = len(data) / 2
    if imager == 'xy':
        image = rtlib.imgonefullxy(n.outer(u, d['freq'] / d['freq_orig'][0]), n.outer(v, d['freq'] / d['freq_orig'][0]), data[i], d['npixx'], d['npixy'], d['uvres'], verbose=verbose)
    elif imager == 'w':
        npix = max(d['npixx'], d['npixy'])
        bls, uvkers = rtlib.genuvkernels(w, wres, npix, d['uvres'], ksize=21, oversample=1)
        image = rtlib.imgonefullw(n.outer(u, d['freq'] / d['freq_orig'][0]), n.outer(v, d['freq'] / d['freq_orig'][0]), data[i], npix, d['uvres'], bls, uvkers, verbose=verbose)
    return image


def estimate_noiseperbl(data):
    """ Takes large data array and sigma clips it to find noise per bl for input to detect_bispectra.
    Takes mean across pols and channels for now, as in detect_bispectra.
    """
    datamean = data.mean(axis=2).imag
    datameanmin, datameanmax = rtlib.sigma_clip(datamean.flatten())
    good = n.where((datamean > datameanmin) & (datamean < datameanmax))
    noiseperbl = datamean[good].std()
    logger.debug('Clipped to %d%% of data (%.3f to %.3f). Noise = %.3f.' % (100.0 * len(good[0]) / len(datamean.flatten()), datameanmin, datameanmax, noiseperbl))
    return noiseperbl


def noisepickle(d, data, u, v, w, chunk=200):
    """ Calculates noise properties and saves values to pickle.
    chunk defines window for measurement. at least one measurement always made.
    """
    if d['savenoise']:
        noisefile = getnoisefile(d)
        if os.path.exists(noisefile):
            logger.warn('noisefile %s already exists' % noisefile)
        else:
            nints = len(data)
            chunk = min(chunk, nints)
            results = []
            rr = range(0, nints, chunk)
            if len(rr) == 1:
                rr.append(1)
            for i in range(len(rr) - 1):
                imid = (rr[i] + rr[(i + 1)]) / 2
                noiseperbl = estimate_noiseperbl(data[rr[i]:rr[(i + 1)]])
                imstd = sample_image(d, data, u, v, w, imid, verbose=0).std()
                zerofrac = float(len(n.where(data[rr[i]:rr[(i + 1)]] == complex(0.0, 0.0))[0])) / data[rr[i]:rr[(i + 1)]].size
                results.append((d['segment'], noiseperbl, zerofrac, imstd))

            with open(noisefile, 'a') as (pkl):
                pickle.dump(results, pkl)
            logger.info('Wrote %d noise measurement%s to %s.' % (len(results), 's'[:len(results) - 1], noisefile))


def savecands(d, cands, domock=False):
    """ Save all candidates in pkl file for later aggregation and filtering.
    domock is option to save simulated cands file
    """
    with open(getcandsfile(d, domock=domock), 'w') as (pkl):
        pickle.dump(d, pkl)
        pickle.dump(cands, pkl)


def datashape(d):
    return (
     d['readints'] / d['read_tdownsample'], d['nbl'], d['nchan'] / d['read_fdownsample'], d['npol'])


def datasize(d):
    return long(d['readints'] * d['nbl'] * d['nchan'] * d['npol'] / (d['read_tdownsample'] * d['read_fdownsample']))


def numpyview(arr, datatype, shape, raw=False):
    """ Takes mp shared array and returns numpy array with given shape.
    """
    if raw:
        return n.frombuffer(arr, dtype=n.dtype(datatype)).view(n.dtype(datatype)).reshape(shape)
    else:
        return n.frombuffer(arr.get_obj(), dtype=n.dtype(datatype)).view(n.dtype(datatype)).reshape(shape)


def initreadonly(shared_arr_):
    global data_read_mem
    data_read_mem = shared_arr_


def initresamp(shared_arr_, shared_arr2_):
    global data_mem
    global data_resamp_mem
    data_mem = shared_arr_
    data_resamp_mem = shared_arr2_


def initread(shared_arr1_, shared_arr2_, shared_arr3_, shared_arr4_, shared_arr5_, shared_arr6_, shared_arr7_, shared_arr8_):
    global data_mem
    global data_read_mem
    global u_mem
    global u_read_mem
    global v_mem
    global v_read_mem
    global w_mem
    global w_read_mem
    data_read_mem = shared_arr1_
    u_read_mem = shared_arr2_
    v_read_mem = shared_arr3_
    w_read_mem = shared_arr4_
    data_mem = shared_arr5_
    u_mem = shared_arr6_
    v_mem = shared_arr7_
    w_mem = shared_arr8_