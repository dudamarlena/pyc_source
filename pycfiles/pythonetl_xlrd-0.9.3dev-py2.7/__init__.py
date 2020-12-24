# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xlrd\__init__.py
# Compiled at: 2013-10-17 14:05:29
from os import path
from .info import __VERSION__
from . import licences
import sys, zipfile, pprint
from . import timemachine
from .biffh import XLRDError, biff_text_from_num, error_text_from_code, XL_CELL_BLANK, XL_CELL_TEXT, XL_CELL_BOOLEAN, XL_CELL_ERROR, XL_CELL_EMPTY, XL_CELL_DATE, XL_CELL_NUMBER
from .formula import *
from .book import Book, colname
from .sheet import empty_cell
from .xldate import XLDateError, xldate_as_tuple
if sys.version.startswith('IronPython'):
    import encodings
try:
    import mmap
    MMAP_AVAILABLE = 1
except ImportError:
    MMAP_AVAILABLE = 0

USE_MMAP = MMAP_AVAILABLE
from . import book

def open_workbook(filename=None, logfile=sys.stdout, verbosity=0, use_mmap=USE_MMAP, file_contents=None, encoding_override=None, formatting_info=False, on_demand=False, ragged_rows=False):
    peeksz = 4
    if file_contents:
        peek = file_contents[:peeksz]
    else:
        f = open(filename, 'rb')
        peek = f.read(peeksz)
        f.close()
    if peek == 'PK\x03\x04':
        if file_contents:
            zf = zipfile.ZipFile(timemachine.BYTES_IO(file_contents))
        else:
            zf = zipfile.ZipFile(filename)
        component_names = zf.namelist()
        if verbosity:
            logfile.write('ZIP component_names:\n')
            pprint.pprint(component_names, logfile)
        if 'xl/workbook.xml' in component_names:
            from . import xlsx
            bk = xlsx.open_workbook_2007_xml(zf, component_names, logfile=logfile, verbosity=verbosity, use_mmap=use_mmap, formatting_info=formatting_info, on_demand=on_demand, ragged_rows=ragged_rows)
            return bk
        if 'xl/workbook.bin' in component_names:
            raise XLRDError('Excel 2007 xlsb file; not supported')
        if 'content.xml' in component_names:
            raise XLRDError('Openoffice.org ODS file; not supported')
        raise XLRDError('ZIP file contents not a known type of workbook')
    bk = book.open_workbook_xls(filename=filename, logfile=logfile, verbosity=verbosity, use_mmap=use_mmap, file_contents=file_contents, encoding_override=encoding_override, formatting_info=formatting_info, on_demand=on_demand, ragged_rows=ragged_rows)
    return bk


def dump(filename, outfile=sys.stdout, unnumbered=False):
    from .biffh import biff_dump
    bk = Book()
    bk.biff2_8_load(filename=filename, logfile=outfile)
    biff_dump(bk.mem, bk.base, bk.stream_len, 0, outfile, unnumbered)


def count_records(filename, outfile=sys.stdout):
    from .biffh import biff_count_records
    bk = Book()
    bk.biff2_8_load(filename=filename, logfile=outfile)
    biff_count_records(bk.mem, bk.base, bk.stream_len, outfile)