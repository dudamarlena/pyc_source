# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/brukerimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 21523 bytes
"""Authors: Henning O. Sorensen & Erik Knudsen
         Center for Fundamental Research: Metal Structures in Four Dimensions
         Risoe National Laboratory
         Frederiksborgvej 399
         DK-4000 Roskilde
         email:erik.knudsen@risoe.dk

Based on: openbruker,readbruker, readbrukerheader functions in the opendata
         module of ImageD11 written by Jon Wright, ESRF, Grenoble, France

Writer by Jérôme Kieffer, ESRF, Grenoble, France

"""
from __future__ import absolute_import, print_function, with_statement, division
__authors__ = [
 'Henning O. Sorensen', 'Erik Knudsen', 'Jon Wright', 'Jérôme Kieffer']
__date__ = '04/03/2019'
__status__ = 'production'
__copyright__ = '2007-2009 Risoe National Laboratory; 2010-2015 ESRF'
__licence__ = 'MIT'
import logging, numpy
from math import ceil
import os, getpass, time
logger = logging.getLogger(__name__)
from .fabioimage import FabioImage
from .fabioutils import pad, StringTypes

class BrukerImage(FabioImage):
    __doc__ = '\n    Read and eventually write ID11 bruker (eg smart6500) images\n\n    TODO: int32 -> float32 conversion according to the "linear" keyword.\n    This is done and works but we need to check with other program that we\n    are appliing the right formula and not the reciprocal one.\n\n    '
    DESCRIPTION = 'File format used by Bruker detectors (version 86)'
    DEFAULT_EXTENSIONS = []
    bpp_to_numpy = {1: numpy.uint8, 
     2: numpy.uint16, 
     4: numpy.uint32}
    SPACER = '\x1a\x04'
    HEADERS_KEYS = ['FORMAT',
     'VERSION',
     'HDRBLKS',
     'TYPE',
     'SITE',
     'MODEL',
     'USER',
     'SAMPLE',
     'SETNAME',
     'RUN',
     'SAMPNUM',
     'TITLE',
     'NCOUNTS',
     'NOVERFL',
     'MINIMUM',
     'MAXIMUM',
     'NONTIME',
     'NLATE',
     'FILENAM',
     'CREATED',
     'CUMULAT',
     'ELAPSDR',
     'ELAPSDA',
     'OSCILLA',
     'NSTEPS',
     'RANGE',
     'START',
     'INCREME',
     'NUMBER',
     'NFRAMES',
     'ANGLES',
     'NOVER64',
     'NPIXELB',
     'NROWS',
     'NCOLS',
     'WORDORD',
     'LONGORD',
     'TARGET',
     'SOURCEK',
     'SOURCEM',
     'FILTER',
     'CELL',
     'MATRIX',
     'LOWTEMP',
     'TEMP',
     'HITEMP',
     'ZOOM',
     'CENTER',
     'DISTANC',
     'TRAILER',
     'COMPRES',
     'LINEAR',
     'PHD',
     'PREAMP',
     'CORRECT',
     'WARPFIL',
     'WAVELEN',
     'MAXXY',
     'AXIS',
     'ENDING',
     'DETPAR',
     'LUT',
     'DISPLIM',
     'PROGRAM',
     'ROTATE',
     'BITMASK',
     'OCTMASK',
     'ESDCELL',
     'DETTYPE',
     'NEXP',
     'CCDPARM',
     'BIS',
     'CHEM',
     'MORPH',
     'CCOLOR',
     'CSIZE',
     'DNSMET',
     'DARK',
     'AUTORNG',
     'ZEROADJ',
     'XTRANS',
     'HKL&XY',
     'AXES2',
     'ENDING2',
     'FILTER2',
     'LEPTOS',
     'CFR']
    version = 86

    def __init__(self, data=None, header=None):
        FabioImage.__init__(self, data, header)
        self._BrukerImage__bpp_file = None
        self.__headerstring__ = ''

    def _readheader(self, infile):
        """
        The bruker format uses 80 char lines in key : value format
        In the first 512*5 bytes of the header there should be a
        HDRBLKS key, whose value denotes how many 512 byte blocks
        are in the total header. The header is always n*5*512 bytes,
        otherwise it wont contain whole key: value pairs
        """
        line = 80
        blocksize = 512
        nhdrblks = 5
        self.__headerstring__ = infile.read(blocksize * nhdrblks).decode('ASCII')
        self.header = self.check_header()
        for i in range(0, nhdrblks * blocksize, line):
            if self.__headerstring__[i:i + line].find(':') > 0:
                key, val = self.__headerstring__[i:i + line].split(':', 1)
                key = key.strip()
                val = val.strip()
                if key in self.header:
                    self.header[key] = self.header[key] + os.linesep + val
                else:
                    self.header[key] = val

        nhdrblks = int(self.header.get('HDRBLKS', 5))
        self.header['HDRBLKS'] = nhdrblks
        self.__headerstring__ += infile.read(blocksize * (nhdrblks - 5)).decode('ASCII')
        for i in range(5 * blocksize, nhdrblks * blocksize, line):
            if self.__headerstring__[i:i + line].find(':') > 0:
                key, val = self.__headerstring__[i:i + line].split(':', 1)
                key = key.strip()
                val = val.strip()
                if key in self.header:
                    self.header[key] = self.header[key] + os.linesep + val
                else:
                    self.header[key] = val

        self.header['datastart'] = blocksize * nhdrblks
        shape = (
         int(self.header['NROWS'].split()[0]), int(self.header['NCOLS'].split()[0]))
        self._shape = shape
        self.version = int(self.header.get('VERSION', '86'))

    def read(self, fname, frame=None):
        """
        Read in and unpack the pixels (including overflow table
        """
        with self._open(fname, 'rb') as (infile):
            try:
                self._readheader(infile)
            except Exception as err:
                raise RuntimeError('Unable to parse Bruker headers: %s' % err)

            rows, cols = self._shape
            try:
                npixelb = int(self.header['NPIXELB'])
            except Exception:
                errmsg = 'length ' + str(len(self.header['NPIXELB'])) + '\n'
                for byt in self.header['NPIXELB']:
                    errmsg += 'char: ' + str(byt) + ' ' + str(ord(byt)) + '\n'

                logger.warning(errmsg)
                raise RuntimeError(errmsg)

            data = numpy.frombuffer(infile.read(rows * cols * npixelb), dtype=self.bpp_to_numpy[npixelb]).copy()
            if not numpy.little_endian and data.dtype.itemsize > 1:
                data.byteswap(True)
            nov = int(self.header['NOVERFL'])
            if nov > 0:
                data = data.astype(numpy.uint32)
                for _ in range(nov):
                    ovfl = infile.read(16)
                    intensity = int(ovfl[0:9])
                    position = int(ovfl[9:16])
                    data[position] = intensity

        if 'LINEAR' in self.header:
            try:
                slope, offset = self.header['LINEAR'].split(None, 1)
                slope = float(slope)
                offset = float(offset)
            except Exception:
                logger.warning('Error in converting to float data with linear parameter: %s' % self.header['LINEAR'])
                slope = 1
                offset = 0

            if slope != 1 or offset != 0:
                logger.warning('performing correction with slope=%s, offset=%s (LINEAR=%s)' % (slope, offset, self.header['LINEAR']))
                data = (data * slope + offset).astype(numpy.float32)
        self.data = data.reshape(self._shape)
        self.resetvals()
        return self

    def write(self, fname):
        """
        Write a bruker image

        """
        if numpy.issubdtype(self.data.dtype, float):
            if 'LINEAR' in self.header:
                try:
                    slope, offset = self.header['LINEAR'].split(None, 1)
                    slope = float(slope)
                    offset = float(offset)
                except Exception:
                    logger.warning('Error in converting to float data with linear parameter: %s' % self.header['LINEAR'])
                    slope, offset = (1.0, 0.0)

            else:
                offset = self.data.min()
                max_data = self.data.max()
                max_range = 16777215
                if max_data > offset:
                    slope = (max_data - offset) / float(max_range)
                else:
                    slope = 1.0
                tmp_data = numpy.round((self.data - offset) / slope).astype(numpy.uint32)
                self.header['LINEAR'] = '%s %s' % (slope, offset)
        else:
            tmp_data = self.data
        bpp = self.calc_bpp(tmp_data)
        self.basic_translate(fname)
        limit = 2 ** (8 * bpp) - 1
        data = tmp_data.astype(self.bpp_to_numpy[bpp])
        reset = numpy.where(tmp_data >= limit)
        data[reset] = limit
        if not numpy.little_endian and bpp > 1:
            data.byteswap(True)
        with self._open(fname, 'wb') as (bruker):
            bruker.write(self.gen_header().encode('ASCII'))
            bruker.write(data.tobytes())
            bruker.write(self.gen_overflow().encode('ASCII'))

    def calc_bpp(self, data=None, max_entry=4096):
        """
        Calculate the number of byte per pixel to get an optimal overflow table.

        :return: byte per pixel
        """
        if data is None:
            data = self.data
        if self._BrukerImage__bpp_file is None:
            for i in [1, 2]:
                overflown = data >= 2 ** (8 * i) - 1
                if overflown.sum() < max_entry:
                    self._BrukerImage__bpp_file = i
                    break
            else:
                self._BrukerImage__bpp_file = 4

        return self._BrukerImage__bpp_file

    def gen_header(self):
        """
        Generate headers (with some magic and guesses)
        """
        headers = []
        for key in self.HEADERS_KEYS:
            if key in self.header:
                value = self.header[key]
                line = key.ljust(7) + ':'
                if type(value) in StringTypes:
                    if os.linesep in value:
                        lines = value.split(os.linesep)
                        for i in lines[:-1]:
                            headers.append((line + str(i)).ljust(80, ' '))
                            line = key.ljust(7) + ':'

                        line += str(lines[(-1)])
                    else:
                        if len(value) < 72:
                            line += str(value)
                        else:
                            for i in range(len(value) // 72):
                                headers.append(line + str(value[72 * i:72 * (i + 1)]))
                                line = key.ljust(7) + ':'

                            line += value[72 * (i + 1):]
                else:
                    if '__len__' in dir(value):
                        f = '%%.%is' % (72 // len(value) - 1)
                        line += ' '.join([f % i for i in value])
                    else:
                        line += str(value)
                    headers.append(line.ljust(80, ' '))

        header = ''.join(headers)
        if len(header) > 512 * self.header['HDRBLKS']:
            tmp = ceil(len(header) / 512.0)
            self.header['HDRBLKS'] = int(ceil(tmp / 5.0) * 5.0)
            for i in range(len(headers)):
                if headers[i].startswith('HDRBLKS'):
                    headers[i] = headers.append(('HDRBLKS:%s' % self.header['HDRBLKS']).ljust(80, ' '))

        res = pad(''.join(headers), self.SPACER + '.' * 78, 512 * int(self.header['HDRBLKS']))
        return res

    def gen_overflow(self):
        """
        Generate an overflow table
        """
        limit = 2 ** (8 * self.calc_bpp()) - 1
        flat = self.data.ravel()
        overflow_pos = numpy.where(flat >= limit)[0]
        overflow_val = flat[overflow_pos]
        overflow = ''.join(['%09i%07i' % (val, pos) for pos, val in zip(overflow_pos, overflow_val)])
        return pad(overflow, '.', 512)

    def basic_translate(self, fname=None):
        """
        Does some basic population of the headers so that the writing is possible
        """
        if 'FORMAT' not in self.header:
            self.header['FORMAT'] = '86'
        if 'HDRBLKS' not in self.header:
            self.header['HDRBLKS'] = 5
        if 'TYPE' not in self.header:
            self.header['TYPE'] = 'UNWARPED'
        if 'USER' not in self.header:
            self.header['USER'] = getpass.getuser()
        if 'FILENAM' not in self.header:
            self.header['FILENAM'] = '%s' % fname
        if 'CREATED' not in self.header:
            self.header['CREATED'] = time.ctime()
        if 'NOVERFL' not in self.header:
            self.header['NOVERFL'] = '0'
        self.header['NPIXELB'] = self.calc_bpp()
        self.header['NROWS'] = self.data.shape[0]
        self.header['NCOLS'] = self.data.shape[1]
        if 'WORDORD' not in self.header:
            self.header['WORDORD'] = '0'
        if 'LONGORD' not in self.header:
            self.header['LONGORD'] = '0'


brukerimage = BrukerImage