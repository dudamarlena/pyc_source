# setup.py

from distutils.core import setup

import sys
from Cython.Build import cythonize
from os.path import join
import numpy
import os

source_path = ''

if sys.argv[-1] == 'build':
    os.system("python setup.py build_ext --inplace")
    source_path = 'safeu/data_quality'


setup(
    name='slp_tools',
    ext_modules=cythonize(join(source_path, 'slp_tools.pyx')),
    include_dirs=[numpy.get_include()]
)
