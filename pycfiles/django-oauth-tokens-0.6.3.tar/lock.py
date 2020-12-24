# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-oauth-tokens/oauth_tokens/lock.py
# Compiled at: 2015-11-01 17:30:22
import distributedlock
from django.core.cache import get_cache
distributedlock.DEFAULT_TIMEOUT = 300
distributedlock.DEFAULT_MEMCACHED_CLIENT = get_cache('default')
from distributedlock import distributedlock, LockNotAcquiredError