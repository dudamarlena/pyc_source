# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solstice/core/assetfile.py
# Compiled at: 2020-03-08 13:23:53
# Size of source mod 2**32: 8364 bytes
"""
Module that contains implementations for the different asset files supported by Solstice
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import os
from tpDcc.libs.python import path as path_utils
import tpDcc as tp