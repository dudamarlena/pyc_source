# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/SWHT/fileio.py
# Compiled at: 2017-08-08 14:46:57
"""
functions to read/write data for the imagers
"""
import cPickle as pkl, numpy as np, datetime, ephem, ecef, lofarConfig, util

def parse(fn, fmt=None):
    """Parse an input visibility filename to determine meta data and type
    XST files are assumed to follow the SE607 format: <date>_<time>_rcu<id>_sb<subband>_int<integration length>_dur<duration of observation>[_<HBA config in hex>]_xst.dat
    fmt: if None then automatically determines format based on filename, else can be set to 'ms' (measurement set), 'acc' (LOFAR ACC), 'xst' (LOFAR XST)
    returns: dictionary"""
    fDict = {}
    fDict['fn'] = fn
    if fn.lower().endswith('.ms') or fmt == 'ms':
        fDict['fmt'] = 'ms'
    elif fmt == 'KAIRA':
        fDict['fmt'] = fmt
        metaData = fn.split('/')[(-1)].split('_')
        fDict['ts'] = datetime.datetime(year=int(metaData[0][:4]), month=int(metaData[0][4:6]), day=int(metaData[0][6:]), hour=int(metaData[1][:2]), minute=int(metaData[1][2:4]), second=int(metaData[1][4:]))
        fDict['rcu'] = 1
        fDict['sb'] = np.array([195])
        fDict['int'] = 1.0
        fDict['dur'] = 1.0
    elif fn.lower().endswith('.dat') or fn.lower().endswith('.dat.sim') or fmt == 'acc' or fmt == 'xst':
        metaData = fn.split('/')[(-1)].split('_')
        fDict['ts'] = datetime.datetime(year=int(metaData[0][:4]), month=int(metaData[0][4:6]), day=int(metaData[0][6:]), hour=int(metaData[1][:2]), minute=int(metaData[1][2:4]), second=int(metaData[1][4:]))
        if metaData[2].startswith('acc'):
            fDict['fmt'] = 'acc'
            fDict['shape'] = map(int, metaData[3].split('.')[0].split('x'))
        elif metaData[(-1)].startswith('xst.dat'):
            fDict['fmt'] = 'xst'
            fDict['rcu'] = int(metaData[2][3:])
            fDict['sb'] = np.array([int(metaData[3][2:])])
            fDict['int'] = float(metaData[4][3:])
            fDict['dur'] = float(metaData[5][3:])
            if len(metaData) == 8:
                fDict['elem'] = metaData[6][2:]
    elif fn.lower().endswith('.pkl') or fmt == 'pkl':
        fDict['fmt'] = 'pkl'
    else:
        fDict['fmt'] = -1
    return fDict


def writeCoeffPkl(fn, coeffs, phs=[
 0.0, 0.0], lst=0.0):
    """Write SWHT image coefficients to file
    fn: str, pickle filename
    coeffs: 2D array of complex coefficients
    phs: [float, float], RA and Dec (radians) position at the center of the image
    lst: float, local sidereal time of snapshot
    """
    coeffDict = {'coeffs': coeffs, 
       'phs': phs, 
       'lst': lst}
    fh = open(fn, 'wb')
    pkl.dump(coeffDict, fh)
    fh.close()


def readCoeffPkl(fn):
    """Read SWHT image coefficients from a pickle file, see writeCoeffPkl() for contents"""
    fh = open(fn, 'rb')
    coeffDict = pkl.load(fh)
    fh.close()
    return coeffDict


def writeImgPkl(fn, d, fDict, res=None, fttype=None, imtype=None):
    """Write an image cube to a pickle file
    fn: str, pickle filename
    d: numpy array, image data
    fDict: dict, meta data from original visibility file
    res: float, resolution at zenith (radians)
    fftype: str, dft or fft convolution function name
    imtype: str, complex or Stokes"""
    imgDict = {'meta': fDict, 
       'res': res, 
       'fttype': fttype, 
       'imtype': imtype, 
       'img': d}
    fh = open(fn, 'wb')
    pkl.dump(imgDict, fh)
    fh.close()


