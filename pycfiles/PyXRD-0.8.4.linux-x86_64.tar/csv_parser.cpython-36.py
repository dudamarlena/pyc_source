# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/xrd_parsers/csv_parser.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 5111 bytes
import os, csv, numpy as np
from pyxrd.generic.io.utils import get_case_insensitive_glob
from pyxrd.generic.utils import u
from ..csv_base_parser import CSVBaseParser
from .namespace import xrd_parsers
from .xrd_parser_mixin import XRDParserMixin

class GenericXYCSVParser(XRDParserMixin, CSVBaseParser):
    __doc__ = '\n        Generic xy-data CSV parser. Does not care about extensions. \n        Should be sub-classed!\n    '
    description = 'ASCII XY data'
    default_fmt_params = {'delimiter':',', 
     'doublequote':True, 
     'escapechar':None, 
     'quotechar':'"', 
     'quoting':csv.QUOTE_MINIMAL, 
     'skipinitialspace':True, 
     'strict':False}

    @classmethod
    def _parse_header(cls, filename, fp, data_objects=None, close=False, split_columns=True, has_header=True, file_start=0, **fmt_params):
        fmt_params = dict((cls.default_fmt_params), **fmt_params)
        f = fp
        f.seek(file_start)
        try:
            basename = u(os.path.basename(filename))
        except:
            basename = None

        header = f.readline().strip()
        if not has_header:
            f.seek(file_start)
        data_start_pos = f.tell()
        first_line = f.readline().strip()
        twotheta_count, last_line = cls.get_last_line(f)
        last_line = last_line.strip()
        f.seek(data_start_pos)
        first_line_vals = (cls.parse_raw_line)(first_line, float, **fmt_params)
        last_line_vals = (cls.parse_raw_line)(last_line, float, **fmt_params)
        num_samples = len(first_line_vals) - 1
        twotheta_min = first_line_vals[0]
        twotheta_max = last_line_vals[0]
        twotheta_step = int((twotheta_max - twotheta_min) / twotheta_count)
        sample_names = (cls.parse_raw_line)(header, (lambda s: s), **fmt_params)[1:]
        if len(sample_names) < num_samples:
            sample_names.extend([''] * (num_samples - len(sample_names)))
        if len(sample_names) > num_samples:
            sample_names = sample_names[:num_samples]
        data_objects = cls._adapt_data_object_list(data_objects, num_samples=num_samples)
        for i, sample_name in enumerate(sample_names):
            data_objects[i].update(filename=basename,
              name=sample_name,
              twotheta_min=twotheta_min,
              twotheta_max=twotheta_max,
              twotheta_step=twotheta_step,
              twotheta_count=twotheta_count)

        if close:
            f.close()
        return data_objects

    @classmethod
    def _parse_data(cls, filename, fp, data_objects=None, close=False, split_columns=True, has_header=True, **fmt_params):
        f = fp
        if f is not None:
            for row in (csv.reader)(f, **fmt_params):
                if row:
                    data = list(map(float, row))
                    x, ay = data[0], data[1:]
                    for data_object, y in zip(data_objects, ay):
                        if getattr(data_object, 'data', None) is None:
                            data_object.data = []
                        data_object.data.append([x, y])

            for data_object in data_objects:
                data_object.data = np.array(data_object.data)

        if close:
            f.close()
        return data_objects

    @classmethod
    def parse(cls, fp, data_objects=None, close=True, split_columns=True, **fmt_params):
        """
            Files are sniffed for the used csv dialect, but an optional set of
            formatting parameters can be passed that will override the sniffed
            parameters.
        """
        filename, f, close = cls._get_file(fp, close=close)
        fmt_params, has_header, file_start = (cls.sniff)(f, **fmt_params)
        data_objects = (cls._parse_header)(filename, f, data_objects=data_objects, split_columns=split_columns, has_header=has_header, file_start=file_start, **fmt_params)
        data_objects = (cls._parse_data)(filename, f, data_objects=data_objects, split_columns=split_columns, has_header=has_header, **fmt_params)
        if close:
            f.close()
        return data_objects


@xrd_parsers.register_parser()
class CSVParser(GenericXYCSVParser):
    __doc__ = '\n        ASCII *.DAT, *.CSV, *.TAB and *.XY format parser\n    '
    description = 'CSV XRD data'
    extensions = get_case_insensitive_glob('*.DAT', '*.CSV', '*.TAB', '*.XY')