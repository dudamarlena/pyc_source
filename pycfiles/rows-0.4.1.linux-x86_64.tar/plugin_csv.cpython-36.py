# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/turicas/software/pyenv/versions/rows/lib/python3.6/site-packages/rows/plugins/plugin_csv.py
# Compiled at: 2019-02-13 03:47:25
# Size of source mod 2**32: 5695 bytes
from __future__ import unicode_literals
import sys
from io import BytesIO
import six, unicodecsv
from rows.plugins.utils import create_table, get_filename_and_fobj, ipartition, serialize
sniffer = unicodecsv.Sniffer()
unicodecsv.field_size_limit(sys.maxsize)

def fix_dialect(dialect):
    if not dialect.doublequote:
        if dialect.escapechar is None:
            dialect.doublequote = True
    if dialect.quoting == unicodecsv.QUOTE_MINIMAL:
        if dialect.quotechar == "'":
            dialect.quotechar = '"'


if six.PY2:

    def discover_dialect(sample, encoding=None, delimiters=(b',', b';', b'\t', b'|')):
        """Discover a CSV dialect based on a sample size.

        `encoding` is not used (Python 2)
        """
        try:
            dialect = sniffer.sniff(sample, delimiters=delimiters)
        except unicodecsv.Error:
            dialect = unicodecsv.excel

        fix_dialect(dialect)
        return dialect


else:
    if six.PY3:

        def discover_dialect(sample, encoding, delimiters=(',', ';', '\t', '|')):
            """Discover a CSV dialect based on a sample size.

        `sample` must be `bytes` and an `encoding must be provided (Python 3)
        """
            finished = False
            while not finished:
                try:
                    decoded = sample.decode(encoding)
                except UnicodeDecodeError as exception:
                    _, _, _, pos, error = exception.args
                    if error == 'unexpected end of data':
                        if pos == len(sample):
                            sample = sample[:-1]
                    else:
                        raise
                else:
                    finished = True

            try:
                dialect = sniffer.sniff(decoded, delimiters=delimiters)
            except unicodecsv.Error:
                dialect = unicodecsv.excel

            fix_dialect(dialect)
            return dialect


def read_sample(fobj, sample):
    """Read `sample` bytes from `fobj` and return the cursor to where it was."""
    cursor = fobj.tell()
    data = fobj.read(sample)
    fobj.seek(cursor)
    return data


def import_from_csv(filename_or_fobj, encoding='utf-8', dialect=None, sample_size=262144, *args, **kwargs):
    """Import data from a CSV file (automatically detects dialect).

    If a file-like object is provided it MUST be in binary mode, like in
    `open(filename, mode='rb')`.
    """
    filename, fobj = get_filename_and_fobj(filename_or_fobj, mode='rb')
    if dialect is None:
        dialect = discover_dialect(sample=(read_sample(fobj, sample_size)),
          encoding=encoding)
    reader = unicodecsv.reader(fobj, encoding=encoding, dialect=dialect)
    meta = {'imported_from':'csv', 
     'filename':filename,  'encoding':encoding}
    return create_table(reader, *args, meta=meta, **kwargs)


def export_to_csv(table, filename_or_fobj=None, encoding='utf-8', dialect=unicodecsv.excel, batch_size=100, callback=None, *args, **kwargs):
    """Export a `rows.Table` to a CSV file.

    If a file-like object is provided it MUST be in binary mode, like in
    `open(filename, mode='wb')`.
    If not filename/fobj is provided, the function returns a string with CSV
    contents.
    """
    if filename_or_fobj is not None:
        _, fobj = get_filename_and_fobj(filename_or_fobj, mode='wb')
    else:
        fobj = BytesIO()
    writer = unicodecsv.writer(fobj, encoding=encoding, dialect=dialect)
    if callback is None:
        for batch in ipartition(serialize(table, *args, **kwargs), batch_size):
            writer.writerows(batch)

    else:
        serialized = serialize(table, *args, **kwargs)
        writer.writerow(next(serialized))
        total = 0
        for batch in ipartition(serialized, batch_size):
            writer.writerows(batch)
            total += len(batch)
            callback(total)

    if filename_or_fobj is not None:
        fobj.flush()
        return fobj
    else:
        fobj.seek(0)
        result = fobj.read()
        fobj.close()
        return result