# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/xrd_parsers/cpi_parser.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 4101 bytes
import os
from datetime import date
import numpy as np
from pyxrd.generic.io.utils import get_case_insensitive_glob
from pyxrd.generic.utils import u
from ..base_parser import BaseParser
from .namespace import xrd_parsers
from .xrd_parser_mixin import XRDParserMixin

@xrd_parsers.register_parser()
class CPIParser(XRDParserMixin, BaseParser):
    __doc__ = '\n        ASCII Sietronics *.CPI format parser\n    '
    description = 'Sietronics *.CPI'
    extensions = get_case_insensitive_glob('*.CPI', '*.CPD', '*.CPS')

    @classmethod
    def _parse_header(cls, filename, fp, data_objects=None, close=False):
        f = fp
        try:
            basename = u(os.path.basename(filename))
        except:
            basename = None

        data_objects = cls._adapt_data_object_list(data_objects, num_samples=1)
        f.seek(0)
        f.readline()
        twotheta_min = float(f.readline().replace(',', '.').strip())
        twotheta_max = float(f.readline().replace(',', '.').strip())
        twotheta_step = float(f.readline().replace(',', '.').strip())
        twotheta_count = int((twotheta_max - twotheta_min) / twotheta_step)
        target_type = f.readline()
        alpha1 = float(f.readline().replace(',', '.').strip())
        name = ''
        while True:
            line = f.readline().strip()
            if line == 'SCANDATA' or line == '':
                data_start = f.tell()
                break
            else:
                name = line

        data_objects[0].update(filename=basename,
          name=name,
          target_type=target_type,
          alpha1=alpha1,
          twotheta_min=twotheta_min,
          twotheta_max=twotheta_max,
          twotheta_step=twotheta_step,
          twotheta_count=twotheta_count,
          data_start=data_start)
        if close:
            f.close()
        return data_objects

    @classmethod
    def _parse_data(cls, filename, fp, data_objects=None, close=False):
        f = fp
        if data_objects[0].data == None:
            data_objects[0].data = []
        if f is not None:
            f.seek(data_objects[0].data_start)
            n = 0
            while n <= data_objects[0].twotheta_count:
                line = f.readline().strip('\n').replace(',', '.')
                if line != '':
                    data_objects[0].data.append([float(data_objects[0].twotheta_min + data_objects[0].twotheta_step * n), float(line)])
                n += 1

        data_objects[0].data = np.array(data_objects[0].data)
        if close:
            f.close()
        return data_objects

    @classmethod
    def write(cls, filename, x, ys, radiation='Cu', wavelength=1.5406, tps=48.0, sample='', **kwargs):
        """
            Writes a SIETRONICS cpi text file. x and ys should be numpy arrays.
        """
        start_angle = x[0]
        end_angle = x[(-1)]
        step_size = (end_angle - start_angle) / (x.size - 1)
        with open(filename, 'w') as (f):
            f.write('SIETRONICS XRD SCAN\n')
            f.write('%.4f\n' % start_angle)
            f.write('%.4f\n' % end_angle)
            f.write('%.4f\n' % step_size)
            f.write('%s\n' % radiation)
            f.write('%.5f\n' % wavelength)
            f.write('%s\n' % date.today().strftime('%d/%m/%y %H:%M:%S'))
            f.write('%.1f\n' % tps)
            f.write('%s\n' % sample)
            f.write('SCANDATA\n')
            for y in ys[0, :]:
                f.write('%.7f\n' % y)