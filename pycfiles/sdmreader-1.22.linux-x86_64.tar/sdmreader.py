# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/claw/miniconda/envs/dev/lib/python2.7/site-packages/sdmreader/sdmreader.py
# Compiled at: 2016-02-05 19:47:08
""" sdmreader -- functions for reading data and metadata from SDM format files

Functions:

read_bdf -- reads data from binary data format and returns numpy array.
calc_uvw -- parses metadata to calculate uvw coordinates for given scan (or time/direction). returns (u,v,w) tuple. Requires CASA libraries.
read_metadata -- parses metadata of SDM file (xml format) to return tuple with two dictionaries (scaninfo, sourceinfo). Scan info defines BDF location per scan.

BDFData class does the heavy lifting to parse binary data format and return numpy array. Does not yet parse flag table.

Note: baseline order used in the bdf is a bit unusual and different from what is assumed when working with a measurement set.
Order of uvw and axis=1 of data array Pythonically would be [i*nants+j for j in range(nants) for i in range(j)], so [ (1,2), (1,3), (2,3), (1,4), ...].
"""
import numpy as np, os, mmap, math, string, sdmpy, logging, cPickle as pickle, xml.etree.ElementTree as et
from email.feedparser import FeedParser
from email.message import Message
logger = logging.getLogger(__name__)

def read_bdf(sdmpath, scan, nskip=0, readints=0, writebdfpkl=False, bdfdir=None):
    """ Reads given range of integrations from sdm of given scan.
    Uses BDFData object to read.
    readints=0 will read all of bdf (skipping nskip).
    Option to write pkl to store bdf info for faster parse next time.
    """
    assert os.path.exists(sdmpath), 'sdmpath %s does not exist' % sdmpath
    scans, sources = read_metadata(sdmpath, scan, bdfdir=bdfdir)
    assert scans[scan]['bdfstr'], 'bdfstr not defined for scan %d' % scan
    bdffile = scans[scan]['bdfstr']
    assert os.path.exists(bdffile), 'Could not find bdf for scan %d and bdfstr %s.' % (scan, scans[scan]['bdfstr'])
    with open(bdffile, 'r') as (fp):
        if writebdfpkl:
            bdfpkldir = os.path.join(sdmpath, 'bdfpkls')
            if not os.path.exists(bdfpkldir):
                os.makedirs(bdfpkldir)
        else:
            bdfpkldir = ''
        bdf = BDFData(fp, bdfpkldir=bdfpkldir).parse()
        if readints == 0:
            readints = bdf.n_integrations - nskip
        logger.info('Reading %d ints starting at int %d' % (readints, nskip))
        data = np.empty((readints, bdf.n_baselines, bdf.n_channels, len(bdf.crosspols)), dtype='complex64', order='C')
        for i in xrange(readints):
            data[i] = bdf.get_data('crossData.bin', i + nskip)

    return data


