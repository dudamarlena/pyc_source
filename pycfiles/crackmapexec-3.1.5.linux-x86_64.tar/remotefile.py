# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/remotefile.py
# Compiled at: 2016-12-29 01:49:52
from impacket.smb3structs import FILE_READ_DATA, FILE_WRITE_DATA

class RemoteFile:

    def __init__(self, smbConnection, fileName, share='ADMIN$', access=FILE_READ_DATA | FILE_WRITE_DATA):
        self.__smbConnection = smbConnection
        self.__share = share
        self.__access = access
        self.__fileName = fileName
        self.__tid = self.__smbConnection.connectTree(share)
        self.__fid = None
        self.__currentOffset = 0
        return

    def open(self):
        self.__fid = self.__smbConnection.openFile(self.__tid, self.__fileName, desiredAccess=self.__access)

    def seek(self, offset, whence):
        if whence == 0:
            self.__currentOffset = offset

    def read(self, bytesToRead):
        if bytesToRead > 0:
            data = self.__smbConnection.readFile(self.__tid, self.__fid, self.__currentOffset, bytesToRead)
            self.__currentOffset += len(data)
            return data
        return ''

    def close(self):
        if self.__fid is not None:
            self.__smbConnection.closeFile(self.__tid, self.__fid)
            self.__fid = None
        return

    def delete(self):
        self.__smbConnection.deleteFile(self.__share, self.__fileName)

    def tell(self):
        return self.__currentOffset

    def __str__(self):
        return ('\\\\{}\\{}\\{}').format(self.__smbConnection.getRemoteHost(), self.__share, self.__fileName)