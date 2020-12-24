from __future__ import absolute_import, division, print_function

import io
import os
import re
import sys

from setuptools import find_packages, setup

# cf.
# https://packaging.python.org/guides/single-sourcing-package-version/#single-sourcing-the-version

if sys.version_info < (2,7):
  sys.exit('Sorry, Python < 2.7 is not supported')

setup(name='libtbx',
      description='cctbx library toolbox',
      url='https://github.com/cctbx/cctbx_project',
      author='Markus Gerstel',
      author_email='scientificsoftware@diamond.ac.uk',
      version="0.0.1",
      packages=find_packages(),
      license='BSD',
      classifiers = [
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ]
     )
