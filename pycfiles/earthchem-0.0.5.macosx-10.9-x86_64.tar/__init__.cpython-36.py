# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jess/.local/conda/lib/python3.6/site-packages/earthchem/__init__.py
# Compiled at: 2018-06-24 21:43:54
# Size of source mod 2**32: 213 bytes
from . import documentation, query, validation, transform, geochem, plot
from .query import Query
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions