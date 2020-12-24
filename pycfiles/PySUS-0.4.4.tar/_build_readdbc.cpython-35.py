# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fccoelho/Documentos/Projects_software/PySUS/utilities/_build_readdbc.py
# Compiled at: 2016-08-17 12:11:00
# Size of source mod 2**32: 878 bytes
"""
Created on 16/08/16
by fccoelho
license: GPL V3 or Later
"""
import os
from cffi import FFI
ffibuilder = FFI()
PATH = os.path.dirname(__file__)
with open(os.path.join(PATH, 'c-src/dbc2dbf.c'), 'r') as (f):
    ffibuilder.set_source('_readdbc', f.read(), libraries=[
     'c'], sources=[
     os.path.join(PATH, 'c-src/blast.c')], include_dirs=[
     os.path.join(PATH, 'c-src/')])
ffibuilder.cdef('\n    static unsigned inf(void *how, unsigned char **buf);\n    static int outf(void *how, unsigned char *buf, unsigned len);\n    void dbc2dbf(char** input_file, char** output_file);\n    ')
with open(os.path.join(PATH, 'c-src/blast.h')) as (f):
    ffibuilder.cdef(f.read(), override=True)
if __name__ == '__main__':
    ffibuilder.compile(verbose=True)