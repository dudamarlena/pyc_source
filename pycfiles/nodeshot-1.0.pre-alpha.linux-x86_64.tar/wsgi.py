# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/conf/wsgi.py
# Compiled at: 2014-10-10 10:57:04
from django.conf import settings
if getattr(settings, 'RAVEN_CONFIG', {}):
    from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
    from django.core.handlers.wsgi import WSGIHandler
    application = Sentry(WSGIHandler())
else:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()