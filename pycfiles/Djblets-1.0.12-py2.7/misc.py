# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/misc.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import warnings
from djblets.cache.backend import cache_memoize, make_cache_key
from djblets.cache.serials import generate_ajax_serial, generate_cache_serials, generate_locale_serial, generate_media_serial
from djblets.db.query import get_object_or_none
from djblets.deprecation import RemovedInDjblets20Warning
from djblets.urls.patterns import never_cache_patterns
warnings.warn(b'djblets.util.misc is deprecated', RemovedInDjblets20Warning)
__all__ = [
 b'cache_memoize',
 b'generate_ajax_serial',
 b'generate_cache_serials',
 b'generate_locale_serial',
 b'generate_media_serial',
 b'get_object_or_none',
 b'make_cache_key',
 b'never_cache_patterns']