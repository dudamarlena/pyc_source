# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/search/indexes.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.core.exceptions import ImproperlyConfigured
from haystack import indexes

class BaseSearchIndex(indexes.SearchIndex):
    """Base class for a search index.

    This sets up a few common fields we want all indexes to include.
    """
    model = None
    local_site_attr = None
    text = indexes.CharField(document=True, use_template=True)
    local_sites = indexes.MultiValueField(null=True)
    NO_LOCAL_SITE_ID = 0

    def get_model(self):
        """Return the model for this index."""
        return self.model

    def prepare_local_sites(self, obj):
        """Prepare the list of local sites for the search index.

        This will take any associated local sites on the object and store
        them in the index as a list. The search view can then easily look up
        values in the list, regardless of the type of object.

        If the object is not a part of a local site, the list will be
        ``[0]``, indicating no local site.
        """
        if not self.local_site_attr:
            raise ImproperlyConfigured(b'local_site_attr must be set on %r' % self.__class__)
        if not hasattr(obj, self.local_site_attr):
            raise ImproperlyConfigured(b'"%s" is not a valid local site attribute on %r' % (
             self.local_site_attr, obj.__class__))
        local_sites = getattr(obj, self.local_site_attr, None)
        if self.local_site_attr.endswith(b'_id'):
            if local_sites is not None:
                return [local_sites]
            else:
                return [
                 self.NO_LOCAL_SITE_ID]

        else:
            return [ local_site.pk for local_site in local_sites.all()
                   ] or [
             self.NO_LOCAL_SITE_ID]
        return