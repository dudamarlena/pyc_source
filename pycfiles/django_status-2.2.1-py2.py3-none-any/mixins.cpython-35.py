# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/perdy/Development/django-status/status/api/mixins.py
# Compiled at: 2016-09-29 07:57:11
# Size of source mod 2**32: 429 bytes
from django.core.urlresolvers import reverse

class ProviderMixin:

    def get_provider_url(self, request, resource, name):
        """
        Get provider url given resource and provider name.

        :param request: Django Request
        :param resource:
        :param name:
        :return:
        """
        return request.build_absolute_uri(reverse('status:api_{}_{}'.format(resource, name)))