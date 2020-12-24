# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/hanzo/warctools/stream.py
# Compiled at: 2012-01-13 12:32:47
"""Read records from normal file and compressed file"""
import zlib, gzip, re
from .log import debug
from .archive_detect import is_gzip_file, guess_record_type

def open_record_stream(record_class=None, filename=None, file_handle=None, mode='rb+', gzip='auto'):
    """Can take a filename or a file_handle. Normally called indirectly from
        A record class i.e WarcRecord.open_archive. If the first parameter is None, will try to guess"""
    if file_handle is None:
        file_handle = open(filename, mode=mode)
    elif not filename:
        filename = file_handle.name
    if record_class == None:
        record_class = guess_record_type(file_handle)
    if record_class == None:
        raise StandardError('Failed to guess compression')
    record_parser = record_class.make_parser()
    if gzip == 'auto':
        if is_gzip_file(file_handle):
            gzip = 'record'
        else:
            gzip = None
    if gzip == 'record':
        return GzipRecordStream(file_handle, record_parser)
    else:
        if gzip == 'file':
            return GzipFileStream(file_handle, record_parser)
        else:
            return RecordStream(file_handle, record_parser)

        return


class RecordStream(object):
    """A readable/writable stream of Archive Records. Can be iterated over
    or read_records can give more control, and potentially offset information.
    """

    def __init__(self, file_handle, record_parser):
        self.fh = file_handle
        self.record_parser = record_parser
        self._parser = None
        return

    def seek(self, offset, pos=0):
        """Same as a seek on a file"""
        self.fh.seek(offset, pos)

    def read_records(self, limit=1, offsets=True):
        """Yield a tuple of (offset, record, errors) where
        Offset is either a number or None. 
        Record is an object and errors is an empty list
        or record is none and errors is a list"""
        nrecords = 0
        while nrecords < limit or limit is None:
            offset, record, errors = self._read_record(offsets)
            nrecords += 1
            yield (offset, record, errors)
            if not record:
                break

        return

    def __iter__(self):
        while True:
            offset, record, errors = self._read_record(offsets=False)
            if record:
                yield record
            elif errors:
                raise StandardError('Errors while decoding ' + (',').join(str(error) for error in errors))
            else:
                break

    def _read_record(self, offsets):
        """overridden by sub-classes to read individual records"""
        offset = self.fh.tell() if offsets else None
        record, errors, offset = self.record_parser.parse(self.fh, offset)
        return (offset, record, errors)

    def write(self, record):
        record.write_to(self)

    def close(self):
        self.fh.close()


class GzipRecordStream(RecordStream):
    """A stream to read/write concatted file made up of gzipped archive records"""

    def __init__(self, file_handle, record_parser):
        RecordStream.__init__(self, file_handle, record_parser)
        self.gz = None
        return

    def _read_record(self, offsets):
        errors = []
        if self.gz is not None:
            record, r_errors, _offset = self.record_parser.parse(self.gz, offset=None)
            if record:
                record.error('multiple warc records in gzip record file')
                return (
                 None, record, errors)
            self.gz.close()
            errors.extend(r_errors)
        offset = self.fh.tell() if offsets else None
        self.gz = GzipRecordFile(self.fh)
        record, r_errors, _offset = self.record_parser.parse(self.gz, offset=None)
        errors.extend(r_errors)
        return (offset, record, errors)


class GzipFileStream(RecordStream):
    """A stream to read/write gzipped file made up of all archive records"""

    def __init__(self, file_handle, record):
        RecordStream.__init__(self, gzip.GzipFile(fileobj=file_handle), record)

    def _read_record(self, offsets):
        return RecordStream._read_record(self, False)


CHUNK_SIZE = 1024
line_rx = re.compile('^(?P<line>^[^\r\n]*(?:\r\n|\r(?!\n)|\n))(?P<tail>.*)$', re.DOTALL)

class GzipRecordFile(object):
    """A file like class providing 'readline' over catted gzip'd records"""

    def __init__(self, fh):
        self.fh = fh
        self.buffer = ''
        self.z = zlib.decompressobj(16 + zlib.MAX_WBITS)
        self.done = False

    def _getline(self):
        if self.buffer:
            match = line_rx.match(self.buffer)
            if match:
                output = match.group('line')
                self.buffer = '' + match.group('tail')
                return output
            if self.done:
                output = self.buffer
                self.buffer = ''
                return output

    def readline(self):
        while True:
            output = self._getline()
            if output:
                return output
            if self.done:
                return ''
            chunk = self.fh.read(CHUNK_SIZE)
            out = self.z.decompress(chunk)
            if out:
                self.buffer += out
            if self.z.unused_data:
                self.fh.seek(-len(self.z.unused_data), 1)
                self.done = True
                continue
            if not chunk:
                self.done = True
                continue

    def close(self):
        if self.z:
            self.z.flush()