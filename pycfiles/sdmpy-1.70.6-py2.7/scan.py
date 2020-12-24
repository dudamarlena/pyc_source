# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sdmpy/scan.py
# Compiled at: 2020-01-07 17:38:36
from __future__ import print_function, division, absolute_import, unicode_literals
from builtins import bytes, dict, object, range, map, input
from future.utils import itervalues, viewitems, iteritems, listvalues, listitems
from io import open
import numpy, os.path
from .bdf import BDF, ant2bl, bl2ant

def uid2fname(s):
    """Convert uid URL to file name (mainly for BDFs)."""
    return s.replace(b':/', b'__').replace(b'/', b'_')


def sdmarray(s, dtype=None):
    """Convert an array-valued SDM entry (string) into a numpy array."""
    fields = str(s).split()
    ndim = int(fields[0])
    dims = tuple(map(int, fields[1:ndim + 1]))
    return numpy.array(fields[ndim + 1:], dtype=dtype).reshape(dims)


class Scan(object):
    """
    Represents a single subscan as part of a SDM/BDF dataset.  Convenience
    interface to open the BDF, get useful metadata, etc.
    """

    def __init__(self, sdm, scanidx, subscanidx=1):
        """
        sdm is the SDM object.
        scanidx is the scan number.
        subscanidx is the subscan number.
        """
        self.sdm = sdm
        self.idx = str(scanidx)
        self.subidx = str(subscanidx)
        self._bdf = None
        self.__main = None
        self.__scan = None
        self.__subscan = None
        return

    @property
    def bdf(self):
        if self._bdf is None:
            self._bdf = BDF(self.bdf_fname)
        return self._bdf

    @property
    def _main(self):
        """Convenience interface to the SDM Main table row."""
        if self.__main is None:
            self.__main = self.sdm[b'Main'][(self.idx, self.subidx)]
        return self.__main

    @property
    def _scan(self):
        """Convenience interface to the SDM Scan table row."""
        if self.__scan is None:
            self.__scan = self.sdm[b'Scan'][self.idx]
        return self.__scan

    @property
    def _subscan(self):
        """Convenience interface to the SDM Subscan table row."""
        if self.__subscan is None:
            self.__subscan = self.sdm[b'Subscan'][(self.idx, self.subidx)]
        return self.__subscan

    @property
    def _config(self):
        """Convenience interfact to the SDM ConfigDescription row."""
        return self.sdm[b'ConfigDescription'][self._main.configDescriptionId]

    @property
    def bdfdir(self):
        if self.sdm.bdfdir:
            return self.sdm.bdfdir
        return os.path.join(self.sdm.path, b'ASDMBinary')

    @property
    def bdf_fname(self):
        try:
            bdf_fname = os.path.join(self.bdfdir, uid2fname(self._main.dataUID.EntityRef.get(b'entityId')))
        except AttributeError:
            bdf_fname = os.path.join(self.bdfdir, uid2fname(self._main.dataOid.EntityRef.get(b'entityId')))

        return bdf_fname

    @property
    def source(self):
        """Source name as defined in SDM Scan table."""
        return self._scan.sourceName

    @property
    def field(self):
        """Field name as defined in SDM Subscan table."""
        return self._subscan.fieldName

    @property
    def coordinates(self):
        """
        Return the pointing coordinates (radians as given in Field table).
        """
        return sdmarray(self.sdm[b'Field'][self._main.fieldId].referenceDir, dtype=numpy.float)[0]

    @property
    def intents(self):
        """Return the list of intents for this scan."""
        return list(sdmarray(self._scan.scanIntent))

    @property
    def subintent(self):
        """Return the subscan intent."""
        return self._subscan.subscanIntent

    @property
    def antennas(self):
        """Return the list of antenna names for this scan."""
        sdm_ants = sdmarray(self._config.antennaId)
        return [ self.sdm[b'Antenna'][a].name for a in sdm_ants ]

    @property
    def stations(self):
        """Return the list of station names for this scan."""
        sdm_ants = sdmarray(self._config.antennaId)
        sdm_stns = [ self.sdm[b'Antenna'][a].stationId for a in sdm_ants ]
        return [ self.sdm[b'Station'][s].name for s in sdm_stns ]

    @property
    def positions(self):
        """
        Return the list of antenna posisitons (XYZ, m) for this scan.
        Result is an nant-by-3 array.
        """
        sdm_ants = sdmarray(self._config.antennaId)
        sdm_stns = [ self.sdm[b'Antenna'][a].stationId for a in sdm_ants ]
        return [ sdmarray(self.sdm[b'Station'][s].position, dtype=numpy.float) for s in sdm_stns
               ]

    @property
    def baselines(self):
        """
        Return the list of antenna pairs for this scan, in BDF ordering.
        """
        ants = self.antennas
        nant = len(ants)
        nbl = nant * (nant - 1) // 2
        return [ (ants[x[0]], ants[x[1]]) for x in map(bl2ant, list(range(nbl)))
               ]

    @property
    def startMJD(self):
        return float(self._subscan.startTime / 86400000000000.0)

    @property
    def endMJD(self):
        return float(self._subscan.endTime / 86400000000000.0)

    @property
    def numIntegration(self):
        """Number of integrations as listed in the SDM Main table."""
        return int(self._main.numIntegration)

    @property
    def spws(self):
        """ Return the list of spw names """
        return [ self.sdm[b'DataDescription'][dd_id].spectralWindowId for dd_id in sdmarray(self._config.dataDescriptionId)
               ]

    @property
    def reffreqs(self):
        """ List of reference frequencies. One per spw in spws list. """
        return [ float(self.spw(spwn).refFreq) for spwn in range(len(self.spws))
               ]

    @property
    def numchans(self):
        """ List of number of channels per spw. One per spw in spws list. """
        return [ int(self.spw(spwn).numChan) for spwn in range(len(self.spws)) ]

    @property
    def chanwidths(self):
        """ List of channel widths. One per spw in spws list. """
        return [ float(self.spw(spwn).chanWidth) for spwn in range(len(self.spws))
               ]

    @property
    def pulsar(self):
        """ Pulsar row entry, if one exists, otherwise None. """
        try:
            dd_id = sdmarray(self._config.dataDescriptionId)[0]
            psr_id = self.sdm[b'DataDescription'][dd_id].pulsarId
            return self.sdm[b'Pulsar'][psr_id]
        except AttributeError:
            return

        return

    def times(self, src=b'bdf'):
        """Return array of midpoint times (MJD) for all integrations in this 
        scan.  If src=='sdm' these will be estimated from the information in
        the SDM Subscan table.  If src=='bdf' they will be read from the BDF.
        If precise times are needed, use the BDF values, but this requires
        reading the BDF which can be slow."""
        if src.lower() == b'sdm':
            t0 = self.startMJD
            ni = int(self._subscan.numIntegration)
            dt = (self.endMJD - self.startMJD) / ni
            return t0 + (numpy.arange(ni) + 0.5) * dt
        if src.lower() == b'bdf':
            return numpy.array([ i.time for i in self.bdf ])
        raise ValueError(b'Unknown data source: ' + str(src))

    def freqs(self, spwidx=b'all'):
        """ Array of per-channel frequences for the given spectral window.
        If spwidx=='all', a nspw-by-nchan array will be returned giving all
        frequencies, if all spectral window have the same number of channels.
        """
        nspw = len(self.spws)
        rf = self.reffreqs
        nc = self.numchans
        cw = self.chanwidths
        if spwidx == b'all':
            if nc.count(nc[0]) != len(nc):
                raise RuntimeError(b'Variable number of channels')
            nc = nc[0]
            out = numpy.zeros((nspw, nc))
            for i in range(nspw):
                out[i, :] = numpy.arange(nc) * cw[i] + rf[i]

        else:
            out = numpy.arange(nc[spwidx]) * cw[spwidx] + rf[spwidx]
        return out

    def tcal(self, spwidx=b'all'):
        """ Array of Tcal values from CalDevice table."""
        sdm_ants = sdmarray(self._config.antennaId)
        nspw = len(self.spws)
        nant = len(sdm_ants)
        if spwidx == b'all':
            out = numpy.zeros((nant, nspw, 2))
            for iant in range(nant):
                for ispw in range(nspw):
                    tmp = self.sdm[b'CalDevice'][(sdm_ants[iant],
                     self.spws[ispw])].coupledNoiseCal
                    out[iant, ispw, :] = sdmarray(tmp, dtype=numpy.float)[:, 0]

        else:
            raise NotImplementedError(b'Single spw not implemented yet')
        return out

    def spw(self, idx):
        """Return the SpectralWindow entry for the given index in this scan."""
        dd_id = sdmarray(self._config.dataDescriptionId)[idx]
        spw_id = self.sdm[b'DataDescription'][dd_id].spectralWindowId
        return self.sdm[b'SpectralWindow'][spw_id]

    def flags(self, mjd, axis=b'bl', pad=False, flagval=0, expand=1.0):
        """
        Return flag array for the given time(s).  Input mjd can be scalar
        or array valued.  If axis=='ant', returned array will have dimensions
        (N_times, N_antenna), otherwise (N_times, N_baselines).  Flag array
        contains 1 for non-flagged points and flagval for flagged data.  If pad
        arg is true, four extra len-1 dimensions will be appended so that
        flags can be applied to standard bdf.get_data() results.  All
        flag start/stop times are increased by the value of the expand
        argument (seconds).
        """
        sdm_ants = self.antennas
        nant = len(sdm_ants)
        nbl = nant * (nant - 1) // 2
        t_ns = numpy.array(numpy.array(mjd) * 86400000000000.0, dtype=numpy.int64)
        exp_ns = int(expand * 1000000000.0)
        d_out = t_ns.shape
        isscalar = d_out == ()
        if axis == b'ant':
            d_out += (nant,)
        else:
            d_out += (nbl,)
        if pad:
            d_out += (1, 1, 1, 1)
        out = numpy.ones(d_out, dtype=type(flagval))
        for flag in self.sdm[b'Flag']:
            tidx = numpy.where((t_ns > int(flag.startTime) - exp_ns) * (t_ns < int(flag.endTime) + exp_ns))[0]
            if len(tidx) == 0:
                continue
            for a in sdmarray(flag.antennaId):
                flagant = self.sdm[b'Antenna'][a].name
                if flagant not in sdm_ants:
                    continue
                if axis == b'ant':
                    flagidx = [
                     sdm_ants.index(flagant)]
                else:
                    flagidx = numpy.where([ flagant in pair for pair in self.baselines
                                          ])[0]
                if isscalar:
                    out[flagidx] = flagval
                else:
                    for ii in flagidx:
                        out[(tidx, ii)] = flagval

        return out