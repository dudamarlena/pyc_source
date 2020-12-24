# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/timesketch_api_client/view.py
# Compiled at: 2020-04-01 11:40:49
# Size of source mod 2**32: 3809 bytes
"""Timesketch API client library."""
from __future__ import unicode_literals
import json
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

    def _get_top_level_attribute(self, name, default_value=None, refresh=False):
        """Returns a top level attribute from a view object.

        Args:
            name: String with the attribute name.
            default_value: The default value if the attribute does not exit,
                defaults to None.
            refresh: If set to True then the data will be refreshed.

        Returns:
            The dict value of the key "name".
        """
        view = self.lazyload_data(refresh_cache=refresh)
        view_objects = view.get('objects')
        if not view_objects:
            return default_value
        if not len(view_objects) == 1:
            return default_value
        first_object = view_objects[0]
        return first_object.get(name, default_value)

    @property
    def description(self):
        """Property that returns the description value of a view.

        Returns:
            Description of the view as a string.
        """
        return self._get_top_level_attribute('description', default_value='')

    @property
    def user(self):
        """Property that returns the username of the view creator.

        Returns:
            A string with the username of the user generating the view.
        """
        user_dict = self._get_top_level_attribute('user', default_value={})
        username = user_dict.get('username')
        if not username:
            return 'System'
        return username

    @property
    def query_string(self):
        """Property that returns the views query string.

        Returns:
            Elasticsearch query as string.
        """
        return self._get_top_level_attribute('query_string', default_value='')

    @property
    def query_filter(self):
        """Property that returns the views filter.

        Returns:
            Elasticsearch filter as a dict.
        """
        query_filter_string = self._get_top_level_attribute('query_filter', default_value='')
        if not query_filter_string:
            return ''
        return json.loads(query_filter_string)

    @property
    def query_dsl(self):
        """Property that returns the views query DSL.

        Returns:
            Elasticsearch DSL as a dict.
        """
        dsl_string = self._get_top_level_attribute('query_dsl', default_value='')
        if not dsl_string:
            return ''
        return json.loads(dsl_string)