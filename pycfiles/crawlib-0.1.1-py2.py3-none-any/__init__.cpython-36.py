# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/__init__.py
# Compiled at: 2019-12-30 22:32:03
# Size of source mod 2**32: 1599 bytes
"""
tool set for crawler project.
"""
from ._version import __version__
__short_description__ = 'tool set for crawler project.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    import scrapy
    _has_scrapy = True
except ImportError:
    _has_scrapy = False

try:
    from .status import Status, StatusDetail
except ImportError:
    pass

try:
    from .middleware.url_builder import BaseUrlBuilder
except ImportError:
    pass

try:
    from .decorator import resolve_arg
except ImportError:
    pass

try:
    from .decode import decoder
except ImportError:
    pass

try:
    from .entity import RelationshipConfig, Relationship, ParseResult
except ImportError:
    pass

try:
    from .entity import MongodbEntity, MongodbEntitySingleStatus
except ImportError:
    pass

try:
    from .entity import SqlEntity, SqlEntitySingleStatus, Base as SqlDeclarativeBase
except ImportError:
    pass

try:
    from .time_util import epoch, utc_now, x_seconds_before_now, x_seconds_after_now
except ImportError:
    pass

try:
    from .cache import create_cache, create_cache_here
    from .cached_request import CachedRequest
except ImportError:
    pass

try:
    from . import exc
except ImportError:
    pass