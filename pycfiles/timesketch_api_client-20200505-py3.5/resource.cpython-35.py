# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/timesketch_api_client/resource.py
# Compiled at: 2019-11-22 09:03:26
# Size of source mod 2**32: 1605 bytes
"""Timesketch API client library."""
from __future__ import unicode_literals

class BaseResource(object):
    __doc__ = 'Base resource object.'

    def __init__(self, api, resource_uri):
        """Initialize object.

        Args:
            api: An instance of TimesketchApi object.
        """
        self.api = api
        self.resource_uri = resource_uri
        self.resource_data = None

    def lazyload_data(self, refresh_cache=False):
        """Load resource data once and cache the result.

        Args:
            refresh_cache: Boolean indicating if to update cache.

        Returns:
            Dictionary with resource data.
        """
        if not self.resource_data or refresh_cache:
            self.resource_data = self.api.fetch_resource_data(self.resource_uri)
        return self.resource_data

    @property
    def data(self):
        """Property to fetch resource data.

        Returns:
            Dictionary with resource data.
        """
        return self.lazyload_data()