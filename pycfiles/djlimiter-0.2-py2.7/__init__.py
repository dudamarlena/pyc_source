# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djlimiter/__init__.py
# Compiled at: 2015-01-08 15:29:54
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
from .middleware import Limiter
from .decorators import limit, exempt, shared_limit
from .errors import RateLimitExceeded