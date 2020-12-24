# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/mpaimage.py
# Compiled at: 2019-03-04 08:01:16
# Size of source mod 2**32: 4302 bytes
"""
Author:
........
* Jesse Hopkins:
  Cornell High Energy Synchrotron Source;
  Ithaca (New York, USA)

mpaimage can read ascii and binary .mpa (multiwire) files
"""
from __future__ import with_statement, print_function, division, absolute_import
import logging, numpy
from .fabioimage import FabioImage, OrderedDict
logger = logging.getLogger(__name__)

class MpaImage(FabioImage):
    __doc__ = '\n    FabIO image class for Images from multiwire data files (mpa)\n    '
    DESCRIPTION = 'multiwire data files'
    DEFAULT_EXTENSIONS = [
     'mpa']

    def _readheader(self, infile):
        """
        Read and decode the header of an image

        :param infile: Opened python file (can be stringIO or bzipped file)
        """
        header_prefix = ''
        tmp_hdr = OrderedDict([('None', OrderedDict())])
        while True:
            line = infile.readline()
            line = line.decode()
            if line.find('=') > -1:
                key, value = line.strip().split('=', 1)
                key = key.strip()
                value = value.strip()
                if header_prefix == '':
                    tmp_hdr['None'][key] = value
                else:
                    tmp_hdr[header_prefix][key] = value
            elif line.startswith('[DATA') or line.startswith('[CDAT'):
                break
            else:
                header_prefix = line.strip().strip('[]')
                tmp_hdr[header_prefix] = {}

        self.header = OrderedDict()
        for key, key_data in tmp_hdr.items():
            key = str(key)
            for subkey, subkey_data in key_data.items():
                subkey = str(subkey)
                if key == 'None':
                    self.header[subkey] = subkey_data
                else:
                    self.header[key + '_' + subkey] = subkey_data

    def read(self, fname, frame=None):
        """
        Try to read image

        :param fname: name of the file
        """
        infile = self._open(fname, 'r')
        self._readheader(infile)
        if 'ADC1_range' not in self.header.keys() or 'ADC2_range' not in self.header.keys() or 'mpafmt' not in self.header.keys():
            logger.error('Error in opening %s: badly formatted mpa header.', fname)
            raise IOError('Error in opening %s: badly formatted mpa header.' % fname)
        dim2 = int(self.header['ADC1_range'])
        dim1 = int(self.header['ADC2_range'])
        self._shape = (dim2, dim1)
        if self.header['mpafmt'] == 'asc':
            lines = infile.readlines()
        else:
            infile.close()
            infile = self._open(fname, 'rb')
            lines = infile.readlines()
        for i, line in enumerate(lines):
            if line.startswith(b'[CDAT'):
                pos = i
                break

        img = numpy.array(lines[pos + 1:], dtype=float)
        self.data = img.reshape(self._shape)
        self._shape = None
        return self


mpaimage = MpaImage