# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hanzo/warctools/arc.py
# Compiled at: 2013-01-14 05:25:26
"""An object to represent arc records"""
import re
from hanzo.warctools.record import ArchiveRecord, ArchiveParser
from hanzo.warctools.archive_detect import register_record_type

@ArchiveRecord.HEADERS(URL='URL', IP='IP-address', DATE='Archive-date', CONTENT_TYPE='Content-type', CONTENT_LENGTH='Archive-length', RESULT_CODE='Result-code', CHECKSUM='Checksum', LOCATION='Location', OFFSET='Offset', FILENAME='Filename')
class ArcRecord(ArchiveRecord):
    """Represents a record in an arc file."""

    def __init__(self, headers=None, content=None, errors=None):
        ArchiveRecord.__init__(self, headers, content, errors)

    @property
    def type(self):
        return 'response'

    def _write_to(self, out, nl):
        pass

    @classmethod
    def make_parser(cls):
        """Constructs a parser for arc records."""
        return ArcParser()


class ArcRecordHeader(ArcRecord):
    """Represents the headers in an arc record."""

    def __init__(self, headers=None, content=None, errors=None, version=None, raw_headers=None):
        ArcRecord.__init__(self, headers, content, errors)
        self.version = version
        self.raw_headers = raw_headers

    @property
    def type(self):
        return 'filedesc'

    def raw(self):
        """Return the raw representation of this record."""
        return ('').join(self.raw_headers) + self.content[1]


def rx(pat):
    """Helper function to compile a regular expression with the IGNORECASE
    flag."""
    return re.compile(pat, flags=re.IGNORECASE)


nl_rx = rx('^\r\n|\r|\n$')
length_rx = rx('^%s$' % ArcRecord.CONTENT_LENGTH)
type_rx = rx('^%s$' % ArcRecord.CONTENT_TYPE)
SPLIT = re.compile('\\b\\s|\\s\\b').split

class ArcParser(ArchiveParser):
    """A parser for arc archives."""

    def __init__(self):
        self.version = 0
        self.headers = []
        self.trailing_newlines = 0

    def parse(self, stream, offset, line=None):
        """Parses a stream as an arc archive and returns an Arc record along
        with the offset in the stream of the end of the record."""
        record = None
        content_type = None
        content_length = None
        if line is None:
            line = stream.readline()
        while not line.rstrip():
            if not line:
                return (None, (), offset)
            self.trailing_newlines -= 1
            line = stream.readline()

        if line.startswith('filedesc:'):
            raw_headers = []
            raw_headers.append(line)
            arc_version_line = stream.readline()
            raw_headers.append(arc_version_line)
            arc_names_line = stream.readline()
            raw_headers.append(arc_names_line)
            arc_version = arc_version_line.strip()
            self.version = arc_version.split()[0]
            self.headers = arc_names_line.strip().split()
            arc_headers = self.parse_header_list(line)
            content_type, content_length, errors = self.get_content_headers(arc_headers)
            content_length = content_length - len(arc_version_line) - len(arc_names_line)
            record = ArcRecordHeader(headers=arc_headers, version=arc_version, errors=errors, raw_headers=raw_headers)
        else:
            if not self.headers:
                raise StandardError('missing filedesc')
            headers = self.parse_header_list(line)
            content_type, content_length, errors = self.get_content_headers(headers)
            record = ArcRecord(headers=headers, errors=errors)
        line = None
        if content_length:
            content = []
            length = 0
            while length < content_length:
                line = stream.readline()
                if not line:
                    break
                content.append(line)
                length += len(line)

            content = ('').join(content)
            content, line = content[0:content_length], content[content_length + 1:]
            record.content = (content_type, content)
        if line:
            record.error('trailing data at end of record', line)
        if line == '':
            self.trailing_newlines = 1
        return (record, (), offset)

    def trim(self, stream):
        return ()

    def parse_header_list(self, line):
        line = line.rstrip('\r\n')
        values = SPLIT(line)
        if len(self.headers) != len(values):
            if self.headers[0] in (ArcRecord.URL, ArcRecord.CONTENT_TYPE):
                values = [ s[::-1] for s in reversed(SPLIT(line[::-1], len(self.headers) - 1)) ]
            else:
                values = SPLIT(line, len(self.headers) - 1)
        if len(self.headers) != len(values):
            raise StandardError('missing headers %s %s' % ((',').join(values), (',').join(self.headers)))
        return zip(self.headers, values)

    @staticmethod
    def get_content_headers(headers):
        content_type = None
        content_length = None
        errors = []
        for name, value in headers:
            if type_rx.match(name):
                if value:
                    content_type = value
                else:
                    errors.append(('invalid header', name, value))
            elif length_rx.match(name):
                try:
                    content_length = int(value)
                except ValueError:
                    errors.append(('invalid header', name, value))

        return (
         content_type, content_length, errors)


register_record_type(re.compile('^filedesc://'), ArcRecord)