# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/mffpy/zipfile.py
# Compiled at: 2020-01-29 20:14:20
# Size of source mod 2**32: 2871 bytes
"""
Copyright 2019 Brain Electrophysiology Laboratory Company LLC

Licensed under the ApacheLicense, Version 2.0(the "License");
you may not use this module except in compliance with the License.
You may obtain a copy of the License at:

http: // www.apache.org / licenses / LICENSE - 2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
ANY KIND, either express or implied.
"""
from zipfile import is_zipfile
from zipfile import ZipFile as _ZipFile

class FilePart:
    __doc__ = '`zipfile.ZipFile.open` uses the file pointer of the original `ZipFile`\n    instance: `ZipFile.fp`.  We need `open` to create a separate file pointer\n    to `ZipFile`, that is however confined to the range of the .zip entry we\n    want to open.  This subclass serves this purpose:  it opens a new\n    filepointer `self.fp` and constrains its range between `self.start` and\n    `self.end`'

    def __init__(self, filename: str, start: int, end: int):
        self.start = start
        self.end = end
        self.fp = open(filename, 'rb')
        self.seek(0)

    def close(self):
        if not self.closed:
            self.fp.close()

    @property
    def closed(self):
        return self.fp.closed

    def __del__(self):
        self.close()

    def __enter__(self):
        self.seek(0)
        return self

    def __exit__(self, *args):
        self.close()

    def read(self, n: int=-1) -> bytes:
        nmax = self.end - self.fp.tell()
        n = min(n, nmax)
        if n >= 0:
            return self.fp.read(n)
        else:
            return self.fp.read(nmax)

    def tell(self) -> int:
        return self.fp.tell() - self.start

    def seek(self, pos: int, whence: int=0) -> None:
        if whence == 0:
            self.fp.seek(self.start + pos, whence)
        else:
            if whence == 1:
                self.fp.seek(pos, whence)
            else:
                if whence == 2:
                    self.fp.seek(self.end + pos, 0)
                else:
                    raise ValueError


class ZipFile(_ZipFile):
    __doc__ = 'ZipFile subclass designed to create a new file pointer to the .zip file\n    whenever a subfile is accessed.  Benefit is that we can seek and read in\n    the subfile without having to unpack the whole thing.'

    def __init__(self, filename):
        super().__init__(filename, 'r')
        assert self.compression == 0
        self.filename = filename
        self.file_size = {zi.filename:zi.file_size for zi in self.filelist}

    def open(self, filename):
        with super().open(filename):
            start_pos = self.fp.tell()
        end_pos = start_pos + self.file_size[filename]
        return FilePart(self.filename, start_pos, end_pos)