def calc_uvw(sdmfile, scan=0, datetime=0, radec=()):
    """ Calculates and returns uvw in meters for a given SDM, time, and pointing direction.
    sdmfile is path to sdm directory that includes "Station.xml" file.
    scan is scan number defined by observatory.
    datetime is time (as string) to calculate uvw (format: '2014/09/03/08:33:04.20')
    radec is (ra,dec) as tuple in units of degrees (format: (180., +45.))
    """
    try:
        import casautil
    except ImportError:
        try:
            import pwkit.environments.casa.util as casautil
        except ImportError:
            logger.info('Cannot find pwkit/casautil. No calc_uvw possible.')
            return

    me = casautil.tools.measures()
    qa = casautil.tools.quanta()
    logger.debug('Accessing CASA libraries with casautil.')
    assert os.path.exists(os.path.join(sdmfile, 'Station.xml')), 'sdmfile %s has no Station.xml file. Not an SDM?' % sdmfile
    scans, sources = read_metadata(sdmfile, scan)
    if datetime == 0 and len(radec) == 0:
        assert scan != 0, 'scan must be set when using datetime and radec'
        logger.info('Calculating uvw for first integration of scan %d of source %s' % (scan, scans[scan]['source']))
        datetime = qa.time(qa.quantity(scans[scan]['startmjd'], 'd'), form='ymd', prec=8)[0]
        sourcenum = [ kk for kk in sources.keys() if sources[kk]['source'] == scans[scan]['source'] ][0]
        direction = me.direction('J2000', str(np.degrees(sources[sourcenum]['ra'])) + 'deg', str(np.degrees(sources[sourcenum]['dec'])) + 'deg')
    else:
        if datetime != 0 and len(radec) == 0:
            assert scan != 0, 'scan must be set when using datetime and radec'
            assert '/' in datetime, 'datetime must be in yyyy/mm/dd/hh:mm:ss.sss format'
            logger.info('Calculating uvw at %s for scan %d of source %s' % (datetime, scan, scans[scan]['source']))
            sourcenum = [ kk for kk in sources.keys() if sources[kk]['source'] == scans[scan]['source'] ][0]
            direction = me.direction('J2000', str(np.degrees(sources[sourcenum]['ra'])) + 'deg', str(np.degrees(sources[sourcenum]['dec'])) + 'deg')
        else:
            assert '/' in datetime, 'datetime must be in yyyy/mm/dd/hh:mm:ss.sss format'
            assert len(radec) == 2, 'radec must be (ra,dec) tuple in units of degrees'
            logger.info('Calculating uvw at %s in direction %s' % (datetime, direction))
            logger.info('This mode assumes all antennas used.')
            ra = radec[0]
            dec = radec[1]
            direction = me.direction('J2000', str(ra) + 'deg', str(dec) + 'deg')
        sdm = sdmpy.SDM(sdmfile)
        telescopename = sdm['ExecBlock'][0]['telescopeName'].strip()
        logger.debug('Found observatory name %s' % telescopename)
        me.doframe(me.observatory(telescopename))
        me.doframe(me.epoch('utc', datetime))
        me.doframe(direction)
        if scan != 0:
            configid = [ row.configDescriptionId for row in sdm['Main'] if scan == int(row.scanNumber) ][0]
            antidlist = [ row.antennaId for row in sdm['ConfigDescription'] if configid == row.configDescriptionId ][0].split(' ')[2:]
            stationidlist = [ ant.stationId for antid in antidlist for ant in sdm['Antenna'] if antid == ant.antennaId ]
        else:
            stationidlist = [ ant.stationId for ant in sdm['Antenna'] ]
        positions = [ station.position.strip().split(' ') for station in sdm['Station'] if station.stationId in stationidlist
                    ]
        x = [ float(positions[i][2]) for i in range(len(positions)) ]
        y = [ float(positions[i][3]) for i in range(len(positions)) ]
        z = [ float(positions[i][4]) for i in range(len(positions)) ]
        ants = me.position('itrf', qa.quantity(x, 'm'), qa.quantity(y, 'm'), qa.quantity(z, 'm'))
        bls = me.asbaseline(ants)
        uvwlist = me.expand(me.touvw(bls)[0])[1]['value']
        u = np.empty(len(uvwlist) / 3)
        v = np.empty(len(uvwlist) / 3)
        w = np.empty(len(uvwlist) / 3)
        nants = len(ants['m0']['value'])
        ord1 = [ i * nants + j for i in range(nants) for j in range(i + 1, nants) ]
        ord2 = [ i * nants + j for j in range(nants) for i in range(j) ]
        key = []
        for new in ord2:
            key.append(ord1.index(new))

        for i in range(len(key)):
            u[i] = uvwlist[(3 * key[i])]
            v[i] = uvwlist[(3 * key[i] + 1)]
            w[i] = uvwlist[(3 * key[i] + 2)]

    return (
     u, v, w)


