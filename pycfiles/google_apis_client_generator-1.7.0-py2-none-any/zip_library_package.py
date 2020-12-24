# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/filesys/zip_library_package.py
# Compiled at: 2019-01-24 16:56:47
"""A LibraryPackage that creates a Zip file.

This module aids in the construction of a ZIP file containing all the
components generated and required by a library.
"""
__author__ = 'aiuto@google.com (Tony Aiuto)'
import os, StringIO, zipfile
from googleapis.codegen.filesys.library_package import LibraryPackage

class ZipLibraryPackage(LibraryPackage):
    """The library package."""

    def __init__(self, stream):
        """Create a new ZipLibraryPackage.

    Args:
      stream: (file) A file-like object to write to.
    """
        super(ZipLibraryPackage, self).__init__()
        self._zip = zipfile.ZipFile(stream, 'w', zipfile.ZIP_STORED)
        self._current_file_data = None
        self._created_dirs = []
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
        self.CreateDirectory(os.path.dirname(self._current_file_name))
        return self._current_file_data

    def CreateDirectory(self, directory):
        """Create one or more directory entries, esssentially mkdir -p.

    Some zip readers do not create needed folders for arbitrary file paths.
    When we encounter a new path for the first time, we make sure the tree
    exists.

    Args:
      directory: (str) a directory name.
    """
        to_create = []
        while directory:
            if directory in self._created_dirs:
                break
            to_create.append(directory)
            self._created_dirs.append(directory)
            directory = os.path.dirname(directory)

        to_create.reverse()
        for directory in to_create:
            info = zipfile.ZipInfo((directory + '/').encode('ascii'), date_time=self.ZipTimestamp())
            info.external_attr = 1106051088
            self._zip.writestr(info, '')

    def EndFile(self):
        """Flush the current output file to the ZIP container."""
        if self._current_file_data:
            info = zipfile.ZipInfo(self._current_file_name, date_time=self.ZipTimestamp())
            info.external_attr = 27525120
            data = self._current_file_data.getvalue()
            if isinstance(data, unicode):
                data = data.encode('utf-8')
            self._zip.writestr(info, data)
            self._current_file_data.close()
            self._current_file_data = None
        return

    def ZipTimestamp(self):
        return (1980, 1, 1, 0, 0, 1)

    def DoneWritingArchive(self):
        """Signal that we are done writing the entire package.

    This method must be called to flush the zip file directory to the output
    stream.
    """
        if self._zip:
            self.EndFile()
            self._zip.close()
            self._zip = None
        return

    def FileExtension(self):
        """Returns the file extension for this archive, which is zip."""
        return 'zip'

    def MimeType(self):
        """Returns the MIME type for this archive."""
        return 'application/zip'