# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/api/serializers/models/discoversavedquery.py
# Compiled at: 2019-09-04 11:05:35
from __future__ import absolute_import
import six
from sentry.api.serializers import Serializer, register
from sentry.discover.models import DiscoverSavedQuery

@register(DiscoverSavedQuery)
class DiscoverSavedQuerySerializer(Serializer):

    def serialize(self, obj, attrs, user, **kwargs):
        query_keys = [
         'fieldnames',
         'environment',
         'query',
         'fields',
         'conditions',
         'aggregations',
         'range',
         'start',
         'end',
         'orderby',
         'limit']
        data = {'id': six.text_type(obj.id), 
           'name': obj.name, 
           'projects': [ project.id for project in obj.projects.all() ], 'dateCreated': obj.date_created, 
           'dateUpdated': obj.date_updated, 
           'createdBy': six.text_type(obj.created_by_id) if obj.created_by_id else None}
        for key in query_keys:
            if obj.query.get(key) is not None:
                data[key] = obj.query[key]

        return data