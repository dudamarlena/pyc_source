# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cfl/ternaris/marv/pycapnp/buildutils/patch.py
__doc__ = 'utils for patching libraries'
import re, sys, os, logging
from .misc import get_output_error
pjoin = os.path.join
LIB_PAT = re.compile('\\s*(.*) \\(compatibility version (\\d+\\.\\d+\\.\\d+), current version (\\d+\\.\\d+\\.\\d+)\\)')

def _get_libs(fname):
    rc, so, se = get_output_error(['otool', '-L', fname])
    if rc:
        logging.error('otool -L %s failed: %r' % (fname, se))
        return
    for line in so.splitlines()[1:]:
        m = LIB_PAT.match(line)
        if m:
            yield m.group(1)


def _find_library(lib, path):
    """Find a library"""
    for d in path[::-1]:
        real_lib = os.path.join(d, lib)
        if os.path.exists(real_lib):
            return real_lib


def _install_name_change(fname, lib, real_lib):
    rc, so, se = get_output_error(['install_name_tool', '-change', lib, real_lib, fname])
    if rc:
        logging.error("Couldn't update load path: %s", se)


def patch_lib_paths(fname, library_dirs):
    """Load any weakly-defined libraries from their real location
    
    (only on OS X)
    
    - Find libraries with `otool -L`
    - Update with `install_name_tool -change`
    """
    if sys.platform != 'darwin':
        return
    libs = _get_libs(fname)
    for lib in libs:
        if not lib.startswith(('@', '/')):
            real_lib = _find_library(lib, library_dirs)
            if real_lib:
                _install_name_change(fname, lib, real_lib)


__all__ = [
 'patch_lib_paths']