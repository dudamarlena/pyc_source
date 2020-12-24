# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/filesys/tar_library_package.py
# Compiled at: 2019-01-24 16:56:47
"""A LibraryPackage that creates a .tar.gz file.

This module aids in the construction of a .tar.gz file containing all the
components generated and required by a library.
"""
__author__ = 'sammccall@google.com (Sam McCall)'
from io import BytesIO
import StringIO, tarfile, time
from googleapis.codegen.filesys.library_package import LibraryPackage

class TarLibraryPackage(LibraryPackage):
    """The library package."""

    def __init__(self, stream, compress=True):
        """Create a new TarLibraryPackage.

    Args:
      stream: (file) A file-like object to write to.
      compress: (boolean) Whether to gzip-compress the output.
    """
        super(TarLibraryPackage, self).__init__()
        mode = 'w:gz' if compress else 'w'
        self._tar = tarfile.open(fileobj=stream, mode=mode)
        self._current_file_data = None
        self._compress = compress
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
        name = '%s%s' % (self._file_path_prefix, name)
        self._current_file_name = name.encode('ascii')
        return self._current_file_data

    def EndFile(self):
        """Flush the current output file to the tar container."""
        if self._current_file_data:
            info = tarfile.TarInfo(self._current_file_name)
            info.mtime = time.time()
            info.mode = 420
            data = self._current_file_data.getvalue()
            if isinstance(data, unicode):
                data = data.encode('utf-8')
            info.size = len(data)
            self._tar.addfile(info, BytesIO(data))
            self._current_file_data.close()
            self._current_file_data = None
        return

    def DoneWritingArchive(self):
        """Signal that we are done writing the entire package.

    This method must be called to flush the tar file directory to the output
    stream.
    """
        if self._tar:
            self.EndFile()
            self._tar.close()
            self._tar = None
        return

    def FileExtension(self):
        """Returns the file extension for this archive, either tar or tgz."""
        if self._compress:
            return 'tgz'
        else:
            return 'tar'

    def MimeType(self):
        """Returns the MIME type for this archive."""
        if self._compress:
            return 'application/x-gtar-compressed'
        return 'application/x-gtar'