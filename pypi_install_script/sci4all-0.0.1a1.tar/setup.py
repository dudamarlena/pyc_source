#!/usr/bin/env python
#
# Copyright (C) 2018 Tore Skaug
#
# This file is part of Sci4All
#
# Sci4All is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sci4All is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Sci4All.  If not, see <https://www.gnu.org/licenses/>.
#

from distutils.core import setup
import os

# Classifiers
cf = ['Development Status :: 2 - Pre-Alpha',
      'Framework :: Jupyter',
      'Intended Audience :: Developers',
      'Intended Audience :: Education',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: '  # continued line ...
      'GNU Lesser General Public License v3 or later (LGPLv3+)',
      'Natural Language :: English',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: Mathematics',
      'Topic :: Software Development :: Libraries :: Python Modules'
      ]

# Packages under ./sci/
packages = []
for dirpath, dirs, files in os.walk('sci'):
    if '__init__.py' in files:
        packages.append(dirpath.replace(os.path.sep, '.'))


if __name__ == '__main__':
    with open('README.md', 'r') as fh:
        ldesc = fh.read()

    _desc = 'Sci4All - scientific toolbox for high school and higher education'
    setup(name='sci4all',
          version='0.0.1a1',
          description=_desc,
          long_description=ldesc,
          provides=['sci4all'],
          author='Tore Skaug',
          author_email='contact@sci4all.org',
          maintainer='Tore Skaug',
          maintainer_email='contact@sci4all.org',
          url='https://www.sci4all.org/',
          packages=packages,
          keywords=['sci4all'],
          classifiers=cf,
          license='GNU Lesser General Public License v3 or later (LGPLv3+)'
          )
