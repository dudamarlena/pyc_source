# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\faster_rcnn\setup_linux.py
# Compiled at: 2019-12-31 04:09:02
# Size of source mod 2**32: 2928 bytes
import os, shutil
from distutils.core import setup
from distutils.extension import Extension
import numpy as np
from Cython.Distutils import build_ext
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
    self.src_extensions.append('.cu')
    default_compiler_so = self.compiler_so
    super = self._compile

    def _compile(obj, src, ext, cc_args, extra_postargs, pp_opts):
        print(extra_postargs)
        if os.path.splitext(src)[1] == '.cu':
            self.set_executable('compiler_so', CUDA['nvcc'])
            postargs = extra_postargs['nvcc']
        else:
            postargs = extra_postargs['gcc']
        super(obj, src, ext, cc_args, postargs, pp_opts)
        self.compiler_so = default_compiler_so

    self._compile = _compile


class custom_build_ext(build_ext):

    def build_extensions(self):
        customize_compiler_for_nvcc(self.compiler)
        build_ext.build_extensions(self)
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        build_path = os.path.join(curr_dir, 'build')
        if os.path.exists(build_path):
            shutil.rmtree(build_path)


ext_modules = [
 Extension('utils.cython_bbox',
   [
  'utils/bbox.pyx'],
   extra_compile_args={'gcc': ['-Wno-cpp', '-Wno-unused-function']},
   include_dirs=[
  numpy_include])]
setup(name='tf_faster_rcnn',
  ext_modules=ext_modules,
  cmdclass={'build_ext': custom_build_ext})