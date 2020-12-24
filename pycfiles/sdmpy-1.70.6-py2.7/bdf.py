# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sdmpy/bdf.py
# Compiled at: 2020-01-07 17:38:36
from __future__ import print_function, division, absolute_import, unicode_literals
from builtins import bytes, dict, object, range, map, input
from future.utils import itervalues, viewitems, iteritems, listvalues, listitems
from io import open
import os, sys, re, mmap, math, numpy
from copy import deepcopy
from lxml import etree, objectify
try:
    from progressbar import ProgressBar
except ImportError:
    ProgressBar = None

from .mime import MIMEPart, MIMEHeader
import logging
logger = logging.getLogger(__name__)
_ns = b'{http://Alma/XASDM/sdmbin}'

def basename_noext(path):
    return os.path.basename(os.path.splitext(path)[0])


def _stripns(tag):
    return re.sub(b'{.+}', b'', tag)


def ant2bl(i, j=None):
    """Returns baseline index for given antenna pair.  Will accept
    two args, or a list/tuple/etc.  Uses 0-based indexing"""
    if j is None:
        a1, a2 = sorted(i[:2])
    else:
        a1, a2 = sorted((i, j))
    return a2 * (a2 - 1) // 2 + a1


def bl2ant(i):
    """Returns antenna pair for given baseline index.  All are 0-based."""
    a2 = int(0.5 * (1.0 + math.sqrt(1.0 + 8.0 * i)))
    a1 = i - a2 * (a2 - 1) // 2
    return (a1, a2)


_mmap_default = b'auto'
_mmap_limit = 8 << 30

