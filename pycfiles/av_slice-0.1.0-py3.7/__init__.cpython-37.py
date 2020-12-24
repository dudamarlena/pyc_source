# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/av_slice/__init__.py
# Compiled at: 2019-06-11 23:51:07
# Size of source mod 2**32: 248 bytes
"""Top-level package for Silence Remover."""
__author__ = 'Alex Elias'
__email__ = 'alex.88.elias@gmail.com'
__version__ = '0.1.0'
from av_slice.video import remove_sections
from av_slice.audio import quiet_sections