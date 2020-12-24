# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbe-master/realfast/anaconda/envs/deployment/lib/python2.7/site-packages/rtpipe/parsems.py
# Compiled at: 2016-10-24 18:03:37
try:
    import casautil
except ImportError:
    import pwkit.environments.casa.util as casautil

import os, time, string, logging, numpy as n, rtpipe.parseparams as pp, cPickle as pickle
logger = logging.getLogger(__name__)
ms = casautil.tools.ms()
tb = casautil.tools.table()
qa = casautil.tools.quanta()

def get_metadata(filename, scan, paramfile='', **kwargs):
    """ Function to scan data (a small read) and define parameters used elsewhere.
    filename needs full path.
    Examples include, read/bgsub windows, image grid, memory profile.
    If pickle file doesn't exist, it creates one. 
    Either way, dictionary is returned with info.
    """
    d = {}
    d['filename'] = os.path.abspath(filename.rstrip('/'))
    d['workdir'] = os.path.dirname(d['filename'])
    params = pp.Params(paramfile)
    for k in params.defined:
        d[k] = params[k]

    for key in kwargs.keys():
        logger.info('Setting %s to %s' % (key, kwargs[key]))
        d[key] = kwargs[key]

    assert d['read_fdownsample'] == 1, 'read_fdownsample not yet implemented for MS files.'
    pklname = d['filename'].rstrip('.ms') + '_init2.pkl'
    if os.path.exists(pklname):
        logger.debug('Initializing pickle found at %s.' % pklname)
        pkl = open(pklname, 'r')
        try:
            stuff = pickle.load(pkl)
        except EOFError:
            logger.warn('Bad pickle file. Exiting...')
            return 1

        for key in stuff.keys():
            d[key] = stuff[key]

    else:
        logger.debug('No initialization pickle found. Making anew...')
        tb.open(d['filename'] + '/POLARIZATION')
        d['pols_orig'] = tb.getcol('CORR_TYPE').flatten()
        d['npol_orig'] = len(d['pols_orig'])
        tb.close()
        tb.open(d['filename'] + '/ANTENNA')
        d['dishdiameter'] = tb.getcol('DISH_DIAMETER')[0]
        tb.close()
        logger.debug('Opening %s...' % d['filename'])
        ms.open(d['filename'])
        md = ms.metadata()
        if 'VLA' in md.observatorynames()[0]:
            d['ants'] = [ int(md.antennanames(aa)[0][2:]) for aa in range(d['nants']) ]
        else:
            if 'GMRT' in md.observatorynames()[0]:
                d['ants'] = md.antennaids()
            for ant in d['excludeants']:
                d['ants'].remove(ant)

            d['nants'] = len(d['ants'])
            d['scans'] = md.scannumbers()
            d['scansummary'] = ms.getscansummary()
            scanlist = sorted(d['scansummary'].keys())
            logger.debug('Reading a little data from each scan...')
            nints_snip = 10
            orig_spws_all = {}
            freq_orig_all = {}
            urange = {}
            vrange = {}
            for ss in scanlist:
                orig_spws0 = md.spwsforscan(int(ss))
                orig_spws_all[ss] = [ sorted(zip(orig_spws0, [ md.chanfreqs(spw0)[0] / 1000000000.0 for spw0 in orig_spws0 ]), key=lambda ss: ss[1])[i][0] for i in range(len(orig_spws0)) ]
                ff = n.array([])
                for spw0 in orig_spws0:
                    ff = n.concatenate((ff, md.chanfreqs(spw0) / 1000000000.0)).astype('float32')

                freq_orig_all[ss] = ff
                starttime_mjd0 = d['scansummary'][ss]['0']['BeginTime']
                inttime0 = d['scansummary'][ss]['0']['IntegrationTime']
                starttime = qa.getvalue(qa.convert(qa.time(qa.quantity(starttime_mjd0, 'd'), form=['ymd'], prec=9)[0], 's'))[0]
                stoptime = qa.getvalue(qa.convert(qa.time(qa.quantity(starttime_mjd0 + nints_snip * inttime0 / 86400.0, 'd'), form=['ymd'], prec=9)[0], 's'))[0]
                selection = {'time': [starttime, stoptime], 'uvdist': [1.0, 10000000000.0]}
                ms.selectinit(datadescid=0)
                ms.select(items=selection)
                ms.iterinit(['TIME'], nints_snip * inttime0)
                ms.iterorigin()
                da = ms.getdata(['axis_info', 'u', 'v', 'w'])
                urange[ss] = da['u'].max() - da['u'].min()
                vrange[ss] = da['v'].max() - da['v'].min()

        d['urange'] = urange
        d['vrange'] = vrange
        d['freq_orig_all'] = freq_orig_all
        d['orig_spws_all'] = orig_spws_all
        ms.close()
        pkl = open(pklname, 'wb')
        pickle.dump(d, pkl)
        pkl.close()
    if datacol:
        d['datacol'] = datacol
    else:
        if not datacol:
            d['datacol'] = 'data'
        pols = []
        for pol in d['pols_orig']:
            if len(selectpol):
                if casautil.pol_names[pol] in selectpol:
                    pols.append(casautil.pol_names[pol])
            else:
                pols.append(casautil.pol_names[pol])

        d['pols'] = pols
        d['npol'] = len(pols)
        d['scan'] = int(scanlist[scan])
        d['orig_spws'] = n.array(d['orig_spws_all'][scanlist[scan]])
        if len(d['spw']):
            d['spwlist'] = d['orig_spws'][spw]
        elif len(d['spw']):
            d['spwlist'] = d['orig_spws'][d['spw']]
        else:
            d['spwlist'] = d['orig_spws']
        d['spw'] = sorted(d['spwlist'])
        allfreq = d['freq_orig_all'][scanlist[scan]]
        chperspw = len(allfreq) / len(d['orig_spws'])
        spwch = []
        for ss in d['orig_spws']:
            if ss in d['spwlist']:
                spwch.extend(range(ss * chperspw, (ss + 1) * chperspw))

    d['freq_orig'] = allfreq[spwch]
    d['nspw'] = len(d['spwlist'])
    if len(d['chans']):
        d['freq'] = d['freq_orig'][chans]
        d['chans'] = chans
    elif len(d['chans']):
        d['freq'] = d['freq_orig'][d['chans']]
    else:
        d['freq'] = d['freq_orig']
        d['chans'] = range(len(d['freq']))
    d['nchan'] = len(d['freq'])
    d['nints'] = d['scansummary'][scanlist[scan]]['0']['nRow'] / (d['nbl'] * d['npol'])
    inttime0 = d['scansummary'][scanlist[scan]]['0']['IntegrationTime']
    d['uvres_full'] = n.round(d['dishdiameter'] / (0.3 / d['freq'].min()) / 2).astype('int')
    urange = d['urange'][scanlist[scan]] * d['freq'].max() * (1000000000.0 / 300000000.0)
    vrange = d['vrange'][scanlist[scan]] * d['freq'].max() * (1000000000.0 / 300000000.0)
    powers = n.fromfunction(lambda i, j: 2 ** i * 3 ** j, (14, 10), dtype='int')
    rangex = n.round(d['uvoversample'] * urange).astype('int')
    rangey = n.round(d['uvoversample'] * vrange).astype('int')
    largerx = n.where(powers - rangex / d['uvres_full'] > 0, powers, powers[(-1, -1)])
    p2x, p3x = n.where(largerx == largerx.min())
    largery = n.where(powers - rangey / d['uvres_full'] > 0, powers, powers[(-1, -1)])
    p2y, p3y = n.where(largery == largery.min())
    d['npixx_full'] = (2 ** p2x * 3 ** p3x)[0]
    d['npixy_full'] = (2 ** p2y * 3 ** p3y)[0]
    d['starttime_mjd'] = d['scansummary'][scanlist[scan]]['0']['BeginTime']
    d['inttime'] = d['scansummary'][scanlist[scan]]['0']['IntegrationTime']
    logger.info('')
    logger.info('Metadata summary:')
    logger.info('\t Using scan %d (index %d)' % (d['scan'], scan))
    logger.info('\t nants, nbl: %d, %d' % (d['nants'], d['nbl']))
    logger.info('\t mid-freq, nspw, nchan: %.3f, %d, %d' % (d['freq'].mean(), d['nspw'], d['nchan']))
    logger.info('\t inttime: %.3f s' % d['inttime'])
    logger.info('\t %d polarizations: %s' % (d['npol'], d['pols']))
    logger.info('\t Ideal uvgrid npix=(%d,%d) and res=%d' % (d['npixx_full'], d['npixy_full'], d['uvres_full']))
    return d


