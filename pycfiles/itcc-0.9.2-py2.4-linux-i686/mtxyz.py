# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/molecule/mtxyz.py
# Compiled at: 2008-04-20 13:19:45
"""Deal with multi tinker xyz file, such as TINKER .arc file.
"""
__revision__ = '$Rev$'
from itcc.molecule import read

class Mtxyz:
    __module__ = __name__

    def __init__(self, ifile):
        self._ifile = ifile

    def __iter__(self):
        return self

    def next(self):
        try:
            return read.readxyz(self._ifile)
        except:
            raise StopIteration

    def read_mol_as_string(self):
        result = ''
        cur = 0
        need = None
        for line in self._ifile:
            if cur == 0:
                need = int(line.split()[0]) + 1
            result += line
            cur += 1
            if cur == need:
                yield result
                result = ''
                cur = 0
                need = None

        return


def read_mtxyz_frame(ifile, frame_idx):
    assert frame_idx >= 0