def readImgPkl(fn):
    """Read an image cube from a pickle file, see writeImgPkl() for contents"""
    fh = open(fn, 'rb')
    imgDict = pkl.load(fh)
    fh.close()
    return imgDict


def writeSWHTImgPkl(fn, d, fDict, mode):
    """Write a SWHT image cube to a pickle file
    fn: str, pickle filename
    d: numpy array, image data
    fDict: dict, meta data from original visibility file
    """
    imgDict = {'meta': fDict, 
       'mode': mode}
    if mode.startswith('3D'):
        imgDict['img'] = d[0]
        imgDict['phi'] = d[1]
        imgDict['theta'] = d[2]
    else:
        imgDict['img'] = d
    fh = open(fn, 'wb')
    pkl.dump(imgDict, fh)
    fh.close()


def readSWHTImgPkl(fn):
    """Read an image cube from a pickle file, see writeSWHTImgPkl() for contents"""
    fh = open(fn, 'rb')
    imgDict = pkl.load(fh)
    fh.close()
    return imgDict


def lofarArrayLatLong(lofarStation, arrayType='LBA'):
    """Return the Latitude, Longitude, Elevation of a LOFAR station
    lofarStation: instance, see lofarConfig.py
    arrayType: string, LOFAR array type

    returns: latitude (degs), longitude (degs), elevation (m)
    """
    arr_xyz = lofarStation.antField.location[arrayType]
    lat, lon, elev = ecef.ecef2geodetic(arr_xyz[0], arr_xyz[1], arr_xyz[2], degrees=True)
    print 'LON(deg):', lon, 'LAT(deg):', lat, 'ELEV(m):', elev
    return (
     lat, lon, elev)


def lofarHBAAntPositions(ants, lofarStation, elem):
    """Update the antenna positions using the HBADeltas file
    ants: [nants, 3] array, antenna positions in XYZ
    lofarStation: instance, see lofarConfig.py
    elem: hex/base-16 string of tile element IDs

    returns: updated [N, 3] antenna position array
    """
    if lofarStation.deltas is None:
        print 'Warning: HBA element string found, but HBADeltas file is missing, your image is probably not going to make sense'
    else:
        print 'Updating antenna positions with HBA element deltas'
        for aid in np.arange(ants.shape[0]):
            delta = lofarStation.deltas[int(elem[aid], 16)]
            delta = np.array([delta, delta])
            ants[aid] += delta

    return ants


def lofarFreqs(fDict, sbs):
    """Compute Frequency information from file meta data and subbands
    fDict: dictionary, file meta data, see parse()
    sbs: 1D array, subband IDs

    returns: [Nsubbands] array with frequency values in Hz
    """
    nchan = lofarConfig.rcuInfo[fDict['rcu']]['nchan']
    bw = lofarConfig.rcuInfo[fDict['rcu']]['bw']
    df = bw / nchan
    freqs = sbs * df + lofarConfig.rcuInfo[fDict['rcu']]['offset'] + df / 2.0
    return (
     freqs, nchan, bw)


