# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_select2/cache.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 632 bytes
"""
Shared memory across multiple machines to the heavy AJAX lookups.

Select2 uses django.core.cache_ to share fields across
multiple threads and even machines.

Select2 uses the cache backend defined in the setting
``SELECT2_CACHE_BACKEND`` [default=``default``].

It is advised to always setup a separate cache server for Select2.

.. _django.core.cache: https://docs.djangoproject.com/en/dev/topics/cache/
"""
from __future__ import absolute_import, unicode_literals
from django.core.cache import caches
from .conf import settings
__all__ = ('cache', )
cache = caches[settings.SELECT2_CACHE_BACKEND]