def read_metadata(sdmfile, scan=0, bdfdir=None):
    """ Parses XML files to get scan and source information.
    Returns tuple of dicts (scan, source).
    bdfdir is optional location to look for bdfs, will try that first, then ASDMBinary subdirectory.
    bdfstr in scan dict helps find BDFs with read_bdf (with special behavior for prearchive data.
    Optional arg scan can be used to speed up parsing for single scan.
    """
    sdmfile = sdmfile.rstrip('/')
    if not os.path.exists(sdmfile):
        raise AssertionError('Could not find sdmfile %s.' % sdmfile)
        if bdfdir:
            os.path.exists(bdfdir) or logger.info('bdfdir %s not found' % bdfdir)
            bdfdir = os.path.join(sdmfile, 'ASDMBinary')
    else:
        bdfdir = os.path.join(sdmfile, 'ASDMBinary')
    logger.info('Looking for bdfs in %s' % bdfdir)
    sdmfile = sdmfile.rstrip('/')
    scandict = {}
    sourcedict = {}
    sdm = sdmpy.SDM(sdmfile)
    if len(sdm['Scan']) > 1:
        for i in range(len(sdm['Scan'])):
            row = sdm['Scan'][i]
            scannum = int(row['scanNumber'])
            if scan in [0, scannum]:
                rowkey = [ k for k in row.keys if k.lower() == 'numsubscan' ][0]
                nsubs = int(row[rowkey])
                scanintents = row['scanIntent']
                intentstr = string.join(scanintents.strip().split(' ')[2:], ' ')
                startmjd = float(row['startTime']) * 1e-09 / 86400.0
                endmjd = float(row['endTime']) * 1e-09 / 86400.0
                try:
                    try:
                        src = str(row['sourceName'])
                    except:
                        logger.warn('Scan %d has no source name' % (len(scandict) + 1))

                finally:
                    scandict[scannum] = {}
                    scandict[scannum]['source'] = src
                    scandict[scannum]['startmjd'] = startmjd
                    scandict[scannum]['endmjd'] = endmjd
                    scandict[scannum]['intent'] = intentstr
                    scandict[scannum]['nsubs'] = nsubs
                    scandict[scannum]['duration'] = endmjd - startmjd
                    scandict[scannum]['nints'] = int(sdm['Main'][i]['numIntegration'])

                try:
                    bdfstr = sdm['Main'][i]['dataUID'].replace(':', '_').replace('/', '_')
                except KeyError:
                    bdfstr = sdm['Main'][i]['dataOid'].replace(':', '_').replace('/', '_')

                scandict[scannum]['bdfstr'] = os.path.join(bdfdir, bdfstr)
                if not os.path.exists(scandict[scannum]['bdfstr']) or 'X1' in bdfstr:
                    scandict[scannum]['bdfstr'] = None
                    logger.debug('No bdf found scan %d of %s' % (scannum, sdmfile))
                if scandict[scannum]['source'] not in [ sourcedict[source]['source'] for source in sourcedict.iterkeys() ]:
                    for row in sdm['Field']:
                        src = row['fieldName'].strip()
                        if src == scandict[scannum]['source']:
                            sourcenum = int(row['sourceId'])
                            direction = row['referenceDir'].strip()
                            ra, dec = [ float(val) for val in direction.strip().split(' ')[3:] ]
                            sourcedict[sourcenum] = {}
                            sourcedict[sourcenum]['source'] = src
                            sourcedict[sourcenum]['ra'] = ra
                            sourcedict[sourcenum]['dec'] = dec
                            break

    elif len(sdm['Scan']) == 1 and len(sdm['Subscan']) > 1:
        logger.warn('Found only one scan with multiple subscans. Treating subscans as scans.')
        for row in sdm['Subscan']:
            scannum = int(row['subscanNumber'])
            if scan in [0, scannum]:
                startmjd = float(row['startTime']) * 1e-09 / 86400.0
                endmjd = float(row['endTime']) * 1e-09 / 86400.0
                scanintents = row['subscanIntent']
                if len(scanintents.strip().split(' ')) > 1:
                    intentstr = string.join(scanintents.strip().split(' ')[2:], ' ')
                else:
                    intentstr = scanintents
                try:
                    try:
                        src = row['fieldName'].strip()
                    except:
                        logger.warn('Scan %d has no source name' % (len(scandict) + 1))

                finally:
                    scandict[scannum] = {}
                    scandict[scannum]['source'] = src
                    scandict[scannum]['intent'] = intentstr
                    scandict[scannum]['startmjd'] = startmjd
                    scandict[scannum]['endmjd'] = endmjd
                    scandict[scannum]['duration'] = endmjd - startmjd

    return [
     scandict, sourcedict]


