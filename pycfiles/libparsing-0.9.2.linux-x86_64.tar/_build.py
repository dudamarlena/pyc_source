# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/libparsing/_build.py
# Compiled at: 2016-11-21 11:00:05
import cffi, glob, re
from os.path import join, dirname, abspath
BASE = dirname(abspath(__file__))
H_SOURCE = open(join(BASE, '_libparsing.h')).read()
C_SOURCE = open(join(BASE, '_libparsing.c')).read()
FFI_SOURCE = open(join(BASE, '_libparsing.ffi')).read()
ffibuilder = cffi.FFI()
ffibuilder.set_source('libparsing._libparsing', H_SOURCE + C_SOURCE, extra_link_args=['-Wl,-lpcre,--export-dynamic'])
ffibuilder.cdef(FFI_SOURCE)
ffibuilder.embedding_init_code('\nfrom my_plugin import ffi\n@ffi.def_extern()\ndef module_init():\n\tpass\n')
ffibuilder.compile(target='src/python/_libparsing.*', verbose=False, tmpdir=join(BASE, 'build'))
if __name__ == '__main__':
    import sys, shutil
    args = sys.argv[1:]