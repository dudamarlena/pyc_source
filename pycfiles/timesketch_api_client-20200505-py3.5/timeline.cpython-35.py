# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/timesketch_api_client/timeline.py
# Compiled at: 2020-05-05 06:18:41
# Size of source mod 2**32: 2207 bytes
"""Timesketch API client library."""
from __future__ import unicode_literals
from . import resource

class Timeline(resource.BaseResource):
    __doc__ = 'Timeline object.\n\n    Attributes:\n        id: Primary key of the view.\n    '

    def __init__(self, timeline_id, sketch_id, api, name=None, searchindex=None):
        """Initializes the Timeline object.

        Args:
            timeline_id: The primary key ID of the timeline.
            sketch_id: ID of a sketch.
            api: Instance of a TimesketchApi object.
            name: Name of the timeline (optional)
            searchindex: The Elasticsearch index name (optional)
        """
        self.id = timeline_id
        self._name = name
        self._searchindex = searchindex
        resource_uri = 'sketches/{0:d}/timelines/{1:d}/'.format(sketch_id, self.id)
        super(Timeline, self).__init__(api, resource_uri)

    @property
    def name(self):
        """Property that returns timeline name.

        Returns:
            Timeline name as string.
        """
        if not self._name:
            timeline = self.lazyload_data()
            self._name = timeline['objects'][0]['name']
        return self._name

    @property
    def index(self):
        """Property that returns index name.

        Returns:
            Elasticsearch index name as string.
        """
        if not self._searchindex:
            timeline = self.lazyload_data()
            index_name = timeline['objects'][0]['searchindex']['index_name']
            self._searchindex = index_name
        return self._searchindex