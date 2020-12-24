# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/testutils/helpers/options.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
__all__ = ['override_options']
from django.test.utils import override_settings
from contextlib import contextmanager
from mock import patch

@contextmanager
def override_options(options):
    """
    A context manager for overriding specific configuration
    Options.
    """
    from django.conf import settings
    from sentry.options import default_manager
    wrapped = default_manager.store.get

    def new_get(key, **kwargs):
        try:
            return options[key.name]
        except KeyError:
            return wrapped(key, **kwargs)

    new_options = settings.SENTRY_OPTIONS.copy()
    new_options.update(options)
    with override_settings(SENTRY_OPTIONS=new_options):
        with patch.object(default_manager.store, 'get', side_effect=new_get):
            yield