# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/xrd_parsers/udf_parser.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 3825 bytes
import os, numpy as np
from pyxrd.generic.io.utils import get_case_insensitive_glob
from pyxrd.generic.utils import u
from ..base_parser import BaseParser
from .namespace import xrd_parsers
from .xrd_parser_mixin import XRDParserMixin

@xrd_parsers.register_parser()
class UDFParser(XRDParserMixin, BaseParser):
    __doc__ = '\n        ASCII Philips *.UDF format\n    '
    description = 'Philips *.UDF'
    extensions = get_case_insensitive_glob('*.UDF')

    @classmethod
    def _parse_header(cls, filename, fp, data_objects=None, close=False):
        f = fp
        try:
            basename = u(os.path.basename(filename))
        except:
            basename = None

        data_objects = cls._adapt_data_object_list(data_objects, num_samples=1)
        f.seek(0)
        header_dict = {}
        for lineno, line in enumerate(f):
            if line.strip() == 'RawScan':
                data_start = f.tell()
                break
            else:
                parts = list(map(str.strip, line.split(',')))
                if len(parts) < 3:
                    raise IOError('Header of UDF file is malformed at line %d' % lineno)
                if parts[0] == 'SampleIdent':
                    name = parts[1]
                else:
                    if parts[0] == 'DataAngleRange':
                        twotheta_min = float(parts[1])
                        twotheta_max = float(parts[2])
                    else:
                        if parts[0] == 'ScanStepSize':
                            twotheta_step = float(parts[1])
                header_dict[parts[0]] = ','.join(parts[1:-1])

        twotheta_count = int((twotheta_max - twotheta_min) / twotheta_step)
        (data_objects[0].update)(filename=basename, 
         name=name, 
         twotheta_min=twotheta_min, 
         twotheta_max=twotheta_max, 
         twotheta_step=twotheta_step, 
         twotheta_count=twotheta_count, 
         data_start=data_start, **header_dict)
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
            last_value_reached = False
            while n <= data_objects[0].twotheta_count and not last_value_reached:
                parts = list(map(str.strip, f.readline().split(',')))
                for part in parts:
                    if part.endswith('/'):
                        part = part[:-1]
                        last_value_reached = True
                    n += 1
                    data_objects[0].data.append([float(data_objects[0].twotheta_min + data_objects[0].twotheta_step * n), float(part)])

        data_objects[0].data = np.array(data_objects[0].data)
        if close:
            f.close()
        return data_objects