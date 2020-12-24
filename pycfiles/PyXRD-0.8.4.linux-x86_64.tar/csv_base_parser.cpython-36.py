# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/file_parsers/csv_base_parser.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2476 bytes
import csv, logging
logger = logging.getLogger(__name__)
from .ascii_parser import ASCIIParser

class CSVBaseParser(ASCIIParser):
    __doc__ = '\n        CSV parser base functionality\n    '
    default_fmt_params = {'delimiter':',', 
     'doublequote':True, 
     'escapechar':None, 
     'quotechar':'"', 
     'quoting':csv.QUOTE_MINIMAL, 
     'skipinitialspace':True, 
     'strict':False}

    @classmethod
    def parse_raw_line(cls, line, conv, **fmt_params):
        """ Parses a single raw line (read as a string) """
        fmt_params = dict((cls.default_fmt_params), **fmt_params)
        for row in (csv.reader)([line], **fmt_params):
            return list(map(conv, row))

    @classmethod
    def sniff(cls, f, **fmt_params):
        """ CSV Dialect guessing - f needs to be a file object! """
        dialect = None
        has_header = True
        file_start = 0
        if f is not None:
            f.seek(file_start)
            while 1:
                file_start = f.tell()
                line = f.readline()
                if not line:
                    break
                if not line.strip().startswith('#'):
                    break

            try:
                sniffer = csv.Sniffer()
                f.seek(file_start)
                has_header = sniffer.has_header(f.read(1024))
                f.seek(file_start)
                f.readline()
                dialect = sniffer.sniff(f.read(1024))
                f.seek(file_start)
            except:
                logger.warning('Errors encountered while sniffing CSV dialect!')

        default_fmt_params = dict((cls.default_fmt_params), **)
        return (
         dict(default_fmt_params, **fmt_params), has_header, file_start)