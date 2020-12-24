# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rgeda/project/repo/webbpsf/astropy_helpers/astropy_helpers/openmp_helpers.py
# Compiled at: 2019-07-20 17:47:20
# Size of source mod 2**32: 3141 bytes
from __future__ import absolute_import, print_function
import os, sys, glob, tempfile, subprocess
from distutils import log
from distutils.ccompiler import new_compiler
from distutils.sysconfig import customize_compiler
from distutils.errors import CompileError, LinkError
from .setup_helpers import get_compiler_option
__all__ = [
 'add_openmp_flags_if_available']
CCODE = '\n#include <omp.h>\n#include <stdio.h>\nint main(void) {\n  #pragma omp parallel\n  printf("nthreads=%d\\n", omp_get_num_threads());\n  return 0;\n}\n'

def add_openmp_flags_if_available(extension):
    """
    Add OpenMP compilation flags, if available (if not a warning will be
    printed to the console and no flags will be added)

    Returns `True` if the flags were added, `False` otherwise.
    """
    ccompiler = new_compiler()
    customize_compiler(ccompiler)
    tmp_dir = tempfile.mkdtemp()
    start_dir = os.path.abspath('.')
    if get_compiler_option() == 'msvc':
        compile_flag = '-openmp'
        link_flag = ''
    else:
        compile_flag = '-fopenmp'
        link_flag = '-fopenmp'
    try:
        try:
            os.chdir(tmp_dir)
            with open('test_openmp.c', 'w') as (f):
                f.write(CCODE)
            os.mkdir('objects')
            ccompiler.compile(['test_openmp.c'], output_dir='objects', extra_postargs=[compile_flag])
            ccompiler.link_executable((glob.glob(os.path.join('objects', '*' + ccompiler.obj_extension))), 'test_openmp', extra_postargs=[link_flag])
            output = subprocess.check_output('./test_openmp').decode(sys.stdout.encoding or 'utf-8').splitlines()
            if 'nthreads=' in output[0]:
                nthreads = int(output[0].strip().split('=')[1])
                if len(output) == nthreads:
                    using_openmp = True
                else:
                    log.warn('Unexpected number of lines from output of test OpenMP program (output was {0})'.format(output))
                    using_openmp = False
            else:
                log.warn('Unexpected output from test OpenMP program (output was {0})'.format(output))
                using_openmp = False
        except (CompileError, LinkError):
            using_openmp = False

    finally:
        os.chdir(start_dir)

    if using_openmp:
        log.info('Compiling Cython extension with OpenMP support')
        extension.extra_compile_args.append(compile_flag)
        extension.extra_link_args.append(link_flag)
    else:
        log.warn('Cannot compile Cython extension with OpenMP, reverting to non-parallel code')
    return using_openmp