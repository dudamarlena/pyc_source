# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tdm_loader\__init__.py
# Compiled at: 2017-06-26 04:29:26
# Size of source mod 2**32: 218 bytes
import os
from .tdm_loader import *
try:
    with open(os.path.join(os.path.dirname(__file__), 'VERSION'), 'r') as (fobj):
        __version__ = fobj.read().strip()
except IOError:
    __version__ = 'unknown'