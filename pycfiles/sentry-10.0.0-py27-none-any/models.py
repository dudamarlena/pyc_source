# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/tagstore/models.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
backends = []
if settings.SENTRY_TAGSTORE == 'sentry.utils.services.ServiceDelegator':
    backends = [ backend['path'] for backend in settings.SENTRY_TAGSTORE_OPTIONS.get('backends', {}).values() ]
else:
    if settings.SENTRY_TAGSTORE.startswith('sentry.tagstore.multi'):
        backends = [ backend[0] for backend in settings.SENTRY_TAGSTORE_OPTIONS.get('backends', []) ]
    else:
        backends = [
         settings.SENTRY_TAGSTORE]
    if not len(backends) > 0:
        raise ImproperlyConfigured('One or more tagstore backend(s) must be specified')
    prefix_map = {'sentry.tagstore.legacy': 'sentry.tagstore.legacy', 
       'sentry.tagstore.v2': 'sentry.tagstore.v2', 
       'sentry.tagstore.snuba': 'sentry.tagstore.v2'}
    for i, backend in enumerate(backends):
        for prefix, path in prefix_map.items():
            if backend.startswith(prefix):
                models = __import__(path, globals(), locals(), ['models'], level=0).models
                if i == 0:
                    if getattr(models, '__all__', None) is not None:

                        def predicate(name):
                            return name in models.__all__


                    else:

                        def predicate(name):
                            return not name.startswith('_')


                    locals().update({k:v for k, v in vars(models).items() if predicate(k) if predicate(k)})
                break
        else:
            raise ImproperlyConfigured("Found unknown tagstore backend '%s'" % backend)