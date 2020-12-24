# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/flask_limiter/__init__.py
# Compiled at: 2017-12-12 18:29:44
# Size of source mod 2**32: 221 bytes
"""
Flask-Limiter extension for rate limiting
"""
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
from .errors import RateLimitExceeded
from .extension import Limiter, HEADERS