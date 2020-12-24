# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/hiro/__init__.py
# Compiled at: 2019-10-04 00:47:03
# Size of source mod 2**32: 163 bytes
"""
time manipulation utilities for python
"""
from .core import run_async, run_sync
from .core import Timeline
__all__ = [
 'run_async', 'run_sync', 'Timeline']