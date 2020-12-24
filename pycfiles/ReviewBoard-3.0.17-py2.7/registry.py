# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/search/search_backends/registry.py
# Compiled at: 2020-02-11 04:03:56
"""The search engine backend registry."""
from __future__ import unicode_literals
from djblets.siteconfig.models import SiteConfiguration
from reviewboard.registries.registry import Registry
from reviewboard.search.search_backends.elasticsearch import ElasticsearchBackend
from reviewboard.search.search_backends.whoosh import WhooshBackend

class SearchBackendRegistry(Registry):
    """A registry for search engines backends.

    Extensions can add support for additional search engine backends.

    See :py:ref:`the registry documentation <registry-guides>` for information
    on how registries work.
    """
    lookup_attrs = [
     b'search_backend_id']

    def get_search_backend(self, search_backend_id):
        """Return the search backend with the specified ID.

        Args:
            search_backend_id (unicode):
                The unique identifier of the search engine.

        Returns:
            reviewboard.search.search_engines.base.SearchBackend:
            The search engine class, if it could be found. Otherwise, ``None``.
        """
        return self.get(b'search_backend_id', search_backend_id)

    def get_defaults(self):
        """Return the default search backends.

        Returns:
            list of reviewboard.search.search_backends.base.SearchBackend:
            The default search backends to use.
        """
        return [
         WhooshBackend(),
         ElasticsearchBackend()]

    @property
    def on_the_fly_indexing_enabled(self):
        """Whether or not on-the-fly indexing is enabled."""
        siteconfig = SiteConfiguration.objects.get_current()
        return siteconfig.get(b'search_on_the_fly_indexing')

    @property
    def search_enabled(self):
        """Whether or not search is enabled."""
        siteconfig = SiteConfiguration.objects.get_current()
        return siteconfig.get(b'search_enable')

    @property
    def results_per_page(self):
        """The number of search results per page."""
        siteconfig = SiteConfiguration.objects.get_current()
        return siteconfig.get(b'search_results_per_page')

    @property
    def current_backend(self):
        """The current search backend, or ``None`` if search is disabled."""
        if not self.search_enabled:
            return None
        else:
            siteconfig = SiteConfiguration.objects.get_current()
            return self.get_search_backend(siteconfig.get(b'search_backend_id'))