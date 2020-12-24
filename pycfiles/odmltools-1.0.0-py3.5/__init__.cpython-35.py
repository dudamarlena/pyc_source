# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odmltools/__init__.py
# Compiled at: 2020-02-17 07:41:52
# Size of source mod 2**32: 380 bytes
import warnings
from sys import version_info as python_version
from .info import VERSION
if python_version.major < 3 or python_version.major == 3 and python_version.minor < 6:
    msg = "The '%s' package is not tested with your Python version. " % __name__
    msg += 'Please consider upgrading to the latest Python distribution.'
    warnings.warn(msg)
__version__ = VERSION