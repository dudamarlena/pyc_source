# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/xrd_parsers/rd_parser.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 4734 bytes
import os, struct
from io import SEEK_SET
import numpy as np
from pyxrd.generic.io.utils import get_case_insensitive_glob
from pyxrd.generic.utils import u
from ..base_parser import BaseParser
from .namespace import xrd_parsers
from .xrd_parser_mixin import XRDParserMixin

def cap(lower, value, upper, out=None):
    if value < lower or value > upper:
        if out is not None:
            return out
        return min(max(value, lower), upper)
    else:
        return value


@xrd_parsers.register_parser()
class RDParser(XRDParserMixin, BaseParser):
    __doc__ = '\n        Philips Binary V3 & V5 *.RD format parser\n    '
    description = 'Phillips Binary V3/V5 *.RD'
    extensions = get_case_insensitive_glob('*.RD')
    mimetypes = ['application/octet-stream']
    __file_mode__ = 'rb'

    @classmethod
    def _parse_header(cls, filename, fp, data_objects=None, close=False):
        f = fp
        try:
            basename = u(os.path.basename(filename))
        except:
            basename = None

        data_objects = cls._adapt_data_object_list(data_objects, num_samples=1)
        f.seek(0, SEEK_SET)
        version = f.read(2).decode()
        if version in ('V3', 'V5'):
            f.seek(84, SEEK_SET)
            diffractomer_type, target_type, focus_type = struct.unpack('bbb', f.read(3))
            diffractomer_type = {0:b'PW1800', 
             1:b'PW1710 based system', 
             2:b'PW1840', 
             3:b'PW3710 based system', 
             4:b'Undefined', 
             5:b"X'Pert MPD"}[cap(0, diffractomer_type, 5, 4)]
            target_type = {0:b'Cu', 
             1:b'Mo', 
             2:b'Fe', 
             3:b'Cr', 
             4:b'Other'}[cap(0, target_type, 3, 4)]
            focus_type = {0:b'BF', 
             1:b'NF', 
             2:b'FF', 
             3:b'LFF', 
             4:b'Unkown'}[cap(0, focus_type, 3, 4)]
            f.seek(94, SEEK_SET)
            alpha1, alpha2, alpha_factor = struct.unpack('ddd', f.read(24))
            f.seek(146, SEEK_SET)
            sample_name = u(f.read(16).replace(b'\x00', b''))
            f.seek(214)
            twotheta_step, twotheta_min, twotheta_max = struct.unpack('ddd', f.read(24))
            twotheta_count = int((twotheta_max - twotheta_min) / twotheta_step)
            data_start = {'V3':250, 
             'V5':810}[version]
            data_objects[0].update(filename=basename,
              name=sample_name,
              twotheta_min=twotheta_min,
              twotheta_max=twotheta_max,
              twotheta_step=twotheta_step,
              twotheta_count=twotheta_count,
              target_type=target_type,
              alpha1=alpha1,
              alpha2=alpha2,
              alpha_factor=alpha_factor,
              data_start=data_start,
              version=version)
        else:
            raise IOError('Only V3 and V5 *.RD files are supported!')
        if close:
            f.close()
        return data_objects

    @classmethod
    def _parse_data(cls, filename, fp, data_objects=None, close=False):
        f = fp
        if data_objects[0].data == None:
            data_objects[0].data = []
        if f is not None:
            if data_objects[0].version in ('V3', 'V5'):
                f.seek(data_objects[0].data_start)
                n = 0
                while n < data_objects[0].twotheta_count:
                    y, = struct.unpack('H', f.read(2))
                    data_objects[0].data.append([
                     data_objects[0].twotheta_min + data_objects[0].twotheta_step * float(n + 0.5),
                     float(y)])
                    n += 1

            else:
                raise IOError('Only V3 and V5 *.RD files are supported!')
        data_objects[0].data = np.array(data_objects[0].data)
        if close:
            f.close()
        return data_objects