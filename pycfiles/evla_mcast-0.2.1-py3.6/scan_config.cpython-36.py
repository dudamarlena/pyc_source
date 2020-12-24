# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/evla_mcast/scan_config.py
# Compiled at: 2018-02-26 13:34:18
# Size of source mod 2**32: 17659 bytes
from __future__ import print_function, division, absolute_import, unicode_literals
from builtins import bytes, dict, object, range, map, input, str
from future.utils import itervalues, viewitems, iteritems, listvalues, listitems
from io import open
import ast
from lxml import objectify
import os.path
from . import angles
from .mcast_clients import _ant_parser, _vci_parser, _obs_parser
import logging
logger = logging.getLogger(__name__)

class ScanConfig(object):
    __doc__ = ' This class defines a complete EVLA observing config,\n    which in practice means both a VCI document and OBS document have been\n    received.  Quantities relevant for pulsar processing are taken\n    from the VCI and OBS and returned.'

    def __init__(self, vci=None, obs=None, ant=None, requires=[
 'obs', 'vci', 'ant', 'stop']):
        """ Sets the documents for a given scan.
        vci, obs, and ant arguments accept filenames or parsed xml string.

        The requires arguments is a list specifying which information is
        required for the ScanConfig to be complete.  It can contain any
        of 'obs', 'vci', 'ant' and 'stop'.  The default is for all
        four to be required.  When all requirements have been filled,
        ScanConfig.is_complete() will return True.
        """
        try:
            if len(obs):
                logger.debug('Received obs doc')
                with open(obs, 'rb') as (fobs):
                    obs = objectify.fromstring((fobs.read()), parser=_obs_parser)
                logger.info('Added obs doc from file {0}'.format(obs))
            else:
                if len(vci):
                    logger.debug('Received vci doc')
                    with open(vci, 'rb') as (fvci):
                        vci = objectify.fromstring((fvci.read()), parser=_vci_parser)
                    logger.info('Added vci doc from file {0}'.format(obs))
                if len(ant):
                    logger.debug('Received ant doc')
                    with open(ant, 'rb') as (fant):
                        ant = objectify.fromstring((fant.read()), parser=_ant_parser)
                    logger.info('Added ant doc from file {0}'.format(ant))
        except (IOError, TypeError):
            logger.debug('Assuming one or more doc was already parsed')

        self.stopTime = None
        self.requires = requires
        self.set_vci(vci)
        self.set_obs(obs)
        self.set_ant(ant)

    def __repr__(self):
        defined = []
        if self.has_obs:
            defined.append('obs')
        if self.has_ant:
            defined.append('ant')
        if self.has_vci:
            defined.append('vci')
        if self.stopTime:
            defined.append('stop')
        return 'ScanConfig with {0} defined'.format(defined)

    @property
    def has_vci(self):
        return self.vci is not None

    @property
    def has_obs(self):
        return self.obs is not None

    @property
    def has_ant(self):
        return self.ant is not None

    def is_complete(self):
        if 'obs' in self.requires:
            if not self.has_obs:
                return False
            else:
                if 'vci' in self.requires:
                    if not self.has_obs:
                        return False
                if 'ant' in self.requires:
                    if not self.has_ant:
                        return False
        else:
            if 'stop' in self.requires:
                if self.stopTime is None:
                    return False
        return True

    def set_vci(self, vci):
        self.vci = vci

    def set_obs(self, obs):
        self.obs = obs
        if self.obs is None:
            self.intents = {}
        else:
            self.intents = self.parse_intents(obs.intent)

    def set_ant(self, ant):
        self.ant = ant

    @staticmethod
    def parse_intents(intents):
        d = {}
        for item in intents:
            k, v = str(item).split('=')
            if v[0] is "'" or v[0] is '"':
                d[k] = ast.literal_eval(v)
            else:
                d[k] = v

        return d

    def get_intent(self, key, default=None):
        try:
            return self.intents[key]
        except KeyError:
            return default

    @property
    def configId(self):
        return self.obs.attrib['configId']

    @property
    def datasetId(self):
        return self.obs.attrib['datasetId']

    @property
    def scanId(self):
        return '%s.%d.%d' % (self.datasetId, self.scanNo, self.subscanNo)

    @property
    def scanNo(self):
        return int(self.obs.scanNo)

    @property
    def subscanNo(self):
        return int(self.obs.subscanNo)

    @property
    def observer(self):
        return self.get_intent('ObserverName', 'Unknown')

    @property
    def projid(self):
        return self.get_intent('ProjectID', 'Unknown')

    @property
    def scan_intent(self):
        return self.get_intent('ScanIntent', 'None')

    @property
    def nchan(self):
        return int(self.get_intent('PsrNumChan', 32))

    @property
    def npol(self):
        return int(self.get_intent('PsrNumPol', 4))

    @property
    def foldtime(self):
        return float(self.get_intent('PsrFoldIntTime', 10.0))

    @property
    def foldbins(self):
        return int(self.get_intent('PsrFoldNumBins', 2048))

    @property
    def timeres(self):
        return float(self.get_intent('PsrSearchTimeRes', 0.001))

    @property
    def nbitsout(self):
        return int(self.get_intent('PsrSearchNumBits', 8))

    @property
    def searchdm(self):
        return float(self.get_intent('PsrSearchDM', 0.0))

    @property
    def freqfac(self):
        return float(self.get_intent('PsrSearchFreqFac', 1))

    @property
    def parfile(self):
        return self.get_intent('TempoFileName', None)

    @property
    def calfreq(self):
        return float(self.get_intent('PsrCalFreq', 10.0))

    @property
    def raw_format(self):
        return self.get_intent('PsrRawFormat', 'GUPPI')

    @property
    def source(self):
        return str(self.obs.name)

    @property
    def ra_deg(self):
        return angles.r2d(self.obs.ra)

    @property
    def ra_hrs(self):
        return angles.r2h(self.obs.ra)

    @property
    def ra_str(self):
        return angles.fmt_angle(self.ra_hrs, ':', ':').lstrip('+-')

    @property
    def dec_deg(self):
        return angles.r2d(self.obs.dec)

    @property
    def dec_str(self):
        return angles.fmt_angle(self.dec_deg, ':', ':')

    @property
    def startLST(self):
        return self.obs.startLST * 86400.0

    @property
    def startTime(self):
        try:
            return float(self.obs.attrib['startTime'])
        except AttributeError:
            return 0.0

    @property
    def seq(self):
        return self.obs.attrib['seq']

    @property
    def telescope(self):
        return 'VLA'

    @property
    def binningPeriod(self):
        bp = {}
        for baseBand in self.vci.stationInputOutput[0].baseBand:
            try:
                if baseBand.binningPeriod is not None:
                    IFid = swbbName_to_IFid(baseBand.swbbName)
                    bp[IFid] = baseBand.binningPeriod
            except AttributeError:
                pass

        return bp

    @property
    def numBins(self):
        nb = {}
        for baseBand in self.vci.stationInputOutput[0].baseBand:
            try:
                if baseBand.phaseBinning[0].numBins is not None:
                    IFid = self.swbbName_to_IFid(baseBand.swbbName)
                    nb[IFid] = baseBand.phaseBinning[0].numBins
            except (AttributeError, IndexError):
                pass

        return nb

    @property
    def listOfStations(self):
        return [str(s.attrib['name']) for s in self.vci.listOfStations.station]

    @property
    def numAntenna(self):
        return len(self.listOfStations)

    def get_sslo(self, IFid):
        """Return the SSLO frequency in MHz for the given IFid.  This will
        correspond to the edge of the baseband.  Uses IFid naming convention
        as in OBS XML."""
        for sslo in self.obs.sslo:
            if sslo.attrib['IFid'] == IFid:
                return sslo.freq

    def get_sideband(self, IFid):
        """Return the sideband sense (int; +1 or -1) for the given IFid.
        Uses IFid naming convention as in OBS XML."""
        for sslo in self.obs.sslo:
            if sslo.attrib['IFid'] == IFid:
                return int(sslo.attrib['Sideband'])

    def get_receiver(self, IFid):
        """Return the receiver name for the given IFid.
        Uses IFid naming convention as in OBS XML."""
        for sslo in self.obs.sslo:
            if sslo.attrib['IFid'] == IFid:
                return sslo.attrib['Receiver']

    @staticmethod
    def swbbName_to_IFid(swbbName):
        """Converts values found in the VCI baseBand.swbbName property to
        matching values as used in the OBS sslo.IFid property.

        swbbNames are like AC_8BIT, A1C1_3BIT, etc.
        IFids are like AC, AC1, etc."""
        conversions = {'A1C1':'AC1', 
         'A2C2':'AC2', 
         'B1D1':'BD1', 
         'B2D2':'BD2'}
        bbname, bits = swbbName.split('_')
        if bbname in conversions:
            return conversions[bbname]
        else:
            return bbname

    def get_subbands(self, only_vdif=False, match_ips=[]):
        """Return a list of SubBand objects for all matching subbands.
        Inputs:

          only_vdif: if True, return only subbands with VDIF output enabled.
                     (default: False)

          match_ips: Only return subbands with VDIF output routed to one of
                     the specified IP addresses.  If empty, all subbands
                     are returned.  non-empty match_ips implies only_vdif
                     always.
                     (default: [])
        """
        if not self.is_complete():
            raise RuntimeError('Complete configuration not available: has_vci={0}, has_obs={1}, has_ant={2}, stoptime={3}'.format(self.has_vci, self.has_obs, self.has_ant, self.stoptime))
        subs = []
        for baseBand in self.vci.stationInputOutput[0].baseBand:
            swbbName = str(baseBand.attrib['swbbName'])
            IFid = self.swbbName_to_IFid(swbbName)
            for subBand in baseBand.subBand:
                if len(match_ips) or only_vdif:
                    for summedArray in subBand.summedArray:
                        vdif = summedArray.vdif
                        if vdif:
                            if len(match_ips):
                                if vdif.aDestIP in match_ips or vdif.bDestIP in match_ips:
                                    subs += [SubBand(subBand, self, IFid, vdif)]
                            else:
                                subs += [SubBand(subBand, self, IFid, vdif)]

                else:
                    subs += [SubBand(subBand, self, IFid, vdif=None)]

        return subs

    def get_antennas(self):
        """Return a list of antenna objects for this scan.  These will
        appear in the correct order relevant to the ordering of data
        in the BDF."""
        ants = []
        for a in self.ant.AntennaProperties:
            if a.attrib['name'] in self.listOfStations:
                ants += [Antenna(a)]

        return sorted(ants, key=(lambda a: int(a.widarID)))


