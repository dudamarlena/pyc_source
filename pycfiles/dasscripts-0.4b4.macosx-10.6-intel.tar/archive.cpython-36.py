# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/dasscripts/archive.py
# Compiled at: 2020-04-18 15:17:19
# Size of source mod 2**32: 9946 bytes
import logging, os
from copy import copy
from datetime import timedelta
from obspy import UTCDateTime
from abc import ABCMeta
from abc import abstractmethod

class Archive(metaclass=ABCMeta):
    __doc__ = 'Base class for the different structures an archive can have'

    @abstractmethod
    def __init__(self, root, strictcheck):
        """Define the root directory where files should be archived and
        whether the archival process should strictly check a coherency in
        the order of the records.

        :param root: Directory where files should be archived
        :type root: str
        :param strictcheck: Flag declaring whether to check that this chunk can be appended in case of existing data
        :type strictcheck: bool
        """
        pass

    @abstractmethod
    def archive(self, trace):
        """Archive mseed

        :param trace: Trace to archive
        :type trace: obspy.Trace
        """
        pass


class StreamBasedHour(Archive):
    __doc__ = 'Class to archive miniSEED in 1-hour files per stream'

    def __init__(self, root='.', strictcheck=True):
        """Define the root directory where files should be archived and
        whether the archival process should strictly check a coherency in
        the order of the records.

        :param root: Directory where files should be archived
        :type root: str
        :param strictcheck: Flag declaring whether to check that this chunk can be appended in case of existing data
        :type strictcheck: bool
        """
        self._StreamBasedHour__root = root
        self._StreamBasedHour__strictcheck = strictcheck
        self._StreamBasedHour__add2files = set()

    def archive(self, trace):
        """Archive mseed

        :param trace: Trace to archive
        :type trace: obspy.Trace
        """
        logs = logging.getLogger('StreamBasedHour')
        net = trace.stats.network
        sta = trace.stats.station
        loc = trace.stats.location
        cha = trace.stats.channel
        nslc = '%s.%s.%s.%s' % (net, sta, loc, cha)
        logs.debug('Trace to archive:  %s' % trace)
        auxstart = copy(trace.stats.starttime)
        while auxstart < trace.stats.endtime:
            dir2check = os.path.join(self._StreamBasedHour__root, net, '%d' % auxstart.year, '%02d' % auxstart.month, '%02d' % auxstart.day)
            auxend = copy(auxstart)
            auxend.minute = 0
            auxend.second = 0
            auxend.microsecond = 0
            auxend = auxend + timedelta(hours=1)
            logs.debug('From %s to %s' % (auxstart, auxend))
            if not os.path.isdir(dir2check):
                os.makedirs(dir2check)
            filename = '%s.%d.%02d.%02d.%02d.00.00.mseed' % (nslc,
             auxstart.year,
             auxstart.month,
             auxstart.day,
             auxstart.hour)
            if filename in self._StreamBasedHour__add2files:
                mode = 'ab'
            else:
                mode = 'wb'
                self._StreamBasedHour__add2files.add(filename)
            with open(os.path.join(dir2check, filename), mode) as (fout):
                hourtrace = trace.slice(starttime=auxstart, endtime=auxend,
                  nearest_sample=False)
                hourtrace.write(fout, format='MSEED')
            auxstart = copy(auxend)


class StreamBased(Archive):
    __doc__ = 'Class to archive miniSEED in one file per stream'

    def __init__(self, root='.', strictcheck=True):
        """Define the root directory where files should be archived and
        whether the archival process should strictly check a coherency in
        the order of the records.

        :param root: Directory where files should be archived
        :type root: str
        :param strictcheck: Flag declaring whether to check that this chunk can be appended in case of existing data
        :type strictcheck: bool
        """
        self._StreamBased__root = root
        self._StreamBased__strictcheck = strictcheck
        self._StreamBased__add2files = set()

    def archive(self, trace):
        """Archive mseed

        :param trace: Trace to archive
        :type trace: obspy.Trace
        """
        nslc = '%s.%s.%s.%s' % (trace.stats.network, trace.stats.station,
         trace.stats.location, trace.stats.channel)
        filename = '%s.mseed' % nslc
        if filename in self._StreamBased__add2files:
            mode = 'ab'
        else:
            mode = 'wb'
            self._StreamBased__add2files.add(filename)
        with open(os.path.join(self._StreamBased__root, filename), mode) as (fout):
            if self._StreamBased__strictcheck:
                pass
            trace.write(fout, format='MSEED')


class SDS(Archive):
    __doc__ = 'Class to archive miniSEED in an SDS structure'

    def __init__(self, root='.', strictcheck=True):
        """Define the root directory of the SDS structure

        The structure is defined as
        <root>/YEAR/NET/STA/CHAN.TYPE/NET.STA.LOC.CHAN.TYPE.YEAR.DAY

        :param root: Root directory of the SDS structure
        :type root: str
        :param strictcheck: Flag to declare if the miniSEED chunk should always be parsed to check proper directory structure
        :type strictcheck: bool
        """
        self._SDS__root = root
        self._SDS__strictcheck = strictcheck
        self._SDS__add2files = set()
        if strictcheck:
            logging.warning('Strict Check was not implemented in SDS class')

    def archive(self, trace):
        """Archive mseed

        :param trace: Trace to archive
        :type trace: obspy.Trace
        """
        logs = logging.getLogger('SDS')
        nslc = '%s.%s.%s.%s' % (trace.stats.network, trace.stats.station,
         trace.stats.location, trace.stats.channel)
        logs.info('Archiving %s %s %s' % (nslc,
         trace.stats.starttime,
         trace.stats.endtime))
        try:
            n, s, l, c = nslc.split('.')
        except ValueError:
            if nslc.count('.') != 3:
                raise Exception('Wrong format in NSLC code: %s' % nslc)
            else:
                raise
        except Exception:
            raise

        for year in range(trace.stats.starttime.year, trace.stats.endtime.year + 1):
            dir2check = os.path.join(self._SDS__root, str(year), trace.stats.network, trace.stats.station, '%s.D' % c)
            if os.path.isdir(dir2check):
                continue
            else:
                os.makedirs(dir2check)

        auxstart = copy(trace.stats.starttime)
        while auxstart < trace.stats.endtime:
            dir2check = os.path.join(self._SDS__root, str(auxstart.year), trace.stats.network, trace.stats.station, '%s.D' % c)
            auxend = UTCDateTime(auxstart.date + timedelta(days=1))
            logs.debug('From %s to %s' % (UTCDateTime(auxstart.date), auxend))
            filename = '%s.D.%d.%03d' % (nslc,
             auxstart.year,
             auxstart.timetuple().tm_yday)
            if filename in self._SDS__add2files:
                mode = 'ab'
            else:
                mode = 'wb'
                self._SDS__add2files.add(filename)
            with open(os.path.join(dir2check, filename), mode) as (fout):
                daytrace = trace.slice(starttime=auxstart, endtime=auxend,
                  nearest_sample=False)
                daytrace.write(fout, format='MSEED')
            auxstart = copy(auxend)