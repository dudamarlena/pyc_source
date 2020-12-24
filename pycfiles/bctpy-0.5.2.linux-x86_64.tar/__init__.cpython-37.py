# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/aestrivex/anaconda3/lib/python3.7/site-packages/bct/__init__.py
# Compiled at: 2020-04-27 14:47:22
# Size of source mod 2**32: 392 bytes
from .algorithms import *
from .utils import *
from .nbs import *
from .version import __version__, __version_info__
from .citations import BCTPY, RUBINOV2010
from .due import due, BibTeX
__citation__ = BCTPY
due.cite((BibTeX(__citation__)), description='Brain Connectivity Toolbox for Python', path='bct')
due.cite((BibTeX(RUBINOV2010)), description='Brain Connectivity Toolbox', path='bct')