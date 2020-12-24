# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/atom_type_parsers/atl_parser.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 4135 bytes
import csv, os
from pyxrd.generic.io import get_case_insensitive_glob
from pyxrd.generic.utils import u
from pyxrd.file_parsers.csv_base_parser import CSVBaseParser
from .namespace import atom_type_parsers

@atom_type_parsers.register_parser()
class ATLAtomTypeParser(CSVBaseParser):
    __doc__ = '\n        Atomic scattering factors CSV file parser\n    '
    namespace = 'atl'
    description = 'Atom types CSV file'
    extensions = get_case_insensitive_glob('*.ATL')
    default_fmt_params = {'delimiter':',', 
     'doublequote':True, 
     'escapechar':None, 
     'quotechar':'"', 
     'quoting':csv.QUOTE_MINIMAL, 
     'skipinitialspace':True, 
     'strict':False}

    @classmethod
    def _parse_header(cls, filename, fp, data_objects=None, close=False, **fmt_params):
        try:
            fmt_params = dict((cls.default_fmt_params), **fmt_params)
            fp.seek(0)
            basename = u(os.path.basename(filename))
            header = cls.parse_raw_line(fp.readline().strip(), str)
            replace = ['a%d' % i for i in range(1, 6)] + ['b%d' % i for i in range(1, 6)] + ['c']
            header = ['par_%s' % val if val in replace else val for val in header]
            data_start_pos = fp.tell()
            line_count, _ = cls.get_last_line(fp)
            fp.seek(data_start_pos)
            data_objects = cls._adapt_data_object_list(data_objects, num_samples=line_count)
            for i in range(line_count):
                data_objects[i].update(filename=basename,
                  header=header)

        finally:
            if close:
                fp.close()

        return data_objects

    @classmethod
    def _parse_data(cls, filename, fp, data_objects=None, close=False, **fmt_params):
        if fp is not None:
            for row, data_object in zip((csv.reader)(fp, **fmt_params), data_objects):
                if row:
                    for key, val in zip(data_object.header, row):
                        setattr(data_object, key, val)

                    data_object.is_json = False

        if close:
            fp.close()
        return data_objects

    @classmethod
    def parse(cls, filename, fp, data_objects=None, close=True, **fmt_params):
        """
            Files are sniffed for the used csv dialect, but an optional set of
            formatting parameters can be passed that will override the sniffed
            parameters.
        """
        filename, fp, close = cls._get_file(filename, fp, close=close)
        fmt_params, _, _ = (cls.sniff)(fp, **fmt_params)
        data_objects = (cls.parse_header)(filename, fp, data_objects=data_objects, **fmt_params)
        data_objects = (cls.parse_data)(filename, fp, data_objects=data_objects, **fmt_params)
        if close:
            fp.close()
        return data_objects

    @classmethod
    def write(cls, filename, items, props):
        """
            Writes the header to the first line, and will write x, y1, ..., yn
            rows for each column inside the x and ys arguments.
            Header argument should not include a newline, and can be a string or
            any iterable containing strings.
        """
        atl_writer = csv.writer((open(filename, 'wb')), delimiter=',', quotechar='"', quoting=(csv.QUOTE_MINIMAL))
        atl_writer.writerow([name for prop, name in props])
        for item in items:
            prop_row = []
            for prop, name in props:
                prop_row.append(getattr(item, prop))

            atl_writer.writerow(prop_row)