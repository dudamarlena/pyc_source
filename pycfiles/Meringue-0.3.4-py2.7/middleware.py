# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/meringue/middleware.py
# Compiled at: 2015-08-17 17:37:49
import re
from django.conf import settings
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
hosts_middleware = 'django_hosts.middleware.HostsMiddleware'
site_middleware = 'meringue.middleware.SiteMiddleware'

class SiteMiddleware:
    """
        Подставляет SITE_ID и SITE_NAME при запросе, используется при
    связке с django-hosts
    """

    def process_request(self, request):
        middlewares = list(settings.MIDDLEWARE_CLASSES)
        if middlewares.index(hosts_middleware) > middlewares.index(site_middleware):
            raise ImproperlyConfigured('The django_hosts and simplemiddlewares are in the wrong order. Make sure %r comes before %r in theMIDDLEWARE_CLASSES setting.' % (hosts_middleware, site_id_middleware))
        r = '^(.[^:]+)'
        host = re.findall(r, request.get_host())[0]
        site = get_object_or_404(Site, domain=host)
        settings.SITE_ID = site.id
        settings.SITE_NAME = site.name