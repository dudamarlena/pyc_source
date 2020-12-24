# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alanjds/src/git/drf-nested-routers/rest_framework_nested/routers.py
# Compiled at: 2018-02-17 10:11:44
# Size of source mod 2**32: 4917 bytes
"""
Routers for nested resources.

Example:

    # urls.py

    from rest_framework_nested import routers

    router = routers.SimpleRouter()
    router.register(r'domains', DomainViewSet)

    domains_router = routers.NestedSimpleRouter(router, r'domains', lookup='domain')
    domains_router.register(r'nameservers', NameserverViewSet)

    url_patterns = patterns('',
        url(r'^', include(router.urls)),
            url(r'^', include(domains_router.urls)),
            )

        router = routers.DefaultRouter()
        router.register('users', UserViewSet, 'user')
        router.register('accounts', AccountViewSet, 'account')

        urlpatterns = router.urls
"""
from __future__ import unicode_literals
import sys, re
from rest_framework.routers import SimpleRouter, DefaultRouter
if sys.version_info[0] < 3:
    IDENTIFIER_REGEX = re.compile('^[^\\d\\W]\\w*$')
else:
    IDENTIFIER_REGEX = re.compile('^[^\\d\\W]\\w*$', re.UNICODE)

class LookupMixin(object):
    __doc__ = '\n    Deprecated.\n\n    No method override is needed since Django Rest Framework 2.4.\n    '


class NestedMixin(object):

    def __init__(self, parent_router, parent_prefix, *args, **kwargs):
        self.parent_router = parent_router
        self.parent_prefix = parent_prefix
        self.nest_count = getattr(parent_router, 'nest_count', 0) + 1
        self.nest_prefix = kwargs.pop('lookup', 'nested_%i' % self.nest_count) + '_'
        (super(NestedMixin, self).__init__)(*args, **kwargs)
        parent_registry = [registered for registered in self.parent_router.registry if registered[0] == self.parent_prefix]
        try:
            parent_registry = parent_registry[0]
            parent_prefix, parent_viewset, parent_basename = parent_registry
        except:
            raise RuntimeError('parent registered resource not found')

        self.check_valid_name(self.nest_prefix)
        nested_routes = []
        parent_lookup_regex = parent_router.get_lookup_regex(parent_viewset, self.nest_prefix)
        self.parent_regex = '{parent_prefix}/{parent_lookup_regex}/'.format(parent_prefix=parent_prefix,
          parent_lookup_regex=parent_lookup_regex)
        if not self.parent_prefix:
            if self.parent_regex[0] == '/':
                self.parent_regex = self.parent_regex[1:]
        if hasattr(parent_router, 'parent_regex'):
            self.parent_regex = parent_router.parent_regex + self.parent_regex
        for route in self.routes:
            route_contents = route._asdict()
            escaped_parent_regex = self.parent_regex.replace('{', '{{').replace('}', '}}')
            route_contents['url'] = route.url.replace('^', '^' + escaped_parent_regex)
            nested_routes.append((type(route))(**route_contents))

        self.routes = nested_routes

    def check_valid_name(self, value):
        if IDENTIFIER_REGEX.match(value) is None:
            raise ValueError("lookup argument '{}' needs to be valid python identifier".format(value))


class NestedSimpleRouter(NestedMixin, SimpleRouter):
    __doc__ = " Create a NestedSimpleRouter nested within `parent_router`\n    Args:\n\n    parent_router: Parent router. Maybe be a SimpleRouter or another nested\n        router.\n\n    parent_prefix: The url prefix within parent_router under which the\n        routes from this router should be nested.\n\n    lookup:\n        The regex variable that matches an instance of the parent-resource\n        will be called '<lookup>_<parent-viewset.lookup_field>'\n        In the example above, lookup=domain and the parent viewset looks up\n        on 'pk' so the parent lookup regex will be 'domain_pk'.\n        Default: 'nested_<n>' where <n> is 1+parent_router.nest_count\n\n    "


class NestedDefaultRouter(NestedMixin, DefaultRouter):
    __doc__ = " Create a NestedDefaultRouter nested within `parent_router`\n    Args:\n\n    parent_router: Parent router. Maybe be a DefaultRouteror another nested\n        router.\n\n    parent_prefix: The url prefix within parent_router under which the\n        routes from this router should be nested.\n\n    lookup:\n        The regex variable that matches an instance of the parent-resource\n        will be called '<lookup>_<parent-viewset.lookup_field>'\n        In the example above, lookup=domain and the parent viewset looks up\n        on 'pk' so the parent lookup regex will be 'domain_pk'.\n        Default: 'nested_<n>' where <n> is 1+parent_router.nest_count\n\n    "