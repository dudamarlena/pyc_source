# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dario/Projects/pysplice/pysplice/__init__.py
# Compiled at: 2015-09-18 18:10:57
# Size of source mod 2**32: 747 bytes
from pysplice._splice import ffi, lib
import os, errno
from collections import namedtuple
Pipe = namedtuple('Pipe', 'fileno')

def mkpipe():
    readfd, writefd = os.pipe()
    return (Pipe(lambda : readfd), Pipe(lambda : writefd))


def splice(infile, off_in, outfile, off_out, size, flags=0):
    off_in = ffi.NULL if off_in is None else ffi.new('loff_t *', off_in)
    off_out = ffi.NULL if off_out is None else ffi.new('loff_t *', off_out)
    while 1:
        res = lib.splice(infile.fileno(), off_in, outfile.fileno(), off_out, size, flags)
        if res != -1:
            return res
        if ffi.errno != errno.EINTR:
            raise OSError(ffi.errno, os.strerror(ffi.errno))