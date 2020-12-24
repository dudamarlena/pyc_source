# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/aaronmeurer/Documents/sphinx-math-dollar/build/lib/sphinx_math_dollar/__init__.py
# Compiled at: 2019-09-17 19:56:44
# Size of source mod 2**32: 233 bytes
from .math_dollar import split_dollars
from .extension import setup, NODE_BLACKLIST
__all__ = ['split_dollars', 'setup', 'NODE_BLACKLIST']
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions