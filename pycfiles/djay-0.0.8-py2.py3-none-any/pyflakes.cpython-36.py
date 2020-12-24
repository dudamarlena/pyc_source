# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/pyflakes/pyflakes/scripts/pyflakes.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 287 bytes
"""
Implementation of the command-line I{pyflakes} tool.
"""
from __future__ import absolute_import
__all__ = [
 'check', 'checkPath', 'checkRecursive', 'iterSourceCode', 'main']
from pyflakes.api import check, checkPath, checkRecursive, iterSourceCode, main