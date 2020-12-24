# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dinolemma/version.py
# Compiled at: 2020-01-24 17:13:18
# Size of source mod 2**32: 873 bytes
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
__version__ = '0.0.12'
AUTHOR = 'Vanessa Sochat'
AUTHOR_EMAIL = 'vsochat@stanford.edu'
NAME = 'dinolemma'
PACKAGE_URL = 'http://www.github.com/vsoch/dinosaur-dilemma'
KEYWORDS = 'simulation, dinosaur, avocados, pygame'
DESCRIPTION = 'Simulate evolution of dinosaurs and avocado trees'
LICENSE = 'LICENSE'
INSTALL_REQUIRES = (
 (
  'numpy', {'min_version': '1.16.2'}),)
TESTS_REQUIRES = (('pytest', {'min_version': '4.6.2'}),)
GAME_REQUIRES = (('pygame', {'min_version': '1.9.6'}),)
INSTALL_REQUIRES_ALL = INSTALL_REQUIRES + GAME_REQUIRES