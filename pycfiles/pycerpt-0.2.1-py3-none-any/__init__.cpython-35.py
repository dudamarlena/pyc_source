# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/cerebro/__init__.py
# Compiled at: 2018-03-08 20:03:41
# Size of source mod 2**32: 228 bytes
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
from cerebro.cdas import context, version