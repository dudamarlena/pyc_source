# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/parser.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import logging, re
from django.utils import six
from django.utils.six.moves import cStringIO as StringIO
from reviewboard.diffviewer.errors import DiffParserError

class ParsedDiffFile(object):
    """A parsed file from a diff.

    This stores information on a single file represented in a diff, including
    the contents of that file's diff, as parsed by :py:class:`DiffParser` or
    one of its subclasses.

    Parsers should set the attributes on this based on the contents of the
    diff, and should add any data found in the diff.

    This class is meant to be used internally and by subclasses of
    :py:class:`DiffParser`.
    """

    def __init__(self):
        """Initialize the parsed file information."""
        self.origFile = None
        self.newFile = None
        self.origInfo = None
        self.newInfo = None
        self.origChangesetId = None
        self.binary = False
        self.deleted = False
        self.moved = False
        self.copied = False
        self.is_symlink = False
        self.insert_count = 0
        self.delete_count = 0
        self._data_io = StringIO()
        self._data = None
        return

    @property
    def data(self):
        """The data for this diff.

        This must be accessed after :py:meth:`finalize` has been called.
        """
        if self._data is None:
            raise ValueError(b'ParsedDiffFile.data cannot be accessed until finalize() is called.')
        return self._data

    def finalize(self):
        """Finalize the parsed diff.

        This makes the diff data available to consumers and closes the buffer
        for writing.
        """
        self._data = self._data_io.getvalue()
        self._data_io.close()

    def prepend_data(self, data):
        """Prepend data to the buffer.

        Args:
            data (bytes):
                The data to prepend.
        """
        if data:
            new_data_io = StringIO()
            new_data_io.write(data)
            new_data_io.write(self._data_io.getvalue())
            self._data_io.close()
            self._data_io = new_data_io

    def append_data(self, data):
        """Append data to the buffer.

        Args:
            data (bytes):
                The data to append.
        """
        if data:
            self._data_io.write(data)


