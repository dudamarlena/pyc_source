# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\PyCharm Projects\NCryptoClient\NCryptoClient\Utils\client_file_manager.py
# Compiled at: 2018-04-19 15:37:38
# Size of source mod 2**32: 2701 bytes
"""
File manager for the client application. Since we need out application to work with a
single instance of the file manager, we inherit it from Singleton metaclass.
"""
import os
from NCryptoTools.Tools.file_manager import IniFileManager
from NCryptoTools.Tools.meta_singleton import Singleton

class ClientFileManager(metaclass=Singleton):
    __doc__ = '\n    Class for the client file manager.\n    '

    def __init__(self):
        """
        Constructor. Being called only in case of non-existence of objects of this type,
        otherwise a reference to the existing object will be returned.
        """
        self._instance = IniFileManager()
        current_path = os.path.abspath(__file__)
        current_path_tokens = current_path.split('\\')
        pos = current_path_tokens.index('ClientApp')
        self._autoexec_path = '\\'.join(current_path_tokens[0:pos + 1]) + '\\Config\\autoexec.ini'
        self._instance.add_file(self._autoexec_path, 'w', 'utf-8')
        self._autoexec_copy_path = self._instance.make_copy(self._autoexec_path)
        self._instance.add_file(self._autoexec_copy_path, 'r', 'utf-8')
        self._instance.open_file(self._autoexec_path)
        self._instance.open_file(self._autoexec_copy_path)
        self._instance.read_to_buffer(self._autoexec_copy_path)

    @property
    def instance(self):
        """
        Getter. Returns instance of the file manager.
        @return: instance of the file manager.
        """
        return self._instance

    @property
    def autoexec_path(self):
        """
        Getter. Returns an absolute path to the autoexec.ini.
        @return: absolute path to the autoexec.ini.
        """
        return self._autoexec_path

    @property
    def autoexec_copy_path(self):
        """
        Getter. Returns an absolute path to the copy of autoexec.ini.
        @return: absolute path to the copy of autoexec.ini.
        """
        return self._autoexec_copy_path

    def save_changes(self):
        """
        Rewires data from the temporary file to the original file. The temporary
        file is being deleted afterwards. Usually this function executes before the
        closing of the application.
        @return:
        """
        self._instance.copy_buffer(self._autoexec_copy_path, self._autoexec_path)
        self._instance.write_from_buffer(self._autoexec_path)
        self._instance.delete_file(self._autoexec_copy_path)