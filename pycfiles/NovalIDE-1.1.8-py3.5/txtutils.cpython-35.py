# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/util/txtutils.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 3292 bytes
"""
Editra Buisness Model Library: FileTypeChecker

Helper class for checking what kind of a content a file contains.

"""
__all__ = [
 'txtutils']
import os, types, noval.util.apputils as apputils

class FileTypeChecker(object):
    __doc__ = 'File type checker and recognizer'
    TXTCHARS = ''.join(map(chr, [7, 8, 9, 10, 12, 13, 27] + list(range(32, 256))))
    ALLBYTES = ''.join(map(chr, list(range(256))))

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

    def IsBinaryBytes(self, bytes_str):
        """Check if the given string is composed of binary bytes
        @param bytes: string

        """
        return False
        trantab = str.maketrans(FileTypeChecker.ALLBYTES, FileTypeChecker.ALLBYTES, FileTypeChecker.TXTCHARS)
        print(trantab)
        nontext = bytes_str.translate(trantab.keys())
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

    @staticmethod
    def IsUnicode(txt):
        """Is the given string a unicode string
        @param txt: object
        @return: bool

        """
        if apputils.is_py2():
            return isinstance(txt, types.UnicodeType)
        if apputils.is_py3_plus():
            return isinstance(txt, str)


def IsUnicode(txt):
    """Is the given string a unicode string
    @param txt: object
    @return: bool

    """
    return FileTypeChecker.IsUnicode(txt)


def DecodeString(txt, enc):
    """Decode the given string with the given encoding,
    only attempts to decode if the given txt is not already Unicode
    @param txt: string
    @param enc: encoding 'utf-8'
    @return: unicode

    """
    if IsUnicode(txt):
        txt = txt.decode(enc)
    return txt


if __name__ == '__main__':
    file_name = 'D:\\env\\Noval\\NovalIDE_Setup.exe'