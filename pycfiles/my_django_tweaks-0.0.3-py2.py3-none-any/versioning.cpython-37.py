# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ricard/develop/my_django_tweaks/my_django_tweaks/versioning.py
# Compiled at: 2019-05-17 08:43:05
# Size of source mod 2**32: 4341 bytes
from django.conf import settings
import django.utils.translation as _
from rest_framework import status
from rest_framework.exceptions import APIException
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

class IncorrectVersionException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('This API Version is Incorrect.')


class ObsoleteVersionException(APIException):
    status_code = status.HTTP_410_GONE
    default_detail = _('This API Version is Obsolete.')


class ApiVersionMixin(object):
    __doc__ = '\n        Use this as first in inheritance chain when creating own API classes\n        Returns serializer depending on versioning_serializer_classess and version\n\n        versioning_serializer_classess = {\n            1: "x",\n            2: "x",\n        }\n\n        You can set custom deprecated/obsolete versions\n        CUSTOM_DEPRECATED_VERSION = X\n        CUSTOM_OBSOLETE_VERSION = Y\n\n        It can be also configured on the settings level as a fixed version\n        API_DEPRECATED_VERSION = X\n        API_OBSOLETE_VERSION = Y\n\n        or as an offset - for example:\n        API_VERSION_DEPRECATION_OFFSET = 6\n        API_VERSION_OBSOLETE_OFFSET = 10\n\n        Offset is calculated using the highest version number:\n        deprecated = max(self.versioning_serializer_classess.keys() - API_VERSION_DEPRECATION_OFFSET)\n        obsolete = max(self.versioning_serializer_classess.keys() - API_VERSION_OBSOLETE_OFFSET)\n\n        If neither is set, deprecation/obsolete will not work. Only the first applicable setting is taken into account\n        (in the order as presented above).\n    '

    @classmethod
    def get_deprecated_and_obsolete_versions(cls):
        deprecated = getattr(settings, 'API_DEPRECATED_VERSION', getattr(cls, 'CUSTOM_DEPRECATED_VERSION', None))
        obsolete = getattr(settings, 'API_OBSOLETE_VERSION', getattr(cls, 'CUSTOM_OBSOLETE_VERSION', None))
        if deprecated is None or obsolete is None:
            API_VERSION_DEPRECATION_OFFSET = getattr(settings, 'API_VERSION_DEPRECATION_OFFSET', None)
            API_VERSION_OBSOLETE_OFFSET = getattr(settings, 'API_VERSION_OBSOLETE_OFFSET', None)
            if hasattr(cls, 'versioning_serializer_classess'):
                max_version = max(cls.versioning_serializer_classess.keys())
                if deprecated is None:
                    if API_VERSION_DEPRECATION_OFFSET is not None:
                        deprecated = max_version - API_VERSION_DEPRECATION_OFFSET
                if obsolete is None:
                    if API_VERSION_OBSOLETE_OFFSET is not None:
                        obsolete = max_version - API_VERSION_OBSOLETE_OFFSET
        return (
         deprecated, obsolete)

    def get_version(self):
        if hasattr(self.request, 'version'):
            if self.request.version is not None:
                try:
                    version = int(self.request.version)
                except ValueError:
                    raise IncorrectVersionException

                return version

    def get_serializer_class(self):
        if hasattr(self.request, 'version'):
            if self.request.version is not None:
                version = self.get_version()
                deprecated, obsolete = self.get_deprecated_and_obsolete_versions()
                if obsolete and version <= obsolete:
                    raise ObsoleteVersionException
                else:
                    if deprecated:
                        if version <= deprecated:
                            self.request._request.deprecated = True
                if hasattr(self, 'versioning_serializer_classess'):
                    try:
                        return self.versioning_serializer_classess[version]
                    except KeyError:
                        raise IncorrectVersionException

        return self.serializer_class


class DeprecationMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        """ Adds deprecation warning - if applicable """
        if getattr(request, 'deprecated', False):
            response['Warning'] = '299 - "This Api Version is Deprecated"'
        return response