# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/ome/omero-fpbioimage/omero_fpbioimage/version.py
# Compiled at: 2020-01-13 09:06:30
# Size of source mod 2**32: 930 bytes
from .utils import get_version
VERSION = (0, 4, 0)
__version__ = get_version(VERSION)