# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpme/version.py
# Compiled at: 2019-12-18 16:06:45
# Size of source mod 2**32: 1563 bytes
"""

Copyright (C) 2017-2020 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
__version__ = '0.0.40'
AUTHOR = 'Vanessa Sochat'
AUTHOR_EMAIL = 'vsochat@stanford.edu'
NAME = 'helpme'
PACKAGE_URL = 'http://www.github.com/researchapps/helpme-client'
KEYWORDS = 'hpc, help, asciinema, questions, answers, client'
DESCRIPTION = 'command line client for helping you out.'
LICENSE = 'LICENSE'
INSTALL_REQUIRES = (
 (
  'requests', {'min_version': '2.18.4'}),)
INSTALL_ASCIINEMA = (
 (
  'asciinema', {'min_version': '2.0.1'}),)
INSTALL_USERVOICE = (('uservoice', {'min_version': '0.0.23'}),)
INSTALL_DISCOURSE = (('pycryptodome', {'min_version': '3.7.2'}),)
INSTALL_ALL = INSTALL_REQUIRES + INSTALL_USERVOICE + INSTALL_DISCOURSE + INSTALL_ASCIINEMA