class SubBand(object):
    __doc__ = 'This class defines relevant info for real-time pulsar processing\n    of a single subband.  Most info is contained in the VCI subBand element,\n    some is copied out for convenience.  Also the corresponding sky frequency\n    is calculated, this depends on the baseBand properties, and LO settings\n    (the latter only available in the OBS XML document).  Note, all frequencies\n    coming out of this class are in MHz.\n\n    Inputs:\n        subBand: The VCI subBand element\n        config:  The original ScanConfig object\n        vdif:    The summedArray.vdif VCI element (optional)\n        IFid:    The IF identification (as in OBS xml)\n    '

    def __init__(self, subBand, config, IFid, vdif=None):
        self.IFid = IFid
        self.swIndex = int(subBand.attrib['swIndex'])
        self.sbid = int(subBand.attrib['sbid'])
        self.vdif = vdif
        self.bw = 1e-06 * float(subBand.attrib['bw'])
        self.bb_center_freq = 1e-06 * float(subBand.attrib['centralFreq'])
        self.sky_center_freq = config.get_sslo(IFid) + config.get_sideband(IFid) * self.bb_center_freq
        self.receiver = config.get_receiver(IFid)
        npp = len(subBand.polProducts.pp)
        self.pp = [None] * npp
        for pp in subBand.polProducts.pp:
            idx = int(pp.attrib['id']) - 1
            self.pp[idx] = str(pp.attrib['correlation'])

        self.spectralChannels = int(subBand.polProducts.pp[0].attrib['spectralChannels'])
        if IFid in list(config.binningPeriod.keys()):
            self.hw_time_res = 1e-06 * config.binningPeriod[IFid] * int(subBand.polProducts.blbProdIntegration.attrib['ltaIntegFactor'])
        else:
            self.hw_time_res = 1e-06 * float(subBand.polProducts.blbProdIntegration.attrib['minIntegTime']) * int(subBand.polProducts.blbProdIntegration.attrib['ccIntegFactor']) * int(subBand.polProducts.blbProdIntegration.attrib['ltaIntegFactor'])
        self.final_time_res = self.hw_time_res * int(subBand.polProducts.blbProdIntegration.attrib['cbeIntegFactor'])

    @property
    def npp(self):
        return len(self.pp)


