# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/__init__.py
# Compiled at: 2019-06-26 11:58:00
# Size of source mod 2**32: 222 bytes
"""
Library of useful Python functions and classes.
"""
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions