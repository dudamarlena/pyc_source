# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/simpleavro/commands.py
# Compiled at: 2011-05-27 20:05:22
__all__ = [
 'read', 'write', 'count']
from avro.datafile import DataFileWriter, DataFileReader
from avro.io import DatumWriter, DatumReader
import avro.schema

def _open(avro, mode):
    if not isinstance(avro, basestring):
        return stream
    return open(avro, mode)


class read:

    def __init__(self, avro_file):
        """Open Avro file for reading.

        avro_file can be either a file object or a file name"""
        fo = _open(avro_file, 'rb')
        self.reader = DataFileReader(fo, DatumReader())
        self.schema = avro.schema.parse(self.reader.meta['avro.schema'])

    def next(self):
        """Return next record."""
        return next(self.reader)

    def __iter__(self):
        """Return iterator."""
        return iter(self.reader)


def write(avro_file, schema, records):
    """Write records to avro.

    avro_file can be either file object or a file name.
    """
    fo = _open(avro_file, 'wb')
    writer = DataFileWriter(fo, DatumWriter(), schema)
    for record in records:
        writer.append(record)

    writer.close()


def count(avro):
    """Return number of records in avro file.

    avro can be either file object or a file name.
    """
    for count, _ in enumerate(read(avro), 1):
        pass

    return count