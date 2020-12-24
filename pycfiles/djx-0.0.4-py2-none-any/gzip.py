# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/views/decorators/gzip.py
# Compiled at: 2019-02-14 00:35:17
from django.middleware.gzip import GZipMiddleware
from django.utils.decorators import decorator_from_middleware
gzip_page = decorator_from_middleware(GZipMiddleware)
gzip_page.__doc__ = 'Decorator for views that gzips pages if the client supports it.'