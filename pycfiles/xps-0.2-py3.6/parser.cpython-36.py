# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.openbsd-6.5-amd64/egg/xps/parser.py
# Compiled at: 2019-06-04 13:19:27
# Size of source mod 2**32: 4048 bytes
"""
parser.py

Parser for XPS files generated from software
"""
__author__ = 'David Kalliecharan'
__license__ = 'ISC License'
__status__ = 'Development'
from io import StringIO as _StringIO
from pandas import read_csv as _read_csv

class CasaXPS:
    __doc__ = 'CasaXPS class is a parser for an individual file output from CasaXPS\n    '

    def __init__(self, filepath_or_buffer, delimiter=',', data_start=7, header_start=2, header_len=4, *args, **kws):
        try:
            with open(filepath_or_buffer, 'r') as (f):
                self._CasaXPS__parse_xps_param(f, delimiter)
        except TypeError:
            self._CasaXPS__parse_xps_param(filepath_or_buffer, delimiter)
            filepath_or_buffer.seek(0)

        self.peak_data = _read_csv(filepath_or_buffer, skiprows=data_start, delimiter=delimiter)
        if type(filepath_or_buffer) is _StringIO:
            filepath_or_buffer.seek(0)
        hdr = _read_csv(filepath_or_buffer, skiprows=header_start, index_col=0,
          nrows=header_len,
          delimiter=delimiter)
        col_names = [col for col in hdr if 'unnamed' not in col.lower()]
        self.peak_param = hdr[col_names]
        self.peak_param = self.peak_param.transpose()
        for k in self.peak_param.keys():
            if k in ('Lineshape', 'Name'):
                self.peak_param[k] = self.peak_param[k].astype(str)
            else:
                self.peak_param[k] = self.peak_param[k].astype('float64')

        self.peak_ids = col_names

    def __parse_xps_param(self, buffer, delimiter):
        ln = buffer.readline()
        cyc, scan, elem = ln.strip().strip('"').split(':')
        ln = buffer.readline()
        offset = 0
        if delimiter == ',':
            offset += 1
        _, char_energy, _, acq_time = ln.strip().split(delimiter)[offset:]
        self.cycle = cyc
        self.scan_type = {scan: elem}
        self.characteristic_energy = float(char_energy)
        self.acq_time = float(acq_time)

    def binding_energy(self, peak_id):
        return self.peak_param.loc[peak_id]['Position']

    def fwhm(self, peak_id):
        return self.peak_param.loc[peak_id]['FWHM']

    def area(self, peak_id):
        if type(peak_id) == list:
            return sum([self.peak_param.loc[pk]['Area'] for pk in peak_id])
        else:
            return self.peak_param.loc[peak_id]['Area']


class CasaXPSColumn:
    __doc__ = 'CasaXPSColumn class reads column data into a list of CasaXPS objects.\n    '

    def __init__(self, filename, delimiter=',', data_start=7, header_start=2, header_len=4, *args, **kws):
        with open(filename, 'r') as (f):
            data = dict()
            lines = f.readlines()
            lineno = list()
            for i, ln in enumerate(lines):
                if 'Cycle' in ln:
                    lineno.append(i)

            lineno.append(-1)
            self.scan = list()
            for i in range(0, len(lineno) - 1):
                a = lineno[i]
                b = lineno[(i + 1)]
                f = ''.join(lines[a:b])
                stream = _StringIO(f)
                casa = CasaXPS(stream, delimiter, data_start, header_start,
 header_len, *args, **kws)
                self.scan.append(casa)