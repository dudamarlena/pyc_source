# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /cygdrive/c/Users/Nad/oneline/oneline/lib/greenlet/my_build_ext.py
# Compiled at: 2014-08-08 03:08:52
import sys, os, shutil
from distutils.command.build_ext import build_ext as _build_ext

def symlink_or_copy(src, dst):
    if hasattr(os, 'symlink'):
        try:
            os.symlink(src, dst)
            return
        except OSError:
            pass
        except NotImplementedError:
            pass

    shutil.copyfile(src, dst)


class build_ext(_build_ext):
    """Command for building extensions

    Prepends library directory to sys.path on normal builds (for tests).
    Otherwise it forces a non-inplace build and symlinks libraries instead.
    """

    def initialize_options(self):
        self.my_inplace = None
        _build_ext.initialize_options(self)
        return

    def finalize_options(self):
        if self.my_inplace is None:
            self.my_inplace = self.inplace
            self.inplace = 0
        _build_ext.finalize_options(self)
        return

    def build_extension(self, ext):
        _build_ext.build_extension(self, ext)
        if not self.my_inplace:
            build_lib = os.path.abspath(self.build_lib)
            if build_lib not in sys.path:
                sys.path.insert(0, build_lib)
            return
        filename = self.get_ext_filename(ext.name)
        build_path = os.path.abspath(os.path.join(self.build_lib, filename))
        src_path = os.path.abspath(filename)
        if build_path != src_path:
            try:
                os.unlink(src_path)
            except OSError:
                pass

            if self.verbose:
                sys.stderr.write('Linking %s to %s\n' % (build_path, src_path))
            symlink_or_copy(build_path, src_path)