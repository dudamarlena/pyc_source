# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/timesketch_api_client/index.py
# Compiled at: 2019-11-22 09:03:26
# Size of source mod 2**32: 2040 bytes
"""Timesketch API client library."""
from __future__ import unicode_literals
from . import resource

class SearchIndex(resource.BaseResource):
    __doc__ = 'Timesketch searchindex object.\n\n    Attributes:\n        id: The ID of the search index.\n        api: An instance of TimesketchApi object.\n    '

    def __init__(self, searchindex_id, api, searchindex_name=None):
        """Initializes the SearchIndex object.

        Args:
            searchindex_id: Primary key ID of the searchindex.
            searchindex_name: Name of the searchindex (optional).
        """
        self.id = searchindex_id
        self._searchindex_name = searchindex_name
        self._resource_uri = 'searchindices/{0:d}'.format(self.id)
        super(SearchIndex, self).__init__(api=api, resource_uri=self._resource_uri)

    @property
    def name(self):
        """Property that returns searchindex name.

        Returns:
            Searchindex name as string.
        """
        if not self._searchindex_name:
            searchindex = self.lazyload_data()
            self._searchindex_name = searchindex['objects'][0]['name']
        return self._searchindex_name

    @property
    def index_name(self):
        """Property that returns Elasticsearch index name.

        Returns:
            Elasticsearch index name as string.
        """
        searchindex = self.lazyload_data()
        return searchindex['objects'][0]['index_name']