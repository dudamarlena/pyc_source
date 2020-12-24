# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swapsha96/mtp/MiraPy/build/lib/mirapy/__init__.py
# Compiled at: 2019-05-03 11:14:15
# Size of source mod 2**32: 914 bytes
from ._astropy_init import *
import sys
__minimum_python_version__ = '3.5'

class UnsupportedPythonError(Exception):
    pass


if sys.version_info < tuple(int(val) for val in __minimum_python_version__.split('.')):
    raise UnsupportedPythonError('mirapy does not support Python < {}'.format(__minimum_python_version__))
if not _ASTROPY_SETUP_:
    from mirapy.fitting import *