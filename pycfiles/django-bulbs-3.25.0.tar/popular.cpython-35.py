# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/reading_list/popular.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 1017 bytes
from requests import ConnectionError
from django.conf import settings
from elasticsearch_dsl import filter as es_filter
from pageview_client.clients import TrendingClient
from bulbs.content.models import Content
DEFAULT_LIMIT = 10
trending_client = TrendingClient(settings.DIGEST_HOSTNAME, settings.DIGEST_ENDPOINT)

def get_popular_ids(limit=DEFAULT_LIMIT):
    try:
        ids = trending_client.get(settings.DIGEST_SITE, offset=settings.DIGEST_OFFSET, limit=limit)
        return list(ids)[:limit]
    except ConnectionError:
        return


def popular_content(**kwargs):
    """
    Use the get_popular_ids() to retrieve trending content objects.
    Return recent content on failure.
    """
    limit = kwargs.get('limit', DEFAULT_LIMIT)
    popular_ids = get_popular_ids(limit=limit)
    if not popular_ids:
        return Content.search_objects.search().extra(size=limit)
    return Content.search_objects.search().filter(es_filter.Ids(values=popular_ids))