class Antenna(object):
    __doc__ = 'Holds info about an antenna, as described in the Antenna Properties\n    Table.  Initialize with the AntennaProperties xml element.'

    def __init__(self, antprop):
        self.name = str(antprop.attrib['name'])
        self.widarID = int(antprop.widarID)
        self.pad = str(antprop.pad)
        self.X = float(antprop.X)
        self.Y = float(antprop.Y)
        self.Z = float(antprop.Z)
        self.offset = float(antprop.offset)

    @property
    def xyz(self):
        return [self.X, self.Y, self.Z]


if __name__ == '__main__':
    import sys, vcixml_parser, obsxml_parser
    vcifile = sys.argv[1]
    obsfile = sys.argv[2]
    print("Parsing vci='%s' obs='%s'" % (vcifile, obsfile))
    vci = vcixml_parser.parse(vcifile)
    obs = obsxml_parser.parse(obsfile)
    config = ScanConfig(vci=vci, obs=obs)
    print('Found these subbands:')
    for sub in config.get_subbands(only_vdif=False):
        print('  IFid=%s swindex=%d sbid=%d vdif=%s bw=%.1f freq=%.1f' % (
         sub.IFid, sub.swIndex, sub.sbid, sub.vdif is not None,
         sub.bw, sub.sky_center_freq))