# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/mozilla/core/zip.py
# Compiled at: 2008-12-22 17:59:07
import zipfile, StringIO

class ZipHandler(object):
    """
  Class for handling zip (jar, xpi) files 
  """

    def __init__(self, path=None):
        """
    @param path: path to a zip-file. If given, the file will be automatically 
    opened
    """
        if path is not None:
            self.open(path)
        return

    def open(self, path):
        """
    Opens the given file and returns a zipfile instance
    @param path: path to a zip-file
    """
        if not zipfile.is_zipfile(path):
            raise Exception('Not a valid ZIP-file: ' + path + ' !')
        self.file = zipfile.ZipFile(path, 'r')

    def open_inlinearchive(self, path):
        """
    Open a zip-file inside an already open zip-file
    @param path: path to the zip-file inside the open zip-file
    @return: instance of the inline zip-file
    """
        if not hasattr(self, 'file'):
            raise KeyError('It looks like this instance has no open zip-file!')
        zfile = StringIO.StringIO()
        zfile.write(self.file.read(path))
        return zipfile.ZipFile(zfile, 'r')

    def close(self):
        """
    Close an open zip-file instance
    """
        if not hasattr(self, 'file'):
            raise KeyError('It looks like this instance has no open zip-file!')
        self.file = self.file.close()

    def read(self, filename, encoding=None):
        """
    Read the file under the given path
    @param filename: path to the file inside the zip-file
    @param encoding: (optional) decode the source with the given encoding 
    @return: source of the file
    """
        if not hasattr(self, 'file'):
            raise KeyError('It looks like this instance has no open zip-file!')
        if encoding is not None:
            return self.file.read(filename).decode(encoding)
        return self.file.read(filename)