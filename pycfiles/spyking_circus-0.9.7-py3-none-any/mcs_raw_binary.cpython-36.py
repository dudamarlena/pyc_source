# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/github/spyking-circus/build/lib/circus/files/mcs_raw_binary.py
# Compiled at: 2019-11-21 11:07:32
# Size of source mod 2**32: 3417 bytes
import numpy, re, sys, re, logging
from circus.shared.messages import print_and_log
from .raw_binary import RawBinaryFile
logger = logging.getLogger(__name__)

class RawMCSFile(RawBinaryFile):
    description = 'mcs_raw_binary'
    extension = ['.raw', '.dat']
    _required_fields = {'data_dtype': str}

    def to_str(self, b, encoding='ascii'):
        """
        Helper function to convert a byte string (or a QByteArray) to a string --
        for Python 3, this specifies an encoding to not end up with "b'...'".
        """
        if sys.version_info[0] == 3:
            return str(b, encoding=encoding)
        else:
            return str(b)

    def _get_header(self):
        try:
            header = 0
            stop = False
            fid = open(self.file_name, 'rb')
            header_text = ''
            while stop is False and header <= 5000:
                header += 1
                char = fid.read(1)
                header_text += char.decode('Windows-1252')
                if header > 2 and header_text[header - 3:header] == 'EOH':
                    stop = True

            fid.close()
            if stop is False:
                print_and_log(['Wrong MCS header: file is not exported with MCRack'], 'error', logger)
                sys.exit(1)
            else:
                header += 2
            full_header = {}
            f = open(self.file_name, 'rb')
            g = self.to_str((f.read(header)), encoding='Windows-1252')
            h = g.replace('\r', '')
            for i, item in enumerate(h.split('\n')):
                if '=' in item:
                    if item.split(' = ')[0] == 'Di':
                        if len(item.split('=')) == 3:
                            full_header['Di'] = item.split(' = ')[1].split(';')[0]
                            full_header['El'] = item.split(' = ')[2]
                    full_header[item.split(' = ')[0]] = item.split(' = ')[1]

            f.close()
            if 'El' in full_header:
                regexp = re.compile('El_\\d*')
            else:
                if 'Fi' in full_header:
                    regexp = re.compile('Fi_\\d*')
            return (
             full_header, header, len(regexp.findall(full_header['Streams'])))
        except Exception:
            print_and_log(['Wrong MCS header: file is not exported with MCRack'], 'error', logger)
            sys.exit(1)

    def _read_from_header(self):
        a, b, c = self._get_header()
        header = a
        header['data_offset'] = b
        header['nb_channels'] = c
        if 'El' in header:
            header['gain'] = float(re.findall('\\d+\\.\\d+', header['El'])[0])
        else:
            if 'Fi' in header:
                header['gain'] = float(re.findall('\\d+\\.\\d+', header['Fi'])[0])
        header['sampling_rate'] = float(header['Sample rate'])
        header['data_dtype'] = self.params['data_dtype']
        self.data = numpy.memmap((self.file_name), offset=(header['data_offset']), dtype=(header['data_dtype']), mode='r')
        self.size = len(self.data)
        self._shape = (self.size // header['nb_channels'], header['nb_channels'])
        del self.data
        return header