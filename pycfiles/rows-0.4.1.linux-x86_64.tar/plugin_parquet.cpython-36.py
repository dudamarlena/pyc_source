# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/turicas/software/pyenv/versions/rows/lib/python3.6/site-packages/rows/plugins/plugin_parquet.py
# Compiled at: 2019-02-13 03:47:25
# Size of source mod 2**32: 2366 bytes
from __future__ import unicode_literals
import logging
from collections import OrderedDict
from rows import fields
from rows.plugins.utils import create_table, get_filename_and_fobj

class NullHandler(logging.Handler):

    def emit(self, record):
        pass


logging.getLogger('parquet').addHandler(NullHandler())
import parquet
PARQUET_TO_ROWS = {parquet.parquet_thrift.Type.BOOLEAN: fields.BoolField, 
 parquet.parquet_thrift.Type.BYTE_ARRAY: fields.BinaryField, 
 parquet.parquet_thrift.Type.DOUBLE: fields.FloatField, 
 parquet.parquet_thrift.Type.FIXED_LEN_BYTE_ARRAY: fields.BinaryField, 
 parquet.parquet_thrift.Type.FLOAT: fields.FloatField, 
 parquet.parquet_thrift.Type.INT32: fields.IntegerField, 
 parquet.parquet_thrift.Type.INT64: fields.IntegerField, 
 parquet.parquet_thrift.Type.INT96: fields.IntegerField}

def import_from_parquet(filename_or_fobj, *args, **kwargs):
    """Import data from a Parquet file and return with rows.Table."""
    filename, fobj = get_filename_and_fobj(filename_or_fobj, mode='rb')
    types = OrderedDict([(schema.name, PARQUET_TO_ROWS[schema.type]) for schema in parquet._read_footer(fobj).schema if schema.type is not None])
    header = list(types.keys())
    table_rows = list(parquet.reader(fobj))
    meta = {'imported_from':'parquet', 
     'filename':filename}
    return create_table(
 ([
  header] + table_rows), *args, meta=meta, force_types=types, **kwargs)