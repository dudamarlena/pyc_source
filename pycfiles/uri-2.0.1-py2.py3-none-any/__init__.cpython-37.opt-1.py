# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /uri/__init__.py
# Compiled at: 2018-10-22 09:58:17
# Size of source mod 2**32: 389 bytes
"""A type to represent, query, and manipulate a Uniform Resource Identifier."""
from .release import version as __version__
from .compat import Path
from .bucket import Bucket
from .qso import QSO
from .uri import URI
__all__ = [
 'Path',
 'Bucket',
 'QSO',
 'URI']