def readiterinit(d):
    """ Prepare to read data with ms.iter*
    """
    starttime_mjd = d['starttime_mjd']
    timeskip = d['inttime'] * d['nskip']
    starttime = qa.getvalue(qa.convert(qa.time(qa.quantity(starttime_mjd + timeskip / 86400.0, 'd'), form=['ymd'], prec=9)[0], 's'))[0]
    stoptime = qa.getvalue(qa.convert(qa.time(qa.quantity(starttime_mjd + (timeskip + (d['nints'] + 1) * d['inttime']) / 86400.0, 'd'), form=['ymd'], prec=9)[0], 's'))[0]
    logger.debug('Time of first integration:', qa.time(qa.quantity(starttime_mjd, 'd'), form=['ymd'], prec=9)[0])
    logger.info('Reading times %s to %s in %d iterations' % (qa.time(qa.quantity(starttime_mjd + timeskip / 86400.0, 'd'), form=['hms'], prec=9)[0], qa.time(qa.quantity(starttime_mjd + (timeskip + (d['nints'] + 1) * d['inttime']) / 86400.0, 'd'), form=['hms'], prec=9)[0], d['nthread']))
    ms.open(d['filename'])
    if len(d['spwlist']) == 1:
        ms.selectinit(datadescid=d['spwlist'][0])
    else:
        ms.selectinit(datadescid=0, reset=True)
    selection = {'time': [starttime, stoptime], 'uvdist': [1.0, 10000000000.0], 'antenna1': d['ants'], 'antenna2': d['ants']}
    ms.select(items=selection)
    ms.selectpolarization(d['pols'])
    ms.iterinit(['TIME'], 0, d['iterint'] * d['nbl'] * d['nspw'] * d['npol'], adddefaultsortcolumns=False)
    iterstatus = ms.iterorigin()


