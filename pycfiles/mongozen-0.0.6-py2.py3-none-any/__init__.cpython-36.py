# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zencity/clones/mongozen/mongozen/__init__.py
# Compiled at: 2018-02-12 03:02:20
# Size of source mod 2**32: 825 bytes
"""Enhance MongoDB for Python dynamic shells and scripts."""
import sys
try:
    import warnings
    from IPython.utils.shimmodule import ShimWarning
    warnings.simplefilter('ignore', ShimWarning)
except ImportError:
    pass

try:
    del ShimWarning
except NameError:
    pass

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
import mongozen.matchop, mongozen.queries, mongozen.util
for name in ('sys', 'warnings', 'constants', 'name', 'mongozen'):
    try:
        globals().pop(name)
    except KeyError:
        pass

try:
    del name
except NameError:
    pass