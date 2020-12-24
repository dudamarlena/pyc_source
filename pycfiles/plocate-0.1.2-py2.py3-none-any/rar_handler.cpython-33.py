# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ploader/rar_handler.py
# Compiled at: 2014-01-06 19:25:51
# Size of source mod 2**32: 856 bytes
import os.path, rarfile
rarfile.NEED_COMMENTS = 0
rarfile.UNICODE_COMMENTS = 1
rarfile.PATH_SEP = '/'

class RAR(object):

    def __init__(self, path, passwd=None):
        self._path = path
        try:
            self._file = rarfile.RarFile(self._path)
            self._passwd = passwd
            self._first_volume = True
            self._have_all_files = True
        except rarfile.NeedFirstVolume:
            self._first_volume = False
            self._have_all_files = True
        except FileNotFoundError:
            self._have_all_files = False

    def is_first_vol(self):
        return self._first_volume

    def all_files_present(self):
        return self._have_all_files

    def extract(self):
        self._file.extractall(path=os.path.dirname(self._path), pwd=self._passwd)

    def list_content(self):
        for f in self._file.infolist():
            print(f.filename, f.file_size, f.volume, f.flags)


def is_rar(fn):
    return rarfile.is_rarfile(fn)