# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/testutils/helpers/auth_providers.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
__all__ = ['AuthProvider']
from contextlib import contextmanager
from sentry.auth import register, unregister

@contextmanager
def AuthProvider(name, cls):
    register(name, cls)
    yield
    unregister(name, cls)