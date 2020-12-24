# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/genmechanics/__init__.py
# Compiled at: 2020-03-26 14:17:33
# Size of source mod 2**32: 192 bytes
"""
Created on Wed Nov 16 14:17:10 2016

@author: steven
"""
from .core import *
import pkg_resources
__version__ = pkg_resources.require('genmechanics')[0].version