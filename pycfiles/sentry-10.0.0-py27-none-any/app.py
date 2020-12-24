# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/app.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from threading import local
from sentry.utils import redis
from sentry.utils.locking.backends.redis import RedisLockBackend
from sentry.utils.locking.manager import LockManager

class State(local):
    request = None
    data = {}


env = State()
from sentry import search, tsdb
from .buffer import backend as buffer
from .digests import backend as digests
from .nodestore import backend as nodestore
from .quotas import backend as quotas
from .ratelimits import backend as ratelimiter
from sentry.utils.sdk import RavenShim
raven = client = RavenShim()
locks = LockManager(RedisLockBackend(redis.clusters.get('default')))