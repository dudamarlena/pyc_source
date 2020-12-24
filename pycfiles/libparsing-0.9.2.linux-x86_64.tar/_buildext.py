# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/libparsing/_buildext.py
# Compiled at: 2017-03-27 15:15:29
import cffi, glob, re, tempfile, sys, os, shutil
from os.path import join, dirname, abspath
__doc__ = '\nBuilds a native CFFI version of libparsing using the sources included in the\nmodule.\n'
NAME = '_libparsing'
BASE = dirname(abspath(__file__))
H_SOURCE = open(join(BASE, NAME + '.h')).read()
C_SOURCE = open(join(BASE, NAME + '.c')).read()
FFI_SOURCE = open(join(BASE, NAME + '.ffi')).read()
PY_VERSION = ('{0}_{1}_{2}').format(sys.version_info.major, sys.version_info.minor, sys.version.rsplit('[', 1)[(-1)].split()[0].lower())
FFI_BUILDER = None

def name():
    """Returns the name of the Python module to be built"""
    return ('{0}py{1}').format(NAME, PY_VERSION)


def filename(ext):
    """Returns the filename of the Python module to be built"""
    return ('{0}py{1}.{2}').format(NAME, PY_VERSION, ext)


def builder():
    if FFI_BUILDER:
        return FFI_BUILDER
    ffibuilder = cffi.FFI()
    ffibuilder.set_source(('{0}').format(name()), H_SOURCE + C_SOURCE, extra_link_args=[
     '-Wl,-lpcre,-Ofast,--export-dynamic'])
    ffibuilder.cdef(FFI_SOURCE)
    ffibuilder.embedding_init_code(('\n\tfrom {0} import ffi\n\t@ffi.def_extern()\n\tdef module_init():\n\t\tpass\n\t').format(name()))
    return ffibuilder


def build(path=BASE):
    """Builds a native Python module/extension using CFFI. The extension will
        be available at `{base}/{name}py{version}.{so|dylib|dll}`."""
    ffibuilder = builder()
    mod_path = dirname(abspath(__file__))
    build_path = tempfile.mkdtemp()
    ext = ffibuilder.compile(verbose=False, tmpdir=build_path)
    dest = os.path.join(path, os.path.basename(ext))
    shutil.move(ext, dest)
    for p in glob.glob(build_path + '/*.*'):
        os.unlink(p)

    os.rmdir(build_path)
    return dest


FFI_BUILDER = builder()
if __name__ == '__main__':
    args = sys.argv[1:]
    build()