def lofarACCSelectSbs(fn, sbs, nchan, nantpol, intTime, antGains=None):
    """Select subband correlation matricies from ACC file
    fn: string, ACC filename
    sbs: [Nsubbands] array
    nchan: int, number of total frequnecy channels
    nantpol: int, number of antenna-polarizations
    intTime: float, integration time in seconds
    antGains: antenna gains from lofarConfig.readCalTable()

    returns:
        sbCorrMatrix: correlation matrix from each subband [Nsubbands, 1, nantpol, nantpol]
        tDeltas: 2D array [Nsubbands, 1], time offsets for each subband from end of file timestep [Nsubbands]
    """
    tDeltas = []
    corrMatrix = np.fromfile(fn, dtype='complex').reshape(nchan, nantpol, nantpol)
    sbCorrMatrix = np.zeros((sbs.shape[0], nantpol, nantpol), dtype=complex)
    for sbIdx, sb in enumerate(sbs):
        if antGains is None:
            sbCorrMatrix[sbIdx] = corrMatrix[sb, :, :]
        else:
            sbAntGains = antGains[sb][np.newaxis].T
            sbVisGains = np.conjugate(np.dot(sbAntGains, sbAntGains.T))
            sbCorrMatrix[sbIdx] = np.multiply(sbVisGains, corrMatrix[sb, :, :])
        tOffset = (nchan - sb) * intTime
        rem = tOffset - int(tOffset)
        tDeltas.append(datetime.timedelta(0, int(tOffset), rem * 1000000.0))

    tDeltas = np.reshape(np.array(tDeltas), (sbs.shape[0], 1))
    sbCorrMatrix = np.reshape(sbCorrMatrix, (sbs.shape[0], 1, nantpol, nantpol))
    print 'CORRELATION MATRIX SHAPE', corrMatrix.shape
    print 'REDUCED CORRELATION MATRIX SHAPE', sbCorrMatrix.shape
    return (
     sbCorrMatrix, tDeltas)


def lofarSE607XST(fn, sb, nantpol, antGains=None):
    """Read in correlation matrix from a SE607 format XST file
    fn: string, XST filename
    sb: [int], subband ID, 1 element list for consistency with lofarACCSelectSbs()
    nantpol: int, number of antenna-polarizations
    antGains: antenna gains from lofarConfig.readCalTable()

    returns:
        sbCorrMatrix: correlation matrix from each subband [1, 1, nantpol, nantpol] for consistency with lofarACCSelectSbs()
        tDeltas: 2D array [1, 1], time offset from end of file timestep, set to 0 but kept for consistency with lofarACCSelectSbs()
    """
    corrMatrix = np.fromfile(fn, dtype='complex').reshape(1, nantpol, nantpol)
    if antGains is None:
        sbCorrMatrix = corrMatrix
    else:
        sbAntGains = antGains[sb][np.newaxis].T
        sbVisGains = np.conjugate(np.dot(sbAntGains, sbAntGains.T))
        sbCorrMatrix = np.multiply(sbVisGains, corrMatrix)
    tDeltas = [
     datetime.timedelta(0, 0)]
    tDeltas = np.array(tDeltas)[np.newaxis]
    sbCorrMatrix = np.reshape(sbCorrMatrix, (1, 1, nantpol, nantpol))
    print 'CORRELATION MATRIX SHAPE', corrMatrix.shape
    print 'REDUCED CORRELATION MATRIX SHAPE', sbCorrMatrix.shape
    return (
     sbCorrMatrix, tDeltas)


