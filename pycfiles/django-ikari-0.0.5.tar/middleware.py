# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zenobius/Dev/django-apps/django-ikari/ikari/middleware.py
# Compiled at: 2013-08-02 00:10:15
import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.cache import patch_vary_headers
from django.contrib.auth import logout
from . import models
from . import signals
from . import settings
from . import cache
from . import decorators
logger = logging.getLogger(__name__)
logger.addHandler(settings.null_handler)

def get_domain_list(facet='domain'):
    return models.Domain.objects.values_list(facet, flat=True)


def get_domain(query_dict=None):
    return models.Domain.objects.get(**query_dict)


class DomainsMiddleware:

    def process_request(self, request):
        host = request.META.get('HTTP_HOST', None)
        if host is None:
            return
        else:
            if settings.PORT_SUFFIX and host.endswith(settings.PORT_SUFFIX):
                host = host[:-len(settings.PORT_SUFFIX)]
            try:
                if host.endswith(settings.SUBDOMAIN_ROOT):
                    query_dict = {'subdomain': host[:-len(settings.SUBDOMAIN_ROOT)]}
                else:
                    query_dict = {'domain': host}
                domain = cache.get_thing(facet='item', query=host, update=lambda : get_domain(query_dict))
                if settings.CANONICAL_DOMAINS and domain.domain:
                    if str(host) != domain.domain:
                        return HttpResponseRedirect(domain.get_absolute_url())
            except models.Domain.DoesNotExist:
                if host != settings.DEFAULT_DOMAIN:
                    return HttpResponseRedirect(settings.DEFAULT_URL)

            request.domain = domain
            if settings.ACCOUNT_URLCONF:
                request.urlconf = settings.ACCOUNT_URLCONF
            if hasattr(request.user, 'pk') > 0 and request.user.is_authenticated:
                can_access = domain.user_can_access(request.user)
                if not can_access:
                    url = settings.DEFAULT_URL.rstrip('/')
                    if not domain.is_public:
                        url = url + reverse('domains-inactive')
                    logout(request)
                    return HttpResponseRedirect(url)
            for receiver, retval in signals.domain_request.send(sender=request, request=request, domain=domain):
                if isinstance(retval, HttpResponse):
                    return retval

            return

    def process_response(self, request, response):
        if getattr(request, 'urlconf', None):
            patch_vary_headers(response, ('Host', ))
        return response