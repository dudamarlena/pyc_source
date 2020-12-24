# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c:\users\luc_t_000\projects\freepybox\freepybox\api\fsnav.py
# Compiled at: 2018-03-09 16:37:27
# Size of source mod 2**32: 1206 bytes
from .fs import Fs
import logging, os
logger = logging.getLogger(__name__)

class Fsnav:

    def __init__(self, access):
        self._fs = Fs(access)
        self._path = '/'

    def pwd(self):
        """
        Print working directory
        """
        print(self._path)

    def cd(self, path):
        """
        Change directory
        """
        norm_path = os.path.normpath(path)
        if norm_path == '.':
            pass
        else:
            if norm_path == '..':
                self._path = os.path.dirname(self._path)
            else:
                if self._path_exists(path):
                    self._path = os.path.join(self._path, path)
                else:
                    logger.error('{0} does not exist'.format(os.path.join(self._path, path)))

    def _path_exists(self, path):
        """
        Return True if the path exists
        """
        try:
            self._fs.get_file_info(os.path.join(self._path, path))
            return True
        except:
            return False

    def ls(self):
        """
        list directory
        """
        for i in self._fs.list_file(self._path):
            print(i['name'])