_datatypes = {'autoData.bin': np.complex64, 
   'crossData.bin': np.complex64, 
   'flags.bin': np.uint32}
nanttag = 'numAntenna'
basebandtag = 'baseband'

class BDFData(object):

    def __init__(self, fp, bdfpkldir=''):
        """fp is an open, seekable filestream."""
        self.fp = fp
        self.mmdata = mmap.mmap(fp.fileno(), 0, mmap.MAP_PRIVATE, mmap.PROT_READ)
        if bdfpkldir:
            self.pklname = os.path.join(bdfpkldir, os.path.basename(self.fp.name) + '.pkl')
        else:
            self.pklname = ''

    def parse(self):
        """wrapper for original parse function. will read pkl with bdf info, if available."""
        if os.path.exists(self.pklname):
            logger.info('Found bdf pkl file %s. Loading...' % self.pklname)
            try:
                with open(self.pklname, 'rb') as (pkl):
                    self.mimemsg, self.headxml, self.sizeinfo, self.binarychunks, self.n_integrations, self.n_antennas, self.n_baselines, self.n_basebands, self.n_spws, self.n_channels, self.crosspols = pickle.load(pkl)
            except:
                logger.warning('Something went wrong. Parsing bdf directly...')
                self._parse()

        else:
            if self.pklname:
                logger.info('Could not find bdf pkl file %s.' % self.pklname)
            self._parse()
        self.headsize, self.intsize = self.calc_intsize()
        return self

    def _parse(self):
        """Parse the BDF mime structure and record the locations of the binary
        blobs. Sets up various data fields in the BDFData object."""
        feedparser = FeedParser(Message)
        binarychunks = {}
        sizeinfo = None
        headxml = None
        self.fp.seek(0, 0)
        while True:
            data = self.fp.readline()
            if not data:
                break
            feedparser.feed(data)
            skip = data == '\n' and len(feedparser._msgstack) == 3 and feedparser._msgstack[(-1)].get_content_type() in ('application/octet-stream',
                                                                                                                         'binary/octet-stream')
            if skip:
                msg = feedparser._msgstack[(-1)]
                ident = msg['Content-Location']
                assert ident.endswith('.bin'), 'confusion #1 in hacky MIME parsing!'
                binarychunks[ident] = self.fp.tell()
                if sizeinfo is None:
                    headxml, sizeinfo, tagpfx = _extract_size_info(feedparser)
                kind = ident.split('/')[(-1)]
                assert kind in sizeinfo, 'no size info for binary chunk kind %s in MIME!' % kind
                self.fp.seek(sizeinfo[kind] + 1, 1)
                sample = self.fp.read(16)
                assert sample.startswith('--MIME'), 'crap, unexpected chunk size in MIME parsing: %r' % sample
                self.fp.seek(-16, 1)
            if any([ k.split('/')[3] == '3' for k in binarychunks.iterkeys() ]):
                break

        if headxml is None:
            raise RuntimeError('never found any binary data')
        self.mimemsg = feedparser.close()
        self.headxml = headxml
        self.sizeinfo = sizeinfo
        self.binarychunks = binarychunks
        headsize, intsize = self.calc_intsize()
        self.n_integrations = os.stat(self.fp.name).st_size / intsize
        self.n_antennas = int(headxml.find(tagpfx + nanttag).text)
        self.n_baselines = self.n_antennas * (self.n_antennas - 1) // 2
        ds = headxml.find(tagpfx + dstag)
        nbb = 0
        nspw = 0
        nchan = 0
        crosspolstr = None
        for bb in ds.findall(tagpfx + basebandtag):
            nbb += 1
            for spw in bb.getchildren():
                nspw += 1
                nchan += int(spw.get('numSpectralPoint'))
                if crosspolstr is None:
                    crosspolstr = spw.get('crossPolProducts')
                elif spw.get('crossPolProducts') != crosspolstr:
                    raise Exception('can only handle spectral windows with identical cross pol products')

        self.n_basebands = nbb
        self.n_spws = nspw
        self.n_channels = nchan
        self.crosspols = crosspolstr.split()
        self.n_pols = len(self.crosspols)
        if os.path.exists(os.path.dirname(self.pklname)) and self.pklname and not os.path.exists(self.pklname):
            logger.info('Writing bdf pkl info to %s...' % self.pklname)
            with open(self.pklname, 'wb') as (pkl):
                pickle.dump((self.mimemsg, self.headxml, self.sizeinfo, self.binarychunks, self.n_integrations, self.n_antennas, self.n_baselines, self.n_basebands, self.n_spws, self.n_channels, self.crosspols), pkl)
        return self

    def get_data(self, datakind, integnum):
        """Given an integration number (0 <= integnum < self.n_integrations) and a
        data kind ('crossData.bin', 'autoData.bin'), memory-map the corresponding data
        and return a wrapping numpy array."""
        if integnum < 0 or integnum >= self.n_integrations:
            raise ValueError('illegal integration number %d' % integnum)
        size = self.sizeinfo.get(datakind)
        if size is None:
            raise ValueError('unrecognized data kind "%s"' % datakind)
        dtype = _datatypes[datakind]
        offset = self.headsize + integnum * self.intsize
        dslice = self.mmdata[offset:offset + size]
        data = np.fromstring(dslice, dtype=dtype)
        if datakind == 'crossData.bin':
            data = data.reshape((self.n_baselines, self.n_channels, len(self.crosspols)))
        elif datakind == 'autoData.bin':
            data = data.reshape((self.n_antennas, self.n_channels, 2))
        elif datakind == 'flags.bin':
            data = data.reshape((self.n_baselines + self.n_antennas, self.n_channels,
             len(self.crosspols)))
        return data

    def calc_intsize(self):
        """ Calculates the size of an integration (cross + auto) in bytes
        """
        for k in self.binarychunks.iterkeys():
            if int(k.split('/')[3]) == 1 and 'cross' in k.split('/')[(-1)]:
                headsize = self.binarychunks[k]
                break

        for k in self.binarychunks.iterkeys():
            if int(k.split('/')[3]) == 2 and 'cross' in k.split('/')[(-1)]:
                intsize = self.binarychunks[k] - headsize
                break

        return (
         headsize, intsize)


tagprefixes = [
 '{http://Alma/XASDM/sdmbin}', '']
dstag = 'dataStruct'
cdtag = 'crossData'
adtag = 'autoData'
fgtag = 'flags'

def _extract_size_info(feedparser):
    text = feedparser._msgstack[0].get_payload()[0].get_payload()
    headxml = et.fromstring(text)
    sizeinfo = {}
    for tp in tagprefixes:
        dselem = headxml.find(tp + dstag)
        if dselem is not None:
            break
    else:
        raise RuntimeError('cannot find dataStruct item in any known XML namespace')

    e = dselem.find(tp + cdtag)
    if e is not None:
        sizeinfo['crossData.bin'] = 4 * int(e.attrib['size'])
    e = dselem.find(tp + adtag)
    if e is not None:
        sizeinfo['autoData.bin'] = 4 * int(e.attrib['size'])
    e = dselem.find(tp + fgtag)
    if e is not None:
        sizeinfo['flags.bin'] = 4 * int(e.attrib['size'])
    return (
     headxml, sizeinfo, tp)