def readiter(d):
    """ Read iteration of size iterint
    """
    da = ms.getdata([d['datacol'], 'axis_info', 'u', 'v', 'w', 'flag', 'data_desc_id'], ifraxis=True)
    good = n.where(da['data_desc_id'] == d['spwlist'][0])[0]
    time0 = da['axis_info']['time_axis']['MJDseconds'][good]
    data0 = n.transpose(da[d['datacol']], axes=[3, 2, 1, 0])[good]
    flag0 = n.transpose(da['flag'], axes=[3, 2, 1, 0])[good]
    u0 = da['u'].transpose()[good] * d['freq_orig'][0] * (1000000000.0 / 300000000.0)
    v0 = da['v'].transpose()[good] * d['freq_orig'][0] * (1000000000.0 / 300000000.0)
    w0 = da['w'].transpose()[good] * d['freq_orig'][0] * (1000000000.0 / 300000000.0)
    if len(d['spwlist']) > 1:
        for spw in d['spwlist'][1:]:
            good = n.where(da['data_desc_id'] == spw)[0]
            data1 = n.transpose(da[d['datacol']], axes=[3, 2, 1, 0])[good]
            data0 = n.concatenate((data0, data1), axis=2)
            flag0 = n.concatenate((flag0, n.transpose(da['flag'], axes=[3, 2, 1, 0])[good]), axis=2)

    del da
    data0 = data0[:, :, d['chans'], :] * n.invert(flag0[:, :, d['chans'], :])
    iterstatus = ms.iternext()
    return (
     data0.astype('complex64'), u0.astype('float32'), v0.astype('float32'), w0.astype('float32'), time0.astype('float32'))


def readsegment(d, segment):
    """ Prepare to read segment of data
    """
    starttime = qa.getvalue(qa.convert(qa.time(qa.quantity(d['segmenttimes'][(segment, 0)], 'd'), form=['ymd'], prec=9)[0], 's'))[0]
    stoptime = qa.getvalue(qa.convert(qa.time(qa.quantity(d['segmenttimes'][(segment, 1)], 'd'), form=['ymd'], prec=9)[0], 's'))[0]
    logger.info('Reading segment %d/%d, times %s to %s' % (segment, len(d['segmenttimes']) - 1, qa.time(qa.quantity(starttime / 86400, 'd'), form=['hms'], prec=9)[0], qa.time(qa.quantity(stoptime / 86400, 'd'), form=['hms'], prec=9)[0]))
    ms.open(d['filename'])
    if len(d['spwlist']) == 1:
        ms.selectinit(datadescid=d['spwlist'][0])
    else:
        ms.selectinit(datadescid=0, reset=True)
    selection = {'time': [starttime, stoptime], 'uvdist': [1.0, 10000000000.0]}
    ms.select(items=selection)
    ms.selectpolarization(d['pols'])
    da = ms.getdata([d['datacol'], 'axis_info', 'u', 'v', 'w', 'flag', 'data_desc_id'], ifraxis=True)
    good = n.where(da['data_desc_id'] == d['spwlist'][0])[0]
    time0 = da['axis_info']['time_axis']['MJDseconds'][good]
    data0 = n.transpose(da[d['datacol']], axes=[3, 2, 1, 0])[good]
    flag0 = n.transpose(da['flag'], axes=[3, 2, 1, 0])[good]
    u0 = da['u'].transpose()[good] * d['freq_orig'][0] * (1000000000.0 / 300000000.0)
    v0 = da['v'].transpose()[good] * d['freq_orig'][0] * (1000000000.0 / 300000000.0)
    w0 = da['w'].transpose()[good] * d['freq_orig'][0] * (1000000000.0 / 300000000.0)
    if len(d['spwlist']) > 1:
        for spw in d['spwlist'][1:]:
            good = n.where(da['data_desc_id'] == spw)[0]
            data1 = n.transpose(da[d['datacol']], axes=[3, 2, 1, 0])[good]
            data0 = n.concatenate((data0, data1), axis=2)
            flag0 = n.concatenate((flag0, n.transpose(da['flag'], axes=[3, 2, 1, 0])[good]), axis=2)

    del da
    data0 = data0[:, :, d['chans'], :] * n.invert(flag0[:, :, d['chans'], :])
    return (
     data0.astype('complex64'), u0.astype('float32'), v0.astype('float32'), w0.astype('float32'))