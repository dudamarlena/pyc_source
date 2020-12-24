# uncompyle6 version 3.7.4
# PyPy Python bytecode 3.2 (3187)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dario/Projects/pysplice/pysplice/__init__.py
# Compiled at: 2015-09-18 14:58:29
from _splice import ffi, lib
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


def testit():
    r, w = mkpipe()
    from urllib.request import urlopen
    u = urlopen('http://arstechnica.com')
    with open('/home/dario/.pythonz/dists/jython-installer-2.7.0.jar', 'rb') as (f1):
        with open('ars', 'wb') as (f2):
            splice(u, None, w, None, 93296)
            splice(u, None, w, None, 93296)
            splice(r, None, f2, 0, 93296)


if __name__ == '__main__':
    testit()