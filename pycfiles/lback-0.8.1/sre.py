# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: sre.pyc
# Compiled at: 2011-03-08 12:43:22
"""This file is only retained for backwards compatibility.
It will be removed in the future.  sre was moved to re in version 2.5.
"""
import warnings
warnings.warn('The sre module is deprecated, please import re.', DeprecationWarning, 2)
from re import *
from re import __all__
from re import _compile