# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: w:\projects\django-rest-framework-mongoengine\rest_framework_mongoengine\routers.py
# Compiled at: 2020-01-02 07:57:46
# Size of source mod 2**32: 830 bytes
from rest_framework import routers as drf_routers

class MongoRouterMixin(object):
    __doc__ = ' Mixin for mongo-routers.\n\n    Determines base_name from mongo queryset\n    '

    def get_default_basename(self, viewset):
        queryset = getattr(viewset, 'queryset', None)
        assert queryset is not None, '`base_name` argument not specified, and could not automatically determine the name from the viewset, as it does not have a `.queryset` attribute.'
        return queryset._document.__name__.lower()


class SimpleRouter(MongoRouterMixin, drf_routers.SimpleRouter):
    __doc__ = ' Adaptation of DRF SimpleRouter '


class DefaultRouter(MongoRouterMixin, drf_routers.DefaultRouter):
    __doc__ = ' Adaptation of DRF DefaultRouter '