class BDF(object):
    """
    Class representing a single BDF file.  For example:

        b = bdf.BDF('uid____evla_bdf_1433189755525')

    Individual integration data is returned as BDFIntegration objects via
    either b.get_integration(idx) or b[idx].  Other useful methods include:

        b.basebands      # list of baseband ids
        b.spws           # list of spectral windows per baseband
        b.numAntenna     # number of antennas
        b.numBaseline    # number of baselines
        b.numIntegration # number of integrations in file
        b.sdmDataHeader  # lxml objectify version of full header

    The constructor takes a kwarg, use_mmap to specify whether the data
    are read using mmap versus a simple read().  The former can handle
    arbitrarily large files easily but seems to have poor performance on
    some filesystems (lustre).  If use_mmap=False is specified you must
    ensure there is enough free memory to hold the entire BDF file.
    Allowed values for use_mmap are:
    
        True:       always use mmap
        False:      never use mmap
        'auto':     use mmap for files larger than sdmpy.bdf._mmap_limit
                    (default 8GB) 
        'default':  Apply setting from sdmpy.bdf._mmap_default

    """

    def __init__(self, fname, use_mmap=b'default'):
        self.fname = fname
        try:
            self.fp = open(fname, b'rb')
        except IOError:
            self.fp = None
        else:
            if use_mmap == b'default':
                use_mmap = _mmap_default
            if use_mmap == b'auto':
                fsize = self.fp.seek(0, os.SEEK_END)
                self.fp.seek(0)
                use_mmap = fsize > _mmap_limit
            if use_mmap:
                self.mmdata = mmap.mmap(self.fp.fileno(), 0, mmap.MAP_PRIVATE, mmap.PROT_READ)
            else:
                self.mmdata = self.fp.read()
            self.read_mime()
            self.parse_spws()

        return

    bin_dtype_size = {b'flags': 4, 
       b'actualTimes': 8, 
       b'actualDurations': 8, 
       b'zeroLags': 4, 
       b'autoData': 4, 
       b'crossData': 4}
    bin_dtype = {b'autoData': numpy.float32, 
       b'crossData': numpy.complex64}

    @property
    def exists(self):
        return self.fp is not None

    def read_mime(self, full_read=False):
        if self.fp:
            self.fp.seek(0, 0)
            if not self.fp.readline().decode(b'utf-8').startswith(b'MIME-Version:'):
                raise RuntimeError(b'Invalid BDF: missing MIME-Version')
            mime_hdr = MIMEPart(self.fp).hdr
            self.top_mime_bound = mime_hdr.boundary
            sdmDataMime = MIMEPart(self.fp, boundary=self.top_mime_bound)
            if sdmDataMime.loc != b'sdmDataHeader.xml':
                raise RuntimeError(b'Invalid BDF: missing sdmDataHeader.xml')
            self.sdmDataHeader = objectify.fromstring(bytes(sdmDataMime.body, b'utf-8'))
            self.bin_size = {}
            self.bin_axes = {}
            for e in self.sdmDataHeader.iter():
                if b'size' in list(e.attrib.keys()) and b'axes' in list(e.attrib.keys()):
                    binname = _stripns(e.tag)
                    self.bin_size[binname] = int(e.attrib[b'size']) * self.bin_dtype_size[binname]
                    self.bin_axes[binname] = e.attrib[b'axes'].split()

            if b'EVLA' in mime_hdr[b'Content-Description'][0] and not full_read:
                self.offset_ints = self.fp.tell()
                self.mime_ints = [
                 MIMEPart(self.fp, boundary=self.top_mime_bound, binary_size=self.bin_size, recurse=True)]
                self.size_ints = self.fp.tell() - self.offset_ints
                numints = int((os.path.getsize(self.fname) - self.offset_ints) // self.size_ints)
                self.mime_ints += [None] * (numints - 1)
            else:
                self.fp.seek(0, 0)
                full_mime = MIMEPart(self.fp, recurse=True, binary_size=self.bin_size)
                self.mime_ints = full_mime.body[1:]
        else:
            logger.warn((b'No BDF file found at {0}').format(self.fname))
        return

    def _raw(self, idx):
        if self.fp:
            if self.mime_ints[idx] is not None:
                return self.mime_ints[idx]
            self.fp.seek(self.offset_ints + idx * self.size_ints, 0)
            self.mime_ints[idx] = MIMEPart(self.fp, boundary=self.top_mime_bound, binary_size=self.bin_size, recurse=True)
            return self.mime_ints[idx]
        else:
            logger.warn((b'No BDF file found at {0}').format(self.fname))
            return
            return

    @property
    def projectPath(self):
        return self.sdmDataHeader.attrib[b'projectPath']

    @property
    def numIntegration(self):
        return len(self.mime_ints)

    @property
    def numAntenna(self):
        return int(self.sdmDataHeader.numAntenna)

    @property
    def numBaseline(self):
        return self.numAntenna * (self.numAntenna - 1) // 2

    @property
    def startTime(self):
        return float(self.sdmDataHeader.startTime) / 86400000000000.0

    def parse_spws(self):
        self.basebands = []
        self.spws = []
        cross_offset = 0
        auto_offset = 0
        self.spws = []
        for bb in self.sdmDataHeader.dataStruct.baseband:
            bbname = bb.attrib[b'name']
            self.basebands.append(bbname)
            for spw_elem in bb.spectralWindow:
                spw = BDFSpectralWindow(spw_elem, cross_offset, auto_offset)
                cross_offset += spw.dsize(b'cross')
                auto_offset += spw.dsize(b'auto')
                self.spws.append(spw)

    def get_integration(self, idx):
        return BDFIntegration(self, idx)

    def __getitem__(self, idx):
        return self.get_integration(idx)

    def zerofraction(self, spwidx=b'all', type=b'cross'):
        """
        Return zero fraction for the entire BDF.  This is done by loading
        each integration's data so may take a while.
        """
        tot = 0.0
        for i in self:
            tot += i.zerofraction(spwidx, type)

        return tot / self.numIntegration

    def get_data(self, spwidx=b'all', type=b'cross', scrunch=False, fscrunch=False, frange=None, trange=None, bar=False):
        """Returns an array containing all integrations for the specified
        spw and data type.  Takes a number of options:

          trange: tuple giving range of integrations to return (default=all).
          scrunch: if True, all requested integrations will be time-averaged.
          fscrunch: if True, data will be averaged over the channel axis.
          frange: range of channels to average if using fscrunch.
          bar: if True and the progressbar package is available, display
            a progress bar as data are loaded.

        If spwidx=='all' and no averaging was requested, then the dimensions
        of the returned array are: (time, baseline/antenna, spw, bin, channel,
        polarization).  If a single spw is selected, the spw axis is omitted.
        If time and/or freq averaging is selected, the time and/or channel
        axes are omitted.
        """
        chidx = -2
        if trange is None:
            i0 = 0
            i1 = self.numIntegration
        else:
            i0 = trange[0]
            i1 = trange[1]
        nsubout = i1 - i0
        subdat = self.get_integration(i0).get_data(spwidx, type)
        if scrunch:
            dshape = subdat.shape
        else:
            dshape = (
             nsubout,) + subdat.shape
        if fscrunch:
            dshape = dshape[:chidx] + dshape[chidx + 1:]
        result = numpy.zeros(dshape, dtype=subdat.dtype)
        if bar and ProgressBar is not None:
            b = ProgressBar()
        else:
            b = lambda x: x
        for i in b(list(range(i0, i1))):
            if fscrunch:
                if frange is None:
                    dat = self.get_integration(i).get_data(spwidx, type).mean(chidx)
                else:
                    dat = self.get_integration(i).get_data(spwidx, type).take(list(range(*frange)), axis=chidx).mean(chidx)
            else:
                dat = self.get_integration(i).get_data(spwidx, type)
            if scrunch:
                result += dat
            else:
                result[i - i0] = dat

        if scrunch:
            result /= float(nsubout)
        return result


class BDFSpectralWindow(object):
    """Class that represents spectral window information present in BDF files,
    including storing appropriate offsets into the main data array.  Should be
    initialized from the spectralWindow XML element from the main BDF
    header.

    Alternatively, a BDFSpectralWindow can be generated directly without
    reference to an existing XML element.  In this case, the following
    arguments should be filled in appropriately (names are same as in XML):
        numBin
        numSpectralPoint
        sw
        swbb
    And the npol argument should be set to either 2 or 4; other values are
    not currently handled.

    An XML Element can be generated (eg for output) using the to_xml()
    method.
    """

    def __init__(self, spw_elem, cross_offset=None, auto_offset=None, numBin=None, numSpectralPoint=None, sw=None, swbb=None, npol=None):
        if spw_elem is not None:
            self._attrib = spw_elem.attrib
        else:
            self._attrib = {}
            self._attrib[b'numBin'] = b'%d' % numBin
            self._attrib[b'numSpectralPoint'] = b'%d' % numSpectralPoint
            self._attrib[b'sw'] = b'%d' % sw
            self._attrib[b'swbb'] = str(swbb)
            if npol == 4:
                self._attrib[b'sdPolProducts'] = b'RR RL LL'
                self._attrib[b'crossPolProducts'] = b'RR RL LR LL'
            elif npol == 2:
                self._attrib[b'sdPolProducts'] = b'RR LL'
                self._attrib[b'crossPolProducts'] = b'RR LL'
            else:
                raise RuntimeError(b"Don't know how to handle npol=%d" % npol)
            self._attrib[b'scaleFactor'] = b'1.000000'
            self._attrib[b'sideband'] = b'NOSB'
        self.cross_offset = cross_offset
        self.auto_offset = auto_offset
        return

    def to_xml(self):
        result = etree.Element(b'spectralWindow')
        for k, v in list(self._attrib.items()):
            result.attrib[k] = v

        return result

    @property
    def numBin(self):
        return int(self._attrib[b'numBin'])

    @property
    def numSpectralPoint(self):
        return int(self._attrib[b'numSpectralPoint'])

    @property
    def sw(self):
        return int(self._attrib[b'sw'])

    @property
    def swbb(self):
        return self._attrib[b'swbb']

    @property
    def name(self):
        return self.swbb + b'-' + str(self.sw)

    def pols(self, type):
        """Return number of polarization array elements for the given data
        type (cross or auto)."""
        try:
            if type[0].lower() == b'c':
                return self._attrib[b'crossPolProducts'].split()
            if type[0].lower() == b'a':
                return self._attrib[b'sdPolProducts'].split()
        except KeyError:
            return 0

    def npol(self, type):
        """Return number of polarization array elements for the given data
        type (cross or auto)."""
        pols = self.pols(type=type)
        if type[0].lower() == b'c':
            return len(pols)
        if type[0].lower() == b'a':
            if len(pols) == 3:
                return 4
            return len(pols)

    def dshape(self, type):
        """Return shape tuple of data array for this spectral window,
        in number of data elements (real for auto, complex for cross).
        """
        return (
         self.numBin, self.numSpectralPoint, self.npol(type))

    def dsize(self, type):
        """Return size of data array for this spectral window, in number of
        data elements (real for auto, complex for cross)."""
        return numpy.product(self.dshape(type))

    @staticmethod
    def dims_match(spwlist, type):
        """Given a list of BDFSpectralWindow objects, return true if all
        of them have consistent array dimensions."""
        if len(spwlist) == 1:
            return True
        for spw in spwlist[1:]:
            if spwlist[0].dshape(type) != spw.dshape(type):
                return False

        return True


class BDFIntegration(object):
    """
    Describes and holds data for a single intgration within a BDF file.
    This should be derived from an existing BDF object using
    get_integration() or indexing, ie:

        b = bdf.BDF('some_file')

        # Get the 5th integration, these two are equivalent:
        i = b.get_integration(5)
        i = b[5]

        # Read the cross-corr data array for spectral window 0
        dat = i.get_data(0)

    Other potentially useful info:

        i.basebands            # list of baseband IDs
        i.spws                 # dict of spws per baseband
        i.numAntenna           # obvious
        i.numBaseline          # "
        i.sdmDataSubsetHeader  # lxml objectify version of full sub-header

    """

    def __init__(self, bdf, idx):
        self.sdmDataSubsetHeader = objectify.fromstring(bytes(bdf._raw(idx).body[0].body, b'utf-8'))
        self.basebands = bdf.basebands
        self.spws = bdf.spws
        self.bin_axes = bdf.bin_axes
        self.numAntenna = bdf.numAntenna
        self.numBaseline = bdf.numBaseline
        self.data = {}
        for m in bdf._raw(idx).body[1:]:
            btype = basename_noext(m.loc)
            bsize = bdf.bin_size[btype]
            baxes = self.bin_axes[btype]
            if baxes[0] == b'BAL' and baxes[1] == b'ANT':
                shape = (
                 self.numBaseline + self.numAntenna, -1)
            elif baxes[0] == b'BAL':
                shape = (
                 self.numBaseline, -1)
            elif baxes[0] == b'ANT':
                shape = (
                 self.numAntenna, -1)
            else:
                shape = (-1, )
            self.data[btype] = numpy.frombuffer(bdf.mmdata[m.body:m.body + bsize], dtype=bdf.bin_dtype[btype]).reshape(shape)

    @property
    def projectPath(self):
        return self.sdmDataSubsetHeader.attrib[b'projectPath']

    @property
    def time(self):
        return float(self.sdmDataSubsetHeader.schedulePeriodTime.time) / 86400000000000.0

    @property
    def interval(self):
        return float(self.sdmDataSubsetHeader.schedulePeriodTime.interval) * 1e-09

    def get_data(self, spwidx=b'all', type=b'cross'):
        """
        Return the data array for the given subset.  Inputs are:

            spwidx:    spw index within file
            type:      'cross' or 'auto' (default 'cross')

        The returned array shape is (nBl/nAnt, nBin, nSpp, nPol).

        If spwidx is 'all' and the array dimensions of all spectral
        windows match, all will be returned in a single array.  In this case
        the returned dimensions will be (nBl/nAnt, nSpw, nBin, nSpp, nPol).
        """
        if type[0].lower() == b'c':
            loc = b'crossData'
        else:
            if type[0].lower() == b'a':
                loc = b'autoData'
            else:
                raise RuntimeError(b'Unsupported data type')
            if spwidx == b'all':
                if not BDFSpectralWindow.dims_match(self.spws, type):
                    raise RuntimeError(b'BDFIntegration: ' + b'mixed array dimensions, spws must be ' + b'retrieved indivdually')
                dshape = (
                 -1, len(self.spws)) + self.spws[0].dshape(type)
                return self.data[loc].reshape(dshape)
        spw = self.spws[spwidx]
        if loc == b'crossData':
            offs = spw.cross_offset
        elif loc == b'autoData':
            offs = spw.auto_offset
        else:
            raise RuntimeError(b'Unsupported data type')
        dsize = spw.dsize(type)
        dshape = (-1, ) + spw.dshape(type)
        return self.data[loc][:, offs:offs + dsize].reshape(dshape)

    def zerofraction(self, spwidx=b'all', type=b'cross'):
        """Returns the fraction of data points in the integration that
        are exactly zero (generally this means they have been flagged
        or otherwise not recorded by the online systems).

        Note that for WIDAR autocorrelation data, the default is to only
        record half the antennas so will typically have ~50% zeros
        according to this function."""
        if type[0].lower() == b'c':
            loc = b'crossData'
        elif type[0].lower() == b'a':
            loc = b'autoData'
        if spwidx == b'all':
            dtmp = self.data[loc].ravel()
        else:
            dtmp = self.get_data(spwidx=spwidx, type=type).ravel()
        return float(len(dtmp) - numpy.count_nonzero(dtmp)) / float(len(dtmp))


_nsmap_hdr = {b'xsi': b'http://www.w3.org/2001/XMLSchema-instance', 
   b'xl': b'http://www.w3.org/1999/xlink', 
   b'xv': b'http://Alma/XVERSION', 
   None: b'http://Alma/XASDM/sdmbin'}

def _sdmDataHeader(time, uid, num_antenna, spws, path=b'0/1/1', cross=True, auto=True):
    """Generate a sdmDataHeader XML element from the specified parameters:
        time: start time in SDM format (MJD ns)
        uid: unique ID for the BDF
        num_antenna: number of antennas in the data
        spws: list of BDFSpectralWindow objects; order matters!
    """
    _E = objectify.ElementMaker(annotate=False, nsmap=_nsmap_hdr)
    xl_type = b'{%s}type' % _nsmap_hdr[b'xl']
    xsi_type = b'{%s}type' % _nsmap_hdr[b'xsi']
    xl_href = b'{%s}href' % _nsmap_hdr[b'xl']
    xl_title = b'{%s}title' % _nsmap_hdr[b'xl']
    xsi_schemalocation = b'{%s}schemaLocation' % _nsmap_hdr[b'xsi']
    xv_schemaversion = b'{%s}schemaVersion' % _nsmap_hdr[b'xv']
    xv_revision = b'{%s}revision' % _nsmap_hdr[b'xv']
    xv_release = b'{%s}release' % _nsmap_hdr[b'xv']
    if cross and auto:
        corr_mode = b'CROSS_AND_AUTO'
        data_type = b'CrossAndAutoData'
    else:
        if cross:
            corr_mode = b'CROSS_ONLY'
            data_type = b'CrossData'
        elif auto:
            corr_mode = b'AUTO_ONLY'
            data_type = b'AutoData'
        else:
            raise RuntimeError(b'No data type specified (cross or auto).')
        result = _E.sdmDataHeader(_E.startTime(time), _E.dataOID({xl_type: b'locator', 
           xl_href: uid, 
           xl_title: b'EVLA WIDAR correlator visibility data'}), _E.dimensionality(1, axes=b'TIM'), _E.execBlock({xl_href: uid, xl_type: b'simple'}), _E.numAntenna(num_antenna), _E.correlationMode(corr_mode), _E.spectralResolution(b'FULL_RESOLUTION'), _E.processorType(b'CORRELATOR'), _E.dataStruct({xsi_type: data_type, b'apc': b'AP_UNCORRECTED'}), {xsi_schemalocation: b'http://Alma/XASDM/sdmbin http://almaobservatory.org/XML/XASDM/sdmbin/2/sdmDataObject.xsd', xv_schemaversion: b'2', 
           xv_revision: b'1.1.2.1', 
           xv_release: b'ALMA-6_1_0-B', 
           b'mainHeaderId': b'sdmDataHeader', 
           b'byteOrder': b'Little_Endian', 
           b'projectPath': path})
        cur_bb = None
        auto_size = 0
        cross_size = 0
        for s in spws:
            if s.swbb != cur_bb:
                cur_bb = s.swbb
                bb = _E.baseband(name=cur_bb)
                result.dataStruct.append(bb)
            bb.append(s.to_xml())
            auto_size += s.dsize(b'auto')
            cross_size += s.dsize(b'cross')

    num_baseline = num_antenna * (num_antenna - 1) // 2
    auto_size *= num_antenna
    cross_size *= 2.0 * num_baseline
    if cross:
        result.dataStruct.append(_E.crossData(size=b'%d' % cross_size, axes=b'BAL BAB SPW BIN SPP STO'))
    if auto:
        result.dataStruct.append(_E.autoData(size=b'%d' % auto_size, axes=b'ANT BAB SPW BIN SPP STO', normalized=b'false'))
    return result


_nsmap_subhdr = {b'xsi': b'http://www.w3.org/2001/XMLSchema-instance', 
   b'xl': b'http://www.w3.org/1999/xlink', 
   None: b'http://Alma/XASDM/sdmbin'}

def _sdmDataSubsetHeader(time, interval, cross=True, auto=True, path=b'0/1/1/1/'):
    _E = objectify.ElementMaker(annotate=False, nsmap=_nsmap_subhdr)
    xl_href = b'{%s}href' % _nsmap_subhdr[b'xl']
    xsi_type = b'{%s}type' % _nsmap_subhdr[b'xsi']
    result = _E.sdmDataSubsetHeader(_E.schedulePeriodTime(_E.time(time), _E.interval(interval)), _E.dataStruct(ref=b'sdmDataHeader'), projectPath=path)
    if cross:
        result.append(_E.crossData({b'type': b'FLOAT32_TYPE', 
           xl_href: path + b'crossData.bin'}))
        result.attrib[xsi_type] = b'BinaryCrossDataFXF'
    if auto:
        result.append(_E.autoData({xl_href: path + b'autoData.bin'}))
        result.attrib[xsi_type] = b'BinaryAutoDataFXF'
    if cross and auto:
        result.attrib[xsi_type] = b'BinaryCrossAndAutoDataFXF'
    return result


class BDFWriter(object):
    """
    Write a BDF file.
    """

    def __init__(self, path, fname=None, bdf=None, start_mjd=None, uid=None, num_antenna=None, spws=None, scan_idx=None, subscan_idx=1, corr_mode=None):
        """Init BDFWrite with output filename (fname).  If the bdf
        argument contains a BDF object, its header is copied for the
        output file.  Otherwise the following arguments need to be
        filled in for the header:

            start_mjd: Start time of the BDF in MJD
            uid: UID to put in the header (eg, uid:///evla/bdf/1484080742396)
            num_antenna: Number of antennas
            spws: List of BDFSpectralWindow objects in correct order
            scan_idx: index of this scan in the SDM
            subscan_idx: idx of the subscan in the SDM (default 1)
            corr_mode:  'ca' for cross and auto, 'c' for cross, 'a' for auto
        """
        if fname is not None:
            self.fname = os.path.join(path, fname)
        else:
            self.fname = os.path.join(path, uid.replace(b':/', b'__').replace(b'/', b'_'))
        self.fp = None
        self.curidx = 1
        self.mb1 = b'MIME_boundary-1'
        self.mb2 = b'MIME_boundary-2'
        self.len0 = 0
        self.len1 = 0
        self.len2 = 0
        self.sdmDataHeader = None
        if bdf is not None:
            self.sdmDataHeader = deepcopy(bdf.sdmDataHeader)
        else:
            cross = b'c' in corr_mode
            auto = b'a' in corr_mode
            path = b'0/%d/%d/' % (scan_idx, subscan_idx)
            self.sdmDataHeader = _sdmDataHeader(int(start_mjd * 86400000000000.0), uid, num_antenna, spws, path=path, cross=cross, auto=auto)
        return

    def write_header(self):
        """Open output and write the current header contents."""
        self.fp = open(self.fname, b'wb')
        tophdr = MIMEHeader()
        tophdr[b'MIME-Version'] = [b'1.0']
        tophdr[b'Content-Type'] = [b'multipart/mixed', b'boundary=' + self.mb1]
        tophdr[b'Content-Description'] = [
         b'EVLA/CORRELATOR/WIDAR/FULL_RESOLUTION']
        nsxl = self.sdmDataHeader.nsmap[b'xl']
        uid = self.sdmDataHeader.dataOID.attrib[(b'{%s}href' % nsxl)][5:]
        tophdr[b'Content-Location'] = [b'http://evla.nrao.edu/wcbe/XSDM' + uid]
        self.fp.write(bytes(tophdr.tostring() + b'\n', b'utf-8'))
        self.fp.write(bytes(b'--' + self.mb1 + b'\n', b'utf-8'))
        xhdr = MIMEHeader()
        xhdr[b'Content-Type'] = [b'text/xml', b'charset=utf-8']
        xhdr[b'Content-Location'] = [b'sdmDataHeader.xml']
        self.fp.write(bytes(xhdr.tostring() + b'\n', b'utf-8'))
        self.fp.write(etree.tostring(self.sdmDataHeader, standalone=True, encoding=b'utf-8') + b'\n')

    def write_integration(self, bdf_int=None, mjd=None, interval=None, data=None):
        """
        Input is a BDFIntegration object (bdf_int).  The projectPath will
        be updated so that it is consistent for the file being written but
        otherwise no changes are made to the contents.

        Alternately, rather than a bdf_int, the remaining arguments can be
        filled in (for creating BDFs from scratch):

          mjd: the MJD of the midpoint of the integaration
          interval: the duration of the integration (sec)
          data: a dict whose entries are the numpy data arrays.  The
            keywords should be one or both of 'crossData' and 'autoData'
            depending on whether cross-correlations, auto-correlations, or
            both are present in the data set.
        """
        tophdr = MIMEHeader()
        tophdr[b'Content-Type'] = [b'multipart/related', b'boundary=' + self.mb2]
        tophdr[b'Content-Description'] = [b'data and metadata subset']
        ppidx = self.sdmDataHeader.attrib[b'projectPath'] + b'%d/' % self.curidx
        hdr = MIMEHeader()
        hdr[b'Content-Type'] = [b'text/xml', b'charset=utf-8']
        hdr[b'Content-Location'] = [ppidx + b'desc.xml']
        if self.len0 == 0:
            self.len0 = len(hdr.tostring()) + 12
        nxpad = self.len0 - len(hdr.tostring())
        if nxpad < 0:
            raise RuntimeError(b'nxpad(0)<0')
        hdr[b'X-pad'] = [
         b'*' * nxpad]
        if bdf_int is not None:
            subhdr = deepcopy(bdf_int.sdmDataSubsetHeader)
            data = bdf_int.data
        else:
            cross = b'crossData' in list(data.keys())
            auto = b'autoData' in list(data.keys())
            subhdr = _sdmDataSubsetHeader(int(mjd * 86400000000000.0), int(interval * 1000000000.0), cross=cross, auto=auto)
        subhdr.attrib[b'projectPath'] = ppidx
        nsxl = subhdr.nsmap[b'xl']
        dtypes = []
        mhdr = {}
        for dtype in ('crossData', 'autoData'):
            try:
                loc = ppidx + dtype + b'.bin'
                getattr(subhdr, dtype).attrib[b'{%s}href' % nsxl] = loc
                dtypes += [dtype]
                mhdr[dtype] = MIMEHeader()
                mhdr[dtype][b'Content-Type'] = [b'application/octet-stream']
                mhdr[dtype][b'Content-Location'] = [loc]
            except AttributeError:
                pass

        subhdr_str = etree.tostring(subhdr, standalone=True, encoding=b'utf-8')
        if self.len1 == 0:
            self.len1 = len(subhdr_str) + len(mhdr[dtypes[0]].tostring()) + 50
        nxpad = self.len1 - (len(subhdr_str) + len(mhdr[dtypes[0]].tostring()))
        if nxpad < 0:
            raise RuntimeError(b'nxpad(1)<0')
        mhdr[dtypes[0]][b'X-pad'] = [
         b'*' * nxpad]
        if len(dtypes) > 1:
            if self.len2 == 0:
                self.len2 = len(mhdr[dtypes[1]].tostring()) + 12
            nxpad = self.len2 - len(mhdr[dtypes[1]].tostring())
            if nxpad < 0:
                raise RuntimeError(b'nxpad(2)<0')
            mhdr[dtypes[1]][b'X-pad'] = [
             b'*' * nxpad]
        self.fp.write(bytes(b'--' + self.mb1 + b'\n', b'utf-8'))
        self.fp.write(bytes(tophdr.tostring() + b'\n', b'utf-8'))
        self.fp.write(bytes(b'--' + self.mb2 + b'\n', b'utf-8'))
        self.fp.write(bytes(hdr.tostring() + b'\n', b'utf-8'))
        self.fp.write(subhdr_str)
        for dtype in dtypes:
            self.fp.write(bytes(b'\n--' + self.mb2 + b'\n', b'utf-8'))
            self.fp.write(bytes(mhdr[dtype].tostring() + b'\n', b'utf-8'))
            self.fp.write(data[dtype])

        self.fp.write(bytes(b'\n--' + self.mb2 + b'--\n', b'utf-8'))
        self.curidx += 1
        return

    def close(self):
        self.fp.write(bytes(b'--' + self.mb1 + b'--\n', b'utf-8'))
        self.fp.close()