# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/dasscripts/tdms.py
# Compiled at: 2020-04-11 05:01:12
# Size of source mod 2**32: 28610 bytes
import logging, datetime, os, struct
from obspy import UTCDateTime
import numpy as np
from math import floor
from math import ceil

class TDMS(object):

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._TDMS__fi is not None:
            self._TDMS__fi.close()

    def __init__(self, filename, directory='.', chstart=0, chstop=None, chstep=1, starttime=None, endtime=None, iterate='D', decimate=1, firfilter='fir235', loglevel='INFO'):
        logs = logging.getLogger('Init TDMS')
        logs.setLevel(loglevel)
        PROJECT_DIR = os.path.dirname(__file__)
        self._TDMS__decimate = decimate
        self._TDMS__loglevel = loglevel
        self._TDMS__chstart = chstart
        self._TDMS__chstop = chstop
        self._TDMS__chstep = chstep
        self._TDMS__twstart = starttime
        self._TDMS__twend = endtime
        self.starttime = None
        self.endtime = None
        self.sampling_rate = None
        self._TDMS__currentfile = None
        self._TDMS__filename = filename
        self._TDMS__directory = directory
        self._TDMS__available = list()
        for file in sorted(os.listdir(directory)):
            if not file.startswith(filename):
                pass
            else:
                dt = datetime.datetime.strptime(file[len(filename):-len('.tdms')], '_%Z_%Y%m%d_%H%M%S.%f')
                self._TDMS__available.append({'dt':dt,  'name':file,  'samples':None})
                if self._TDMS__twstart is None:
                    self._TDMS__twstart = dt

        if self._TDMS__twstart < self._TDMS__available[0]['dt']:
            self._TDMS__twstart = self._TDMS__available[0]['dt']
        self._TDMS__origstarttime = self._TDMS__twstart
        self._TDMS__origendtime = self._TDMS__twend
        self.iterate = iterate
        self._TDMS__buffer = dict()
        self._TDMS__datatypes = dict()
        self.metadata = dict()
        self._TDMS__HEADERLEN = 28
        self._TDMS__MAXSAMPLES = 30000
        self._TDMS__FF64b = 18446744073709551615
        self._TDMS__FF32b = 4294967295
        self._TDMS__data2mask = {0:('c', 1), 
         1:('b', 1), 
         2:('h', 2), 
         3:('i', 4), 
         4:('q', 8), 
         5:('b', 1), 
         6:('h', 2), 
         7:('i', 4), 
         8:('q', 8), 
         9:('f', 4), 
         10:('d', 8), 
         32:('I', 4), 
         33:('?', 1), 
         68:('Qq', 16)}
        auxfilter = list()
        with open(os.path.join(PROJECT_DIR, 'data/filters/%s.txt' % firfilter)) as (fin):
            for line in fin.readlines():
                auxfilter.append(float(line))

        self._TDMS__filter = np.array(auxfilter)
        logs.debug('FIR filter: %s' % self._TDMS__filter)

    def __select_file(self):
        logs = logging.getLogger('Select file')
        logs.setLevel(self._TDMS__loglevel)
        if self._TDMS__currentfile is None:
            for idx, fi in enumerate(self._TDMS__available):
                if self._TDMS__twstart < fi['dt']:
                    if not idx:
                        raise Exception('Data not available in the specified time window')
                    filename = os.path.join(self._TDMS__directory, self._TDMS__available[(idx - 1)]['name'])
                    self._TDMS__currentfile = idx - 1
                    break
            else:
                raise Exception('Data not available in the specified time window')

        else:
            if self._TDMS__currentfile >= len(self._TDMS__available):
                logs.debug('Last file already processed')
                raise IndexError
            else:
                filename = os.path.join(self._TDMS__directory, self._TDMS__available[self._TDMS__currentfile]['name'])
                self._TDMS__twstart = self._TDMS__available[self._TDMS__currentfile]['dt']
                if self._TDMS__twend is not None and self._TDMS__twstart > self._TDMS__twend:
                    logs.debug('Start is greater than end. %s %s' % (self._TDMS__twstart, self._TDMS__twend))
                    raise IndexError
                logs.debug('Opening %s; Startime: %s' % (self._TDMS__available[self._TDMS__currentfile]['name'], self._TDMS__twstart))
        self.starttime = self._TDMS__available[self._TDMS__currentfile]['dt']
        self.endtime = None
        self.metadata = dict()
        self._TDMS__fi = open(filename, 'rb')
        leadin = self._TDMS__fi.read(self._TDMS__HEADERLEN)
        tag, ToCmask = struct.unpack('<4si', leadin[:8])
        kTocMetaData = 2
        kTocNewObjList = 4
        kTocRawData = 8
        kTocInterleavedData = 32
        kTocBigEndian = 64
        kTocDAQmxRawData = 128
        self.hasmetadata = bool(ToCmask & kTocMetaData)
        self.hasnewObjects = bool(ToCmask & kTocNewObjList)
        self.hasrawData = bool(ToCmask & kTocRawData)
        self.hasInterleavedData = bool(ToCmask & kTocInterleavedData)
        self.hasDAQmxRawData = bool(ToCmask & kTocDAQmxRawData)
        self._TDMS__endian = '>' if ToCmask & kTocBigEndian else '<'
        if tag.decode() != 'TDSm':
            raise Exception('Tag is not TDSm!')
        versionTDMS, self._TDMS__segmentOffset, self._TDMS__dataOffset = struct.unpack('%ciQQ' % self._TDMS__endian, leadin[8:])
        logs.debug((tag, ToCmask, versionTDMS, self._TDMS__segmentOffset, self._TDMS__dataOffset))
        if versionTDMS != 4713:
            logs.warning('Version number is not 4713!')
        if self._TDMS__segmentOffset == self._TDMS__FF64b:
            logs.error('Severe problem while writing data (crash, power outage)')
        if self.hasmetadata:
            if not self._TDMS__dataOffset:
                logs.error('Flag indicates Metadata but its length is 0!')
        if self.hasDAQmxRawData:
            logs.warning('DAQmx raw data is still not supported!')
        self._TDMS__segmentOffset += self._TDMS__HEADERLEN
        self._TDMS__dataOffset += self._TDMS__HEADERLEN
        logs.debug('Metadata: ' + ('yes' if self.hasmetadata else 'no'))
        logs.debug('Object list: ' + ('yes' if self.hasnewObjects else 'no'))
        logs.debug('Raw data: ' + ('yes' if self.hasrawData else 'no'))
        logs.debug('Interleaved data: ' + ('yes' if self.hasInterleavedData else 'no'))
        logs.debug('BigEndian: ' + ('yes' if self._TDMS__endian == '<' else 'no'))
        logs.debug('DAQmx raw data: ' + ('yes' if self.hasDAQmxRawData else 'no'))
        self.readMetadata()

    def resetcurrenttime(self):
        self._TDMS__twstart = self._TDMS__origstarttime
        self._TDMS__twend = self._TDMS__origendtime
        self._TDMS__currentfile = None
        self._TDMS__select_file()

    def __enter__(self):
        self._TDMS__select_file()
        for channel in range(self._TDMS__chstart, self._TDMS__chstop + 1, self._TDMS__chstep):
            logging.debug('Create empty buffers')
            self._TDMS__buffer[channel] = None

        return self

    def readMetadata(self):
        logs = logging.getLogger('Read Metadata')
        self._TDMS__fi.seek(self._TDMS__HEADERLEN, 0)
        numObjects = struct.unpack('%cI' % self._TDMS__endian, self._TDMS__fi.read(4))[0]
        logs.debug('Number of objects in metadata: %s' % numObjects)
        numChannels = 0
        for obj in range(numObjects):
            objPath = self._TDMS__readstring()
            self.metadata[obj] = {'path': objPath}
            rawDataIdx = struct.unpack('%cI' % self._TDMS__endian, self._TDMS__fi.read(4))[0]
            if rawDataIdx == self._TDMS__FF32b:
                logs.debug('No raw data assigned to this segment')
                self.metadata[obj]['data'] = False
                self._TDMS__readproperties(self.metadata[obj])
                try:
                    if self.sampling_rate is None:
                        self.sampling_rate = self.metadata[obj]['SamplingFrequency[Hz]']
                except:
                    pass

                try:
                    if self.starttime is None:
                        self.starttime = self.metadata[obj]['GPSTimeStamp']
                except:
                    pass

                continue
            elif not rawDataIdx:
                logs.debug('Raw data index in this segment matches the index the same object had in the previous segment')
            else:
                self.metadata[obj]['data'] = True
                numChannels += 1
                sizeBytes = None
                datatype, arraylen, numValues = struct.unpack('%cIIQ' % self._TDMS__endian, self._TDMS__fi.read(16))
                if datatype == 32:
                    self.metadata[obj]['sizeBytes'] = struct.unpack('%cQ' % self._TDMS__endian, self._TDMS__fi.read(8))[0]
                if arraylen != 1:
                    logs.error('Array length MUST be 1! Actual value: %s' % arraylen)
                self.metadata[obj]['datatype'] = self._TDMS__data2mask[datatype][0]
                self._TDMS__readproperties(self.metadata[obj])

        if self._TDMS__data2mask[datatype][0] == 'h':
            self.datatype = '%ci2' % self._TDMS__endian
        else:
            if self._TDMS__data2mask[datatype][0] == 'f':
                self.datatype = '%cf4' % self._TDMS__endian
            else:
                raise Exception('Data type not supported! (%s)' % self._TDMS__data2mask[datatype][0])
            self.datatypesize = self._TDMS__data2mask[datatype][1]
            self.numChannels = numChannels
            self.samples = int((self._TDMS__segmentOffset - self._TDMS__dataOffset) / numChannels / self.datatypesize)
            self.endtime = self.starttime + datetime.timedelta(seconds=((self.samples - 1) / self.sampling_rate))
            self._TDMS__samplestart = max(floor((self._TDMS__twstart - self.starttime).total_seconds() * self.sampling_rate), 0)
            self._TDMS__twstart = self.starttime + datetime.timedelta(seconds=(self._TDMS__samplestart / self.sampling_rate))
            self._TDMS__samplecur = self._TDMS__samplestart
            if self._TDMS__twend is None or self._TDMS__twend >= self.endtime:
                self._TDMS__sampleend = self.samples - 1
            else:
                self._TDMS__sampleend = ceil((self._TDMS__twend - self.starttime).total_seconds() * self.sampling_rate)
            logs.debug('Samples: %s' % self.samples)
            logs.debug('Samples selected: %s-%s' % (self._TDMS__samplestart, self._TDMS__sampleend))
            logs.debug('Total chunks size: %s' % (self._TDMS__segmentOffset - self._TDMS__dataOffset))
            logs.debug('Length of channel: %d' % ((self._TDMS__segmentOffset - self._TDMS__dataOffset) / numChannels / self._TDMS__data2mask[datatype][1]))
            if self._TDMS__chstart >= numChannels:
                logs.error('Cannot export from channel %s. Only %s channels present.' % (self._TDMS__chstart, numChannels))
                raise IndexError
            if self._TDMS__chstop is None:
                self._TDMS__chstop = numChannels - 1
            elif self._TDMS__chstop >= numChannels:
                logs.warning('Resetting chstart to %s' % (numChannels - 1))
                self._TDMS__chstop = numChannels - 1
        newObjects = struct.unpack('%cI' % self._TDMS__endian, self._TDMS__fi.read(4))[0]

    def __iter__(self):
        """Iterate through data (or metadata) and filter and decimate if requested"""
        logs = logging.getLogger('__iter__')
        if self.iterate == 'M':
            for info in self.__iter_metadata__():
                yield info

        else:
            if self._TDMS__decimate == 1:
                for info in self.__iter_data__():
                    yield info

            else:
                inbuf = dict()
                outbuf = dict()
                nodecimation = dict()
                expectedtime = dict()
                startofchunk = True
                for data, stats in self.__iter_data__():
                    ch = int(stats['station'])
                    if ch in expectedtime:
                        if expectedtime[ch] != stats['starttime']:
                            logs.warning('GAP! Expected: %s ; Current: %s' % (expectedtime[ch], stats['starttime']))
                            if ch in inbuf:
                                logs.debug('Remove last %s components of previous chunk' % len(inbuf[ch]['data']))
                                del inbuf[ch]
                            if ch in outbuf:
                                leftover = len(nodecimation[ch]) % 5
                                outbuf[ch]['stats']['npts'] = 1
                                yield (nodecimation[ch][-leftover::5], outbuf[ch]['stats'])
                                logs.debug('Flushing: %s %s' % (nodecimation[ch][-leftover::5], outbuf[ch]['stats']))
                                del outbuf[ch]
                            del expectedtime[ch]
                            startofchunk = True
                    expectedtime[ch] = stats['starttime'] + stats['npts'] / self.sampling_rate
                    if ch not in inbuf:
                        inbuf[ch] = {'data':np.array(data),  'stats':stats}
                    else:
                        inbuf[ch]['data'] = np.append(inbuf[ch]['data'], data)
                    if ch not in outbuf:
                        outbuf[ch] = {'stats': inbuf[ch]['stats'].copy()}
                        if startofchunk:
                            outbuf[ch]['stats']['starttime'] += (len(self._TDMS__filter) - 1) / (2 * outbuf[ch]['stats']['sampling_rate'])
                            startofchunk = False
                        outbuf[ch]['stats']['sampling_rate'] = stats['sampling_rate'] / 5
                    if len(inbuf[ch]['data']) < len(self._TDMS__filter):
                        pass
                    else:
                        nodecimation[ch] = np.convolve(inbuf[ch]['data'], self._TDMS__filter, 'valid').astype(data.dtype)
                        logs.debug('filtered: %d components' % len(nodecimation[ch]))
                        logs.debug('filtered[%d][:11] %s' % (ch, nodecimation[ch][:11]))
                        logs.debug('filtered[%d][-11:] %s' % (ch, nodecimation[ch][-11:]))
                        leftover = len(nodecimation[ch]) % 5
                        logs.debug('filtered: leave %d components for next iteration %s' % (leftover, nodecimation[ch][-leftover:]))
                    if leftover:
                        if 'data' not in outbuf[ch]:
                            outbuf[ch]['data'] = nodecimation[ch][:-leftover][::5]
                        else:
                            outbuf[ch]['data'] = np.append(outbuf[ch]['data'], nodecimation[ch][:-leftover][::5])
                    else:
                        if 'data' not in outbuf[ch]:
                            outbuf[ch]['data'] = nodecimation[ch][::5]
                        else:
                            outbuf[ch]['data'] = np.append(outbuf[ch]['data'], nodecimation[ch][::5])
                        logs.debug('outbuf[%d][:11] %s' % (ch, outbuf[ch]['data'][:11]))
                        logs.debug('outbuf[%d][-11:] %s' % (ch, outbuf[ch]['data'][-11:]))
                        valuesprocessed = len(inbuf[ch]['data']) - len(self._TDMS__filter) + 1 - leftover
                        logs.debug('values processed: %d' % valuesprocessed)
                        inbuf[ch]['data'] = inbuf[ch]['data'][-len(self._TDMS__filter) + 1 - leftover:]
                        inbuf[ch]['stats']['starttime'] += valuesprocessed / inbuf[ch]['stats']['sampling_rate']
                        if len(outbuf[ch]['data']) > 2000:
                            outbuf[ch]['stats']['npts'] = len(outbuf[ch]['data'])
                            yield (
                             outbuf[ch]['data'], outbuf[ch]['stats'])
                            outbuf[ch]['stats']['starttime'] += len(outbuf[ch]['data']) / outbuf[ch]['stats']['sampling_rate']
                            del outbuf[ch]['data']

                for ch in outbuf:
                    if 'data' in outbuf[ch] and len(outbuf[ch]['data']):
                        outbuf[ch]['stats']['npts'] = len(outbuf[ch]['data'])
                        yield (outbuf[ch]['data'], outbuf[ch]['stats'])

    def __iter_data__(self):
        """Read data from files based on channel selection"""
        logs = logging.getLogger('Iterate Data')
        if not self.hasInterleavedData:
            for ch in range(self._TDMS__chstart, self._TDMS__chstop + 1, self._TDMS__chstep):
                self.resetcurrenttime()
                while self._TDMS__twend is None or self._TDMS__twstart < self._TDMS__twend:
                    while self._TDMS__samplecur <= self._TDMS__sampleend:
                        data = self._TDMS__readdata(channels=[ch])
                        stats = {'network':'XX',  'station':'%05d' % ch,  'location':'',  'channel':'FH1', 
                         'npts':len(data[ch]),  'sampling_rate':self.sampling_rate, 
                         'starttime':UTCDateTime(self._TDMS__twstart), 
                         'mseed':{'byteorder':self._TDMS__endian, 
                          'reclen':512}}
                        logs.debug('Data length: %d; First component: %s' % (len(data[ch]), data[ch][0]))
                        yield (data[ch], stats)
                        self._TDMS__samplecur += len(data[ch])

                    self._TDMS__currentfile += 1
                    try:
                        self._TDMS__select_file()
                    except IndexError:
                        break

        else:
            channels = list(range(self._TDMS__chstart, self._TDMS__chstop + 1, self._TDMS__chstep))
            while self._TDMS__twend is None or self._TDMS__twstart < self._TDMS__twend:
                while self._TDMS__samplecur <= self._TDMS__sampleend:
                    data = self._TDMS__readdata(channels=channels)
                    for ch in channels:
                        stats = {'network':'XX', 
                         'station':'%05d' % ch,  'location':'',  'channel':'FH1', 
                         'npts':len(data[ch]),  'sampling_rate':self.sampling_rate, 
                         'starttime':UTCDateTime(self._TDMS__twstart), 
                         'mseed':{'byteorder':self._TDMS__endian, 
                          'reclen':512}}
                        logs.debug('Data length: %d; First component: %s' % (len(data[ch]), data[ch][0]))
                        yield (data[ch], stats)

                    self._TDMS__samplecur += len(data[channels[0]])

                self._TDMS__currentfile += 1
                try:
                    logs.debug('Moving to next file...')
                    self._TDMS__select_file()
                except IndexError:
                    break

    def __iter_metadata__(self):
        while self._TDMS__twend is None or self._TDMS__twstart < self._TDMS__twend:
            for ch in self.metadata:
                yield self.metadata[ch]

            self._TDMS__currentfile += 1
            try:
                self._TDMS__select_file()
            except IndexError:
                break

    def __readstring(self):
        strlen = struct.unpack('%cI' % self._TDMS__endian, self._TDMS__fi.read(4))
        return self._TDMS__fi.read(strlen[0]).decode()

    def __readvalue(self):
        logs = logging.getLogger('readvalue')
        datatype = self._TDMS__readdatatype()
        if datatype == 32:
            return self._TDMS__readstring()
        else:
            mask, numBytes = self._TDMS__data2mask[datatype]
            result = struct.unpack('%c%s' % (self._TDMS__endian, mask), self._TDMS__fi.read(numBytes))
            if datatype == 68:
                result = (self._TDMS__tup2time)(*result)
            else:
                result = result[0]
            return result

    def __readproperties(self, result=dict()):
        logs = logging.getLogger('readproperties')
        numProps = struct.unpack('%cI' % self._TDMS__endian, self._TDMS__fi.read(4))[0]
        if numProps:
            logs.debug('%s properties' % numProps)
        for prop in range(numProps):
            propStr = self._TDMS__readstring()
            value = self._TDMS__readvalue()
            result[propStr] = value
            if self.iterate == 'M':
                logs.debug('%s: %s' % (propStr, value))

        return result

    def __readdatatype(self):
        return struct.unpack('%cI' % self._TDMS__endian, self._TDMS__fi.read(4))[0]

    def __tup2time(self, fraction, seconds):
        logs = logging.getLogger('tup2time')
        dt1904 = datetime.datetime(1904, 1, 1)
        delta = seconds + fraction * 5.421010862427522e-20
        result = dt1904 + datetime.timedelta(seconds=delta)
        return result

    def __readdata(self, channels=[
 0]):
        """Read a chunk of data from the specified channels

        :param channels: List of channel numbers to read data from
        :type channels: list
        :return: Dictionary with channel as key and a numpy array with data as value
        :rtype: dict
        """
        result = dict()
        numSamples = self._TDMS__sampleend - self._TDMS__samplestart + 1
        if not self.hasInterleavedData:
            for ch in channels:
                self._TDMS__fi.seek(self._TDMS__dataOffset + self.datatypesize * self.samples * ch + self._TDMS__samplecur, 0)
                result[ch] = np.fromfile((self._TDMS__fi), dtype=(self.datatype), count=numSamples)

            return result
        else:
            self._TDMS__fi.seek(self._TDMS__dataOffset + self._TDMS__samplecur * self.datatypesize * self.numChannels, 0)
            for ch in channels:
                result[ch] = np.zeros((numSamples,), dtype=(self.datatype))

            for sample in range(numSamples):
                allchannels = np.fromfile((self._TDMS__fi), dtype=(self.datatype), count=(self.numChannels))
                for ch in channels:
                    result[ch][sample] = allchannels[ch]

            return result