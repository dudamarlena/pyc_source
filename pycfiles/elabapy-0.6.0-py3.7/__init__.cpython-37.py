# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/elabapy/__init__.py
# Compiled at: 2020-05-07 20:18:48
# Size of source mod 2**32: 317 bytes
"""A python module to interact with elabftw API"""
__version__ = '0.6.0'
__author__ = 'Nicolas CARPi'
__author_email__ = 'nico-git@deltablot.email'
__license__ = 'GPL v3'
__copyright__ = 'Copyright (©) 2017 Nicolas CARPi'
from .baseapi import Error, SetupError
from .Manager import Manager