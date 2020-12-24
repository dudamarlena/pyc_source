# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/utils/windows.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 811 bytes
import sys
if sys.platform != 'win32':
    raise ImportError('This module should not be imported on non `win32` platforms')
import win32file, pywintypes

class NamedPipe:

    def __init__(self, ipc_path):
        try:
            self.handle = win32file.CreateFile(ipc_path, win32file.GENERIC_READ | win32file.GENERIC_WRITE, 0, None, win32file.OPEN_EXISTING, 0, None)
        except pywintypes.error as err:
            raise IOError(err)

    def recv(self, max_length):
        err, data = win32file.ReadFile(self.handle, max_length)
        if err:
            raise IOError(err)
        return data

    def sendall(self, data):
        return win32file.WriteFile(self.handle, data)

    def close(self):
        self.handle.close()