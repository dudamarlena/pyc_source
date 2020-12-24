# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lsbardel/workspace/python-stdnet/extensions/setup.py
# Compiled at: 2013-07-02 02:26:21
import os, sys
from distutils.core import setup
from distutils.extension import Extension
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError
from Cython.Distutils import build_ext
from Cython.Build import cythonize
try:
    import numpy
    include_dirs = [
     numpy.get_include()]
except ImportError:
    include_dirs = []

ext_errors = (
 CCompilerError, DistutilsExecError, DistutilsPlatformError)
if sys.platform == 'win32' and sys.version_info > (2, 6):
    ext_errors += (IOError,)

class BuildFailed(Exception):

    def __init__(self, msg=None):
        if not msg:
            msg = str(sys.exc_info()[1])
        self.msg = msg


class tolerant_build_ext(build_ext):

    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError:
            raise BuildFailed

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except ext_errors:
            raise BuildFailed
        except ValueError:
            if "'path'" in str(sys.exc_info()[1]):
                raise BuildFailed
            raise


lib_path = os.path.dirname(__file__)
extra_compile_args = []
extension = Extension('stdnet.backends.redisb.cparser', [
 os.path.join(lib_path, 'src', 'cparser.pyx')], language='c++', include_dirs=include_dirs)
include_dirs.append(os.path.join(lib_path, 'src'))
libparams = {'ext_modules': cythonize(extension), 
   'cmdclass': {'build_ext': tolerant_build_ext}, 'include_dirs': include_dirs}