# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/apps/search/forms.py
# Compiled at: 2015-02-18 15:13:31
# Size of source mod 2**32: 1872 bytes
from __future__ import absolute_import, division
import logging
from datetime import timedelta
from django.utils import timezone
from haystack.forms import FacetedModelSearchForm
from .utils import CelerityFacetedSearchFallbackMixin
logger = logging.getLogger('pegasus')

class CeleritySearchForm(FacetedModelSearchForm, CelerityFacetedSearchFallbackMixin):

    def no_query_found(self):
        """ If an empty search query is passed, assume that all results are
            being requested."""
        return self.searchqueryset.all()

    def search(self):
        sqs = super(CeleritySearchForm, self).search()
        self.facet_counts = sqs.facet('content_type').facet('article_type').facet('topic').facet('issue').facet_counts()
        if not self.facet_counts:
            self._apply_mock_facets(sqs)
        for k, v in getattr(self.data, 'iterlists', lambda : {})():
            if k == 'topic':
                sqs = sqs.filter(topic__in=v)
            elif k == 'issue':
                sqs = sqs.filter(issue__in=v)
            elif k == 'article_type':
                sqs = sqs.filter(article_type__in=v)
            elif k == 'content_type':
                sqs = sqs.filter(content_type__in=v)
            elif k == 'min_age':
                sqs = sqs.filter(pub_date__lte=timezone.now() - timedelta(days=int(v[0])))
            elif k == 'max_age':
                sqs = sqs.filter(pub_date__gte=timezone.now() - timedelta(days=int(v[0])))
                continue

        return sqs