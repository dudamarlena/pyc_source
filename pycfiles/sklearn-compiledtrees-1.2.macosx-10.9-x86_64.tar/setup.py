# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tulloch/.virtualenvs/sklearn-dev/lib/python2.7/site-packages/compiledtrees/setup.py
# Compiled at: 2014-04-03 08:28:07
import os, numpy
from numpy.distutils.misc_util import Configuration

def configuration(parent_package='', top_path=None):
    config = Configuration('compiledtrees', parent_package, top_path)
    libraries = []
    if os.name == 'posix':
        libraries.append('m')
    config.add_extension('_compiled', sources=[
     '_compiled.c'], include_dirs=[
     numpy.get_include()], libraries=libraries, extra_compile_args=[
     '-O3', '-Wno-unused-function'])
    config.add_subpackage('tests')
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())