class DiffParser(object):
    """
    Parses diff files into fragments, taking into account special fields
    present in certain types of diffs.
    """
    INDEX_SEP = b'=' * 67

    def __init__(self, data):
        from reviewboard.diffviewer.diffutils import split_line_endings
        self.base_commit_id = None
        self.new_commit_id = None
        self.data = data
        self.lines = split_line_endings(data)
        return

    def parse(self):
        """
        Parses the diff, returning a list of File objects representing each
        file in the diff.
        """
        logging.debug(b'DiffParser.parse: Beginning parse of diff, size = %s', len(self.data))
        preamble = StringIO()
        self.files = []
        parsed_file = None
        i = 0
        while i < len(self.lines):
            next_linenum, new_file = self.parse_change_header(i)
            if new_file:
                if self.files:
                    self.files[(-1)].finalize()
                parsed_file = new_file
                parsed_file.prepend_data(preamble.getvalue())
                preamble.close()
                preamble = StringIO()
                self.files.append(parsed_file)
                i = next_linenum
            elif parsed_file:
                i = self.parse_diff_line(i, parsed_file)
            else:
                preamble.write(self.lines[i])
                preamble.write(b'\n')
                i += 1

        if self.files:
            self.files[(-1)].finalize()
        preamble.close()
        logging.debug(b'DiffParser.parse: Finished parsing diff.')
        return self.files

    def parse_diff_line(self, linenum, info):
        line = self.lines[linenum]
        if info.origFile is not None and info.newFile is not None:
            if line.startswith(b'-'):
                info.delete_count += 1
            elif line.startswith(b'+'):
                info.insert_count += 1
        info.append_data(line)
        info.append_data(b'\n')
        return linenum + 1

    def parse_change_header(self, linenum):
        """
        Parses part of the diff beginning at the specified line number, trying
        to find a diff header.
        """
        info = {}
        parsed_file = None
        start = linenum
        linenum = self.parse_special_header(linenum, info)
        linenum = self.parse_diff_header(linenum, info)
        if info.get(b'skip', False):
            return (linenum, None)
        else:
            if b'origFile' in info and b'newFile' in info and b'origInfo' in info and b'newInfo' in info:
                if linenum < len(self.lines):
                    linenum = self.parse_after_headers(linenum, info)
                    if info.get(b'skip', False):
                        return (linenum, None)
                parsed_file = ParsedDiffFile()
                parsed_file.origChangesetId = info.get(b'origChangesetId')
                for attr in ('binary', 'deleted', 'moved', 'copied', 'is_symlink'):
                    setattr(parsed_file, attr, info.get(attr, False))

                for attr in ('origFile', 'newFile', 'origInfo', 'newInfo'):
                    attr_value = info.get(attr)
                    if isinstance(attr_value, six.binary_type):
                        attr_value = attr_value.decode(b'utf-8')
                    setattr(parsed_file, attr, attr_value)

                lines = self.lines[start:linenum]
                for line in lines:
                    parsed_file.append_data(line)
                    parsed_file.append_data(b'\n')

            return (
             linenum, parsed_file)

    def parse_special_header(self, linenum, info):
        """
        Parses part of a diff beginning at the specified line number, trying
        to find a special diff header. This usually occurs before the standard
        diff header.

        The line number returned is the line after the special header,
        which can be multiple lines long.
        """
        try:
            index_line = self.lines[linenum]
            is_index = index_line.startswith(b'Index: ')
        except IndexError:
            is_index = False

        if is_index:
            temp_linenum = linenum + 1
            while temp_linenum + 1 < len(self.lines):
                line = self.lines[temp_linenum]
                if line == self.INDEX_SEP:
                    try:
                        info[b'index'] = index_line.split(None, 1)[1]
                    except ValueError:
                        raise DiffParserError(b'Malformed Index line', linenum)

                    linenum = temp_linenum + 1
                    break
                elif line.startswith(('---', '+++')):
                    break
                temp_linenum += 1

        return linenum

    def parse_diff_header(self, linenum, info):
        """
        Parses part of a diff beginning at the specified line number, trying
        to find a standard diff header.

        The line number returned is the line after the special header,
        which can be multiple lines long.
        """
        try:
            line1 = self.lines[linenum]
            line2 = self.lines[(linenum + 1)]
            is_diff_header = line1.startswith(b'--- ') and line2.startswith(b'+++ ') or line1.startswith(b'*** ') and line2.startswith(b'--- ') and not line1.endswith(b' ****')
        except IndexError:
            is_diff_header = False

        if is_diff_header:
            try:
                info[b'origFile'], info[b'origInfo'] = self.parse_filename_header(self.lines[linenum][4:], linenum)
                linenum += 1
                info[b'newFile'], info[b'newInfo'] = self.parse_filename_header(self.lines[linenum][4:], linenum)
                linenum += 1
            except ValueError:
                raise DiffParserError(b'The diff file is missing revision information', linenum)

        return linenum

    def parse_after_headers(self, linenum, info):
        """Parses data after the diff headers but before the data.

        By default, this does nothing, but a DiffParser subclass can
        override to look for special headers before the content.
        """
        return linenum

    def parse_filename_header(self, s, linenum):
        if b'\t' in s:
            return s.split(b'\t', 1)
        if b'  ' in s:
            return re.split(b'  +', s, 1)
        raise DiffParserError(b'No valid separator after the filename was ' + b'found in the diff header', linenum)

    def raw_diff(self, diffset):
        """Returns a raw diff as a string.

        The returned diff as composed of all FileDiffs in the provided diffset.
        """
        return (b'').join([ filediff.diff for filediff in diffset.files.all() ])

    def get_orig_commit_id(self):
        """Returns the commit ID of the original revision for the diff.

        This is overridden by tools that only use commit IDs, not file
        revision IDs.
        """
        return

    def normalize_diff_filename(self, filename):
        """Normalize filenames in diffs.

        This strips off any leading slashes, which might occur due to
        differences in various diffing methods or APIs.
        """
        if filename.startswith(b'/'):
            return filename[1:]
        else:
            return filename