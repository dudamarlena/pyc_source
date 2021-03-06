# Copyright (c) 2014, Sven Thiele <sthiele78@gmail.com>
#
# This file is part of precursor.
#
# precursor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# precursor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with precursor.  If not, see <http://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-
from setuptools import setup

                         
setup(
  name             = 'precursor',
  version          = '1.2.4',
  url              = 'http://bioasp.github.io/precursor/',
  license          = 'GPLv3+',
  description      = 'Compute minimal metabolic precursors sets that enable the production of target metabolites.',
  long_description = open('README.md').read(),
  long_description_content_type="text/markdown", 
  author           = 'Sven Thiele',
  author_email     = 'sthiele78@gmail.com',
  packages         = ['__precursor__'],
  package_dir      = {'__precursor__' : 'src'},
  package_data     = {'__precursor__' : ['encodings/*.lp']},
  scripts          = ['precursor.py'],
  install_requires = ['pyasp == 1.4.4']
)

