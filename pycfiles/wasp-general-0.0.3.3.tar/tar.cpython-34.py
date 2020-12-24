# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/tar.py
# Compiled at: 2017-12-21 01:59:26
# Size of source mod 2**32: 4275 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import io, os, tarfile, time, pwd, grp
from datetime import datetime

class WDynamicTarArchive(io.BufferedWriter):
    __default_tar_mode__ = int('440', base=8)

    def __init__(self, archive, inside_file_name, patch_header=True, patch_alignment=True, patch_tail=False):
        archive = open(archive, mode='wb', buffering=0) if isinstance(archive, str) is True else archive
        io.BufferedWriter.__init__(self, archive)
        self._WDynamicTarArchive__inside_file_name = inside_file_name
        self._WDynamicTarArchive__patch_header = patch_header
        self._WDynamicTarArchive__patch_alignment = patch_alignment
        self._WDynamicTarArchive__patch_tail = patch_tail
        self._WDynamicTarArchive__bytes_written = 0
        if self._WDynamicTarArchive__patch_header is True:
            self.write(self.tar_header(self.inside_file_name()))

    def inside_file_name(self):
        return self._WDynamicTarArchive__inside_file_name

    def patch_header(self):
        return self._WDynamicTarArchive__patch_header

    def patch_alignment(self):
        return self._WDynamicTarArchive__patch_alignment

    def patch_tail(self):
        return self._WDynamicTarArchive__patch_tail

    def bytes_written(self):
        return self._WDynamicTarArchive__bytes_written

    def write(self, b):
        self._WDynamicTarArchive__bytes_written += len(b)
        return io.BufferedWriter.write(self, b)

    def close(self):
        if self.closed is False:
            self._patch()
        io.BufferedWriter.close(self)

    def alignment_padding(self):
        bytes_written = self.bytes_written()
        if self.patch_header() is True:
            bytes_written -= tarfile.BLOCKSIZE
        return self.block_size(bytes_written) - bytes_written

    def _patch_alignment(self):
        self.write(self.padding(self.alignment_padding()))

    def _patch_tail(self):
        self.write(self.padding(tarfile.BLOCKSIZE * 2))
        bytes_written = self.bytes_written()
        delta = self.record_size(bytes_written) - bytes_written
        self.write(self.padding(delta))

    def _patch_header(self, archive_size):
        tar_header = self.tar_header(self.inside_file_name(), size=archive_size)
        self.seek(-self.bytes_written(), os.SEEK_CUR)
        self.write(tar_header)

    def _patch(self):
        bytes_written = self.bytes_written()
        if self.patch_alignment() is True:
            self._patch_alignment()
        if self.patch_tail():
            self._patch_tail()
        if self.patch_header() is True:
            self._patch_header(bytes_written - tarfile.BLOCKSIZE)

    @classmethod
    def tar_info(cls, name, size=None):
        tar_info = tarfile.TarInfo(name=name)
        if size is not None:
            tar_info.size = size
        tar_info.mtime = time.mktime(datetime.now().timetuple())
        tar_info.mode = cls.__default_tar_mode__
        tar_info.type = tarfile.REGTYPE
        tar_info.uid = os.getuid()
        tar_info.gid = os.getgid()
        tar_info.uname = pwd.getpwuid(tar_info.uid).pw_name
        tar_info.gname = grp.getgrgid(tar_info.gid).gr_name
        return tar_info

    @classmethod
    def tar_header(cls, name, size=None):
        return cls.tar_info(name, size=size).tobuf()

    @classmethod
    def align_size(cls, size, chunk_size):
        result = divmod(size, chunk_size)
        return (result[0] if result[1] == 0 else result[0] + 1) * chunk_size

    @classmethod
    def record_size(cls, size):
        return cls.align_size(size, tarfile.RECORDSIZE)

    @classmethod
    def block_size(cls, size):
        return cls.align_size(size, tarfile.BLOCKSIZE)

    @classmethod
    def padding(cls, padding_size):
        if padding_size > 0:
            return tarfile.NUL * padding_size
        return b''