# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/timesketch_api_client/view.py
# Compiled at: 2019-11-22 09:03:26
# Size of source mod 2**32: 2130 bytes
"""Timesketch API client library."""
from __future__ import unicode_literals
from . import resource

class View(resource.BaseResource):
    __doc__ = 'Saved view object.\n\n    Attributes:\n        id: Primary key of the view.\n        name: Name of the view.\n    '

    def __init__(self, view_id, view_name, sketch_id, api):
        """Initializes the View object.

        Args:
            view_id: Primary key ID for the view.
            view_name: The name of the view.
            sketch_id: ID of a sketch.
            api: Instance of a TimesketchApi object.
        """
        self.id = view_id
        self.name = view_name
        resource_uri = 'sketches/{0:d}/views/{1:d}/'.format(sketch_id, self.id)
        super(View, self).__init__(api, resource_uri)

    @property
    def query_string(self):
        """Property that returns the views query string.

        Returns:
            Elasticsearch query as string.
        """
        view = self.lazyload_data()
        return view['objects'][0]['query_string']

    @property
    def query_filter(self):
        """Property that returns the views filter.

        Returns:
            Elasticsearch filter as JSON string.
        """
        view = self.lazyload_data()
        return view['objects'][0]['query_filter']

    @property
    def query_dsl(self):
        """Property that returns the views query DSL.

        Returns:
            Elasticsearch DSL as JSON string.
        """
        view = self.lazyload_data()
        return view['objects'][0]['query_dsl']