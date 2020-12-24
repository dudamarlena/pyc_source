# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/filesys/single_file_library_package.py
# Compiled at: 2019-01-30 13:37:02
"""A LibraryPackage that creates a single output file with delimiters.

Merge all the individual output files into a single stream with delimiters of
the form |=== begin: <path>| and |=== end: <path>|, where the path names are
sorted by name. This is designed to make diffing output against a golden copy
easy, but is is wildly inefficent, as we store all the data before writing any.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import StringIO
from googleapis.codegen.filesys.library_package import LibraryPackage

class SingleFileLibraryPackage(LibraryPackage):
    """The library package."""

    def __init__(self, stream):
        """Create a new SingleFileLibraryPackage.

    Args:
      stream: (file) A file-like object to write to.
    """
        super(SingleFileLibraryPackage, self).__init__()
        self._files = {}
        self._current_file_data = None
        self._final_output_stream = stream
        return

    def StartFile(self, name):
        """Start writing a named file to the package.

    Args:
      name: (str) path which will identify the contents in the archive.

    Returns:
      A file-like object to write the contents to.
    """
        self.EndFile()
        self._current_file_data = StringIO.StringIO()
        self._current_file_name = '%s%s' % (self._file_path_prefix, name)
        return self._current_file_data

    def EndFile(self):
        """Flush the current output file."""
        if self._current_file_data:
            data = self._current_file_data.getvalue()
            self._current_file_data.close()
            self._current_file_data = None
            if isinstance(data, unicode):
                data = data.encode('utf-8')
            self._files[self._current_file_name] = data.replace('\r\n', '\n')
        return

    def DoneWritingArchive(self):
        """Signal that we are done writing the entire package.

    Emit the files.
    """
        self.EndFile()
        for file_name in sorted(self._files):
            print('=== begin: %s' % file_name, file=self._final_output_stream)
            self._final_output_stream.write(self._files[file_name])
            print('=== end: %s' % file_name, file=self._final_output_stream)

        self._final_output_stream.flush()

    def FileExtension(self):
        """Returns the file extension for this archive."""
        return 'txt'

    def MimeType(self):
        """Returns the MIME type for this archive."""
        return 'text/plain'