# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/cerebro/__init__.py
# Compiled at: 2018-05-22 15:24:37
# Size of source mod 2**32: 228 bytes
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
from cerebro.cdas import context, version