def lofarKAIRAXST(fn, sb, nantpol, intTime, antGains=None, times='0'):
    """Read in correlation matrix from a KAIRA format XST file
    fn: string, XST filename
    sb: [int], subband ID, 1 element list for consistency with lofarACCSelectSbs()
    nantpol: int, number of antenna-polarizations
    antGains: antenna gains from lofarConfig.readCalTable()
    times: the KAIRA XST files contain ~3600 integrations of 1 second each, this will result in a slow SWHT, to reduce this a number of options can be used
        i) a[seconds] : average together integrations into correlation matrixs for every block of time, e.g. times='a600' will average for 600 seconds, which is reasonable for the low resolution KAIRA station
        ii) select unique integrations: for multiple integrations use X,Y,Z and for range use X_Y notation, these can be combined, e.g. 0,100,200,300_310,400, default to function is to select only the first integration
        iii) d[step size]: decimate the integrations to select an integration every 'step size', e.g. d600 will select every 600th integration

    returns:
        reducedCorrMatrix: correlation matrix from each subband and integration [1, tids.size, nantpol, nantpol] for consistency with lofarACCSelectSbs()
        tDeltas: 2D array [1, tids.size], time offset from end of file timestep, for consistency with lofarACCSelectSbs()
    """
    corrMatrix = np.fromfile(fn, dtype='complex')
    nints = corrMatrix.shape[0] / (nantpol * nantpol)
    corrMatrix = np.reshape(corrMatrix, (nints, nantpol, nantpol))
    if times.startswith('a'):
        intLen = float(times[1:]) * intTime
        nAvgInts = int(nints / intLen)
        print 'KAIRA: avergaing XST file to %.2f second integrations, this will produce %i integrations' % (intLen, nAvgInts)
        reducedCorrMatrix = np.mean(corrMatrix[:int(intLen * nAvgInts)].reshape(nAvgInts, intLen, nantpol, nantpol), axis=1)
        tids = np.linspace(intLen / 2.0, intLen * (nAvgInts - 0.5), nAvgInts)
    else:
        if times.startswith('d'):
            decimateFactor = int(times[1:])
            tids = np.arange(nints)[::decimateFactor]
            print 'KAIRA: decimating XST file to %i integrations' % tids.shape[0]
            reducedCorrMatrix = corrMatrix[tids]
        else:
            tids = np.array(util.convert_arg_range(times))
            print 'KAIRA: selecting %i unique integrations' % tids.shape[0]
            reducedCorrMatrix = corrMatrix[tids]
        tDeltas = []
        if antGains is not None:
            sbAntGains = antGains[sb][np.newaxis].T
            sbVisGains = np.conjugate(np.dot(sbAntGains, sbAntGains.T))
            reducedCorrMatrix = sbVisGains * reducedCorrMatrix
        for tIdx, tid in enumerate(tids):
            tOffset = (nints - tid - 1) * intTime
            rem = tOffset - int(tOffset)
            tDeltas.append(datetime.timedelta(0, int(tOffset), rem * 1000000.0))

    tDeltas = np.array(tDeltas)[np.newaxis]
    reducedCorrMatrix = np.reshape(reducedCorrMatrix, (1, tids.shape[0], nantpol, nantpol))
    print 'ORIGINAL CORRELATION MATRIX SHAPE', corrMatrix.shape
    print 'REDUCED CORRELATION MATRIX SHAPE', reducedCorrMatrix.shape
    return (
     reducedCorrMatrix, tDeltas)


def lofarObserver(lat, lon, elev, ts):
    """Create an ephem Observer for a LOFAR station
    lat: float, latitude (deg)
    lon: float, longitude (deg)
    elev: float, elevation (m)
    ts: datetime, EOF timestamp

    returns: ephem.Observer()
    """
    obs = ephem.Observer()
    obs.long = lon * (np.pi / 180.0)
    obs.lat = lat * (np.pi / 180.0)
    obs.elevation = float(elev)
    obs.epoch = ts
    obs.date = ts
    return obs


def lofarGenUVW(corrMatrix, ants, obs, sbs, ts):
    """Generate UVW coordinates from antenna positions, timestamps/subbands
    corrMatrix: [Nsubbands, Nints, nantpol, nantpol] array, correlation matrix for each subband, time integration
    ants: [Nantennas, 3] array, antenna positions in XYZ
    obs: ephem.Observer() of station
    sbs: [Nsubbands] array, subband IDs
    ts: datetime 2D array [Nsubbands, Nints], timestamp for each correlation matrix

    returns:
        vis: visibilities [4, Nsamples*Nints, Nsubbands]
        uvw: UVW coordinates [Nsamples*Nints, 3, Nsubbands]
    """
    nants = ants.shape[0]
    ncorrs = nants * (nants + 1) / 2
    nints = ts.shape[1]
    uvw = np.zeros((nints, ncorrs, 3, len(sbs)), dtype=float)
    vis = np.zeros((4, nints, ncorrs, len(sbs)), dtype=complex)
    for sbIdx, sb in enumerate(sbs):
        for tIdx in np.arange(nints):
            refObs = lofarObserver(0.0, -90.0, 0.0, ts[(sbIdx, tIdx)])
            LSTangle = refObs.sidereal_time()
            print 'LST:', LSTangle, 'Dec:', obs.lat
            antPosRep = np.repeat(ants[:, 0, :], nants, axis=0).reshape((nants, nants, 3))
            xyz = util.vectorize(antPosRep - np.transpose(antPosRep, (1, 0, 2)))
            dec = float(np.pi / 2.0)
            decRotMat = np.array([[1.0, 0.0, 0.0],
             [
              0.0, np.sin(dec), np.cos(dec)],
             [
              0.0, -1.0 * np.cos(dec), np.sin(dec)]])
            ha = float(LSTangle) - 0.0
            haRotMat = np.array([[np.sin(ha), np.cos(ha), 0.0],
             [
              -1.0 * np.cos(ha), np.sin(ha), 0.0],
             [
              0.0, 0.0, 1.0]])
            rotMatrix = np.dot(decRotMat, haRotMat)
            uvw[tIdx, :, :, sbIdx] = np.dot(rotMatrix, xyz.T).T
            vis[0, tIdx, :, sbIdx] = util.vectorize(corrMatrix[sbIdx, tIdx, 0::2, 0::2])
            vis[1, tIdx, :, sbIdx] = util.vectorize(corrMatrix[sbIdx, tIdx, 1::2, 0::2])
            vis[2, tIdx, :, sbIdx] = util.vectorize(corrMatrix[sbIdx, tIdx, 0::2, 1::2])
            vis[3, tIdx, :, sbIdx] = util.vectorize(corrMatrix[sbIdx, tIdx, 1::2, 1::2])

    vis = np.reshape(vis, (vis.shape[0], vis.shape[1] * vis.shape[2], vis.shape[3]))
    uvw = np.reshape(uvw, (uvw.shape[0] * uvw.shape[1], uvw.shape[2], uvw.shape[3]))
    return (
     vis, uvw, LSTangle)


def readACC(fn, fDict, lofarStation, sbs, calTable=None):
    """Return the visibilites and UVW coordinates from a LOFAR station ACC file
    fn: ACC filename
    fDict: dictionary of file format meta data, see parse()
    lofarStation: instance, see lofarConfig.py
    sbs: 1-D array of subband IDs (in range 0-511)
    calTable: station gain calibration table filename

    returns:
        vis: visibilities [4, Nsamples, Nsubbands]
        uvw: UVW coordinates [Nsamples, 3, Nsubbands]
        freqs: frequencies [Nsubbands]
        obsdata: [latitude, longitude, LST]
    """
    lat, lon, elev = lofarArrayLatLong(lofarStation, lofarConfig.rcuInfo[fDict['rcu']]['array_type'])
    ants = lofarStation.antField.antpos[lofarConfig.rcuInfo[fDict['rcu']]['array_type']]
    if 'elem' in fDict:
        ants = lofarHBAAntPositions(ants, lofarStation, fDict['elem'])
    nants = ants.shape[0]
    print 'NANTENNAS:', nants
    freqs, nchan, bw = lofarFreqs(fDict, sbs)
    print 'SUBBANDS:', sbs, '(', freqs / 1000000.0, 'MHz)'
    npols = 2
    if calTable is not None:
        if antGains is None:
            print 'Using CalTable:', calTable
            antGains = lofarConfig.readCalTable(calTable, nants, nchan, npols)
    else:
        antGains = None
    nantpol = nants * npols
    print 'Reading in visibility data file ...',
    corrMatrix, tDeltas = lofarACCSelectSbs(fn, sbs, nchan, nantpol, fDict['int'], antGains)
    print 'done'
    obs = lofarObserver(lat, lon, elev, fDict['ts'])
    obsLat = float(obs.lat)
    obsLong = float(obs.long)
    print 'Observatory:', obs
    vis, uvw, LSTangle = lofarGenUVW(corrMatrix, ants, obs, sbs, fDict['ts'] - np.array(tDeltas))
    return (
     vis, uvw, freqs, [obsLat, obsLong, LSTangle])


def readSE607XST(fn, fDict, lofarStation, sbs, calTable=None):
    """Return the visibilites and UVW coordinates from a SE607 LOFAR XST format file
    fn: XST filename
    fDict: dictionary of file format meta data, see parse()
    lofarStation: instance, see lofarConfig.py
    sbs: 1-D array of subband IDs (in range 0-511)
    calTable: station gain calibration table filename

    returns:
        vis: visibilities [4, Nsamples, Nsubbands]
        uvw: UVW coordinates [Nsamples, 3, Nsubbands]
        freqs: frequencies [Nsubbands]
        obsdata: [latitude, longitude, LST]
    """
    lat, lon, elev = lofarArrayLatLong(lofarStation, lofarConfig.rcuInfo[fDict['rcu']]['array_type'])
    ants = lofarStation.antField.antpos[lofarConfig.rcuInfo[fDict['rcu']]['array_type']]
    if 'elem' in fDict:
        ants = lofarHBAAntPositions(ants, lofarStation, fDict['elem'])
    nants = ants.shape[0]
    print 'NANTENNAS:', nants
    freqs, nchan, bw = lofarFreqs(fDict, sbs)
    print 'SUBBANDS:', sbs, '(', freqs / 1000000.0, 'MHz)'
    npols = 2
    if calTable is not None:
        if antGains is None:
            print 'Using CalTable:', calTable
            antGains = lofarConfig.readCalTable(calTable, nants, nchan, npols)
    else:
        antGains = None
    nantpol = nants * npols
    print 'Reading in visibility data file ...',
    corrMatrix, tDeltas = lofarSE607XST(fn, fDict['sb'], nantpol, antGains)
    print 'done'
    obs = lofarObserver(lat, lon, elev, fDict['ts'])
    obsLat = float(obs.lat)
    obsLong = float(obs.long)
    print 'Observatory:', obs
    vis, uvw, LSTangle = lofarGenUVW(corrMatrix, ants, obs, sbs, fDict['ts'] - np.array(tDeltas))
    return (
     vis, uvw, freqs, [obsLat, obsLong, LSTangle])


def readKAIRAXST(fn, fDict, lofarStation, sbs, calTable=None, times='0'):
    """Return the visibilites and UVW coordinates from a KAIRA LOFAR XST format file
    fn: XST filename
    fDict: dictionary of file format meta data, see parse()
    lofarStation: instance, see lofarConfig.py
    sbs: 1-D array of subband IDs (in range 0-511)
    calTable: station gain calibration table filename
    times: the KAIRA XST files contain ~3600 integrations of 1 second each, this will result in a slow SWHT, to reduce this a number of options can be used
        i) a[seconds] : average together integrations into correlation matrixs for every block of time, e.g. times='a600' will average for 600 seconds, which is reasonable for the low resolution KAIRA station
        ii) select unique integrations: for multiple integrations use X,Y,Z and for range use X_Y notation, these can be combined, e.g. 0,100,200,300_310,400, default to function is to select only the first integration
        iii) d[step size]: decimate the integrations to select an integration every 'step size', e.g. d600 will select every 600th integration

    returns:
        vis: visibilities [4, Nsamples, Nsubbands]
        uvw: UVW coordinates [Nsamples, 3, Nsubbands]
        freqs: frequencies [Nsubbands]
        obsdata: [latitude, longitude, LST]
    """
    lat, lon, elev = lofarArrayLatLong(lofarStation, lofarConfig.rcuInfo[fDict['rcu']]['array_type'])
    ants = lofarStation.antField.antpos[lofarConfig.rcuInfo[fDict['rcu']]['array_type']]
    if 'elem' in fDict:
        ants = lofarHBAAntPositions(ants, lofarStation, fDict['elem'])
    nants = ants.shape[0]
    print 'NANTENNAS:', nants
    freqs, nchan, bw = lofarFreqs(fDict, sbs)
    print 'SUBBANDS:', sbs, '(', freqs / 1000000.0, 'MHz)'
    npols = 2
    if calTable is not None:
        if antGains is None:
            print 'Using CalTable:', calTable
            antGains = lofarConfig.readCalTable(calTable, nants, nchan, npols)
    else:
        antGains = None
    nantpol = nants * npols
    print 'Reading in visibility data file ...',
    corrMatrix, tDeltas = lofarKAIRAXST(fn, fDict['sb'], nantpol, fDict['int'], antGains, times=times)
    print 'done'
    obs = lofarObserver(lat, lon, elev, fDict['ts'])
    obsLat = float(obs.lat)
    obsLong = float(obs.long)
    print 'Observatory:', obs
    vis, uvw, LSTangle = lofarGenUVW(corrMatrix, ants, obs, sbs, fDict['ts'] - np.array(tDeltas))
    return (
     vis, uvw, freqs, [obsLat, obsLong, LSTangle])


