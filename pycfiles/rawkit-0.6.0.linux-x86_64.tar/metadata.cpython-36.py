# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.6/site-packages/rawkit/metadata.py
# Compiled at: 2015-07-03 22:58:20
# Size of source mod 2**32: 549 bytes
""":mod:`rawkit.metadata` --- Metadata structures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from collections import namedtuple
Orientation = namedtuple('Orientation', [
 'landscape',
 'portrait'])(0, 1)
Metadata = namedtuple('Metadata', [
 'aperture',
 'timestamp',
 'shutter',
 'flash',
 'focal_length',
 'height',
 'iso',
 'make',
 'model',
 'orientation',
 'width'])