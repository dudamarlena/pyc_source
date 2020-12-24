# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\faster_rcnn\setup_win.py
# Compiled at: 2019-12-31 04:09:02
# Size of source mod 2**32: 2932 bytes
import numpy as np, os
from setuptools import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
nvcc_bin = 'nvcc.exe'
lib_dir = 'lib/x64'
try:
    numpy_include = np.get_include()
except AttributeError:
    numpy_include = np.get_numpy_include()

def customize_compiler_for_nvcc(self):
    """inject deep into distutils to customize how the dispatch
    to gcc/nvcc works.
    If you subclass UnixCCompiler, it's not trivial to get your subclass
    injected in, and still have the right customizations (i.e.
    distutils.sysconfig.customize_compiler) run on it. So instead of going
    the OO route, I have this. Note, it's kindof like a wierd functional
    subclassing going on."""
    super = self.compile

    def compile(sources, output_dir=None, macros=None, include_dirs=None, debug=0, extra_preargs=None, extra_postargs=None, depends=None):
        postfix = os.path.splitext(sources[0])[1]
        if postfix == '.cu':
            postargs = extra_postargs['nvcc']
        else:
            postargs = extra_postargs['gcc']
        return super(sources, output_dir, macros, include_dirs, debug, extra_preargs, postargs, depends)

    self.compile = compile


class custom_build_ext(build_ext):

    def build_extensions(self):
        customize_compiler_for_nvcc(self.compiler)
        build_ext.build_extensions(self)


ext_modules = [
 Extension('utils.cython_bbox',
   sources=[
  'utils\\bbox.pyx'],
   extra_compile_args={'gcc': []},
   include_dirs=[
  numpy_include])]
setup(name='fast_rcnn',
  ext_modules=ext_modules,
  cmdclass={'build_ext': custom_build_ext})