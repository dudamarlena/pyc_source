# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ebmlib/fchecker.py
# Compiled at: 2010-08-07 18:48:51
"""
Editra Buisness Model Library: FileTypeChecker

Helper class for checking what kind of a content a file contains.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__cvsid__ = '$Id: fchecker.py 65147 2010-07-31 05:59:58Z CJP $'
__revision__ = '$Revision: 65147 $'
__all__ = [
 'FileTypeChecker']
import os

class FileTypeChecker(object):
    """File type checker and recognizer"""
    TXTCHARS = ('').join(map(chr, [7, 8, 9, 10, 12, 13, 27] + range(32, 256)))
    ALLBYTES = ('').join(map(chr, range(256)))

    def __init__(self, preread=4096):
        """Create the FileTypeChecker
        @keyword preread: number of bytes to read for checking file type

        """
        super(FileTypeChecker, self).__init__()
        self._preread = preread

    @staticmethod
    def _GetHandle(fname):
        """Get a file handle for reading
        @param fname: filename
        @return: file object or None

        """
        try:
            handle = open(fname, 'rb')
        except:
            handle = None

        return handle

    def IsBinary(self, fname):
        """Is the file made up of binary data
        @param fname: filename to check
        @return: bool

        """
        handle = self._GetHandle(fname)
        if handle is not None:
            bytes = handle.read(self._preread)
            handle.close()
            return self.IsBinaryBytes(bytes)
        else:
            return False
            return

    def IsBinaryBytes(self, bytes):
        """Check if the given string is composed of binary bytes
        @param bytes: string

        """
        nontext = bytes.translate(FileTypeChecker.ALLBYTES, FileTypeChecker.TXTCHARS)
        return bool(nontext)

    def IsReadableText(self, fname):
        """Is the given path readable as text. Will return True if the
        file is accessable by current user and is plain text.
        @param fname: filename
        @return: bool

        """
        f_ok = False
        if os.access(fname, os.R_OK):
            f_ok = not self.IsBinary(fname)
        return f_ok