def readMS(fn, sbs, column='DATA'):
    """Return the visibilites and UVW coordinates from a SE607 LOFAR XST format file
    fn: XST filename
    column: string, data column
    sbs: 1-D array of subband IDs

    returns:
        vis: visibilities [4, Nsamples, Nsubbands]
        uvw: UVW coordinates [Nsamples, 3, Nsubbands]
        freqs: frequencies [Nsubbands]
        obsdata: [latitude, longitude, LST]
    """
    try:
        import casacore.tables as tbls
    except ImportError:
        print 'ERROR: could not import casacore.tables, cannot read measurement sets'
        exit(1)

    MS = tbls.table(fn, readonly=True)
    data_column = column.upper()
    uvw = MS.col('UVW').getcol()
    vis = MS.col(data_column).getcol()
    vis = vis[:, sbs, :]
    MS.close()
    ANTS = tbls.table(fn + '/ANTENNA')
    positions = ANTS.col('POSITION').getcol()
    ant0Lat, ant0Long, ant0hgt = ecef.ecef2geodetic(positions[(0, 0)], positions[(0,
                                                                                  1)], positions[(0,
                                                                                                  2)], degrees=False)
    ANTS.close()
    SRC = tbls.table(fn + '/SOURCE')
    direction = SRC.col('DIRECTION').getcol()
    obsLat = direction[(0, 1)]
    obsLong = ant0Long
    LSTangle = direction[(0, 0)]
    SRC.close()
    SW = tbls.table(fn + '/SPECTRAL_WINDOW')
    freqs = SW.col('CHAN_FREQ').getcol()[(0, sbs)]
    print 'SUBBANDS:', sbs, '(', freqs / 1000000.0, 'MHz)'
    SW.close()
    print 'LST:', LSTangle
    rotAngle = float(LSTangle) - obsLong
    rotAngle += np.pi
    rotAngle *= -1
    rotMatrix = np.array([[np.cos(rotAngle), -1.0 * np.sin(rotAngle), 0.0],
     [
      np.sin(rotAngle), np.cos(rotAngle), 0.0],
     [
      0.0, 0.0, 1.0]])
    uvwRot = np.dot(uvw, rotMatrix).reshape(uvw.shape[0], uvw.shape[1], 1)
    uvwRotRepeat = np.repeat(uvwRot, len(sbs), axis=2)
    return (
     np.transpose(vis, (2, 0, 1)), uvwRotRepeat, freqs, [obsLat, obsLong, LSTangle])


if __name__ == '__main__':
    print 'Running test cases...'
    fDict = parse('../examples/20150607_122433_acc_512x192x192.dat')
    print fDict
    fDict = parse('../examples/zen.2455819.26623.uvcRREM.MS')
    print fDict
    fDict = parse('../examples/20150915_191137_rcu5_sb60_int10_dur10_elf0f39fe2034ea85fc02b3cc1544863053b328fd83291e880cd0bf3c3d3a50a164a3f3e0c070c73d073f4e43849c0e93b_xst.dat')
    print fDict
    fDict = parse('20160228_040005_xst.dat', fmt='KAIRA')
    print fDict
    print '...Made it through without errors'