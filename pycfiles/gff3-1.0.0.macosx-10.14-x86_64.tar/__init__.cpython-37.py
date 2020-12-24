# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/gff3/__init__.py
# Compiled at: 2018-08-02 12:38:50
# Size of source mod 2**32: 451 bytes
"""Manipulate genomic features and validate the syntax and reference sequence of your GFF3 files"""
from __future__ import absolute_import
from .gff3 import Gff3
__all__ = [
 'Gff3']
VERSION = (0, 3, 0)
__version__ = '.'.join(map(str, VERSION[0:3])) + ''.join(VERSION[3:])
__author__ = 'Han Lin'
__email__ = 'hotdogee [at] gmail [dot] com'
__homepage__ = 'https://github.com/hotdogee/gff3-py'
__docformat__ = 'restructuredtext'