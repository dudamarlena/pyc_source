# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/webapptitude/googleapi.py
# Compiled at: 2016-08-31 16:32:16
"""Simplified access to Google's various service APIs"""
try:
    from oauth2client.appengine import AppAssertionCredentials
except ImportError:
    from oauth2client.contrib.appengine import AppAssertionCredentials

from apiclient import discovery
from apiclient.http import HttpError
from webapp2 import cached_property
from httpclient import HTTP

class Executor(object):
    """A generic pagination and iteration facility for queries/etc."""

    def __init__(self, http, factory=None, **props):
        self.http = http
        self.factory = factory
        self.options = props

    def paginate(self, factory, **props):
        page_count = 0
        while True:
            result = self.execute(factory, **props)
            yield (page_count, result)
            props['pageToken'] = result.get('nextPageToken', None)
            page_count = page_count + 1
            if not props['pageToken']:
                break

        return

    def execute(self, factory, **props):
        num_retries = props.pop('retries', 0)
        return factory(**props).execute(http=self.http, num_retries=num_retries)

    def map(self, factory, attrib, **props):
        """
        Iterate through named collections within all pages of a resultset.

        Example:
            # list all tables in a bigquery dataset (presumably many)
            tables = executor.map(bigquery.tables().list, 'tables',
                                  project_id=... dataset_id=...)

            # loop through all the table records.
            for page_id, page, record_id, table in tables:
                # do something with each table record
                pass

        This abstracts the pagination logic, so iteration can run at the
        level of all records in aggregate.
        """
        for page_id, result in self.paginate(factory, **props):
            if attrib is None:
                yield result
            else:
                for record_id, record in enumerate(result.get(attrib, [])):
                    yield (
                     page_id, result, record_id, record)

        return

    def __iter__(self):
        """
        Iterate through all pages of a result set.

        NOTE: this only works when instantiated with suitable factory and
        query properties.
        """
        if self.factory is not None:
            return self.paginate(self.factory, **self.options)
        else:
            return []
            return


class ServiceBase(object):
    """Provide authentication and service handling generics."""
    _cache_namespace = 'googleapi#'
    _cache_lifetime = 300
    API_SCOPE = []

    def __init__(self, credential_factory=None):
        if credential_factory is None:
            credential_factory = AppAssertionCredentials
        self.credentials = credential_factory(self.API_SCOPE)
        return

    @cached_property
    def http(self):
        return self.credentials.authorize(HTTP(namespace=self._cache_namespace, lifetime=self._cache_lifetime))

    @cached_property
    def executor(self):
        return Executor(self.http)

    def discover(self, name, version, **props):
        """Retrieve a service interface under the authenticated environment."""
        return discovery.build(name, version, http=self.http, **props)

    def execute(self, factory, **props):
        """Execute a prepared request with the authenticated environment."""
        return self.executor.execute(factory, **props)