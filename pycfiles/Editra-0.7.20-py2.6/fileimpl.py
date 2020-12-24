# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ebmlib/fileimpl.py
# Compiled at: 2012-03-17 12:57:51
"""
Editra Business Model Library: FileObjectImpl

Implementation of a file object interface class. Objects and methods inside
of this library expect a file object that derives from this interface.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: fileimpl.py 70309 2012-01-10 00:09:26Z CJP $'
__revision__ = '$Revision: 70309 $'
import os, sys, txtutil, fileutil

class FileObjectImpl(object):
    """File Object Interface implementation base class"""

    def __init__(self, path='', modtime=0):
        super(FileObjectImpl, self).__init__()
        self._path = fileutil.GetPathFromURI(path)
        self._modtime = modtime
        self._handle = None
        self.open = False
        self.last_err = None
        return

    Path = property(lambda self: self.GetPath(), lambda self, path: self.SetPath(path))
    Handle = property(lambda self: self._handle)
    ModTime = property(lambda self: self.GetModTime(), lambda self, tstamp: self.SetModTime(tstamp))
    ReadOnly = property(lambda self: self.IsReadOnly())

    def ClearLastError(self):
        """Reset the error marker on this file"""
        del self.last_err
        self.last_err = None
        return

    def Clone(self):
        """Clone the file object
        @return: FileObject

        """
        fileobj = FileObjectImpl(self._path, self._modtime)
        fileobj.SetLastError(self.last_err)
        return fileobj

    def Close(self):
        """Close the file handle
        @note: this is normally done automatically after a read/write operation

        """
        try:
            self._handle.close()
        except:
            pass

        self.open = False

    def DoOpen(self, mode):
        """Opens and creates the internal file object
        @param mode: mode to open file in
        @return: True if opened, False if not
        @postcondition: self._handle is set to the open handle

        """
        if not len(self._path):
            return False
        else:
            try:
                file_h = open(self._path, mode)
            except (IOError, OSError), msg:
                self.SetLastError(unicode(msg))
                return False

            self._handle = file_h
            self.open = True
            return True

    def Exists(self):
        """Does the file exist on disk?
        @return: bool

        """
        if self._path:
            return fileutil.PathExists(self._path)
        else:
            return False

    def GetExtension(self):
        """Get the files extension if it has one else simply return the
        filename minus the path.
        @return: string file extension (no dot)

        """
        fname = os.path.split(self._path)
        return fname[(-1)].split(os.extsep)[(-1)].lower()

    def GetHandle(self):
        """Get this files handle"""
        return self._handle

    def GetLastError(self):
        """Return the last error that occurred when using this file
        @return: err traceback or None

        """
        errstr = 'None'
        if self.last_err:
            if not txtutil.IsUnicode(self.last_err):
                errstr = unicode(self.last_err)
            else:
                errstr = self.last_err
        return errstr

    def GetModTime(self):
        """Get the timestamp of this files last modification"""
        return self._modtime

    def GetPath(self):
        """Get the path of the file
        @return: string

        """
        return self._path

    def GetSize(self):
        """Get the size of the file
        @return: int

        """
        if self._path:
            return fileutil.GetFileSize(self._path)
        else:
            return 0

    def IsOpen(self):
        """Check if file is open or not
        @return: bool

        """
        return self.open

    def IsReadOnly(self):
        """Is the file Read Only
        @return: bool

        """
        if os.path.exists(self._path):
            return not os.access(self._path, os.R_OK | os.W_OK)
        else:
            return False

    def ResetAll(self):
        """Reset all file attributes"""
        self._handle = None
        self.open = False
        self._path = ''
        self._modtime = 0
        self.last_err = None
        return

    def SetLastError(self, err):
        """Set the last error
        @param err: exception object / msg

        """
        self.last_err = err

    def SetPath(self, path):
        """Set the path of the file
        @param path: absolute path to file

        """
        self._path = fileutil.GetPathFromURI(path)

    def SetModTime(self, mtime):
        """Set the modtime of this file
        @param mtime: long int to set modtime to

        """
        self._modtime = mtime

    def Read(self):
        """Open/Read the file
        @return: string (file contents)

        """
        txt = ''
        if self.DoOpen('rb'):
            try:
                txt = self._handle.read()
            except:
                pass

        return txt

    def Write(self, value):
        """Open/Write the value to disk
        @param value: string

        """
        if self.DoOpen('wb'):
            self._handle.write(value)
            self._handle.close()