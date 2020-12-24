# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/discover/endpoints/discover_saved_queries.py
# Compiled at: 2019-08-16 17:27:47
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.serializers import serialize
from sentry.api.bases.discoversavedquery import DiscoverSavedQuerySerializer
from sentry.api.bases import OrganizationEndpoint
from sentry.discover.models import DiscoverSavedQuery
from sentry import features
from sentry.discover.endpoints.bases import DiscoverSavedQueryPermission

class DiscoverSavedQueriesEndpoint(OrganizationEndpoint):
    permission_classes = (
     DiscoverSavedQueryPermission,)

    def get(self, request, organization):
        """
        List saved queries for organization
        """
        if not features.has('organizations:discover', organization, actor=request.user):
            return self.respond(status=404)
        saved_queries = list(DiscoverSavedQuery.objects.filter(organization=organization).all().prefetch_related('projects').order_by('name'))
        return Response(serialize(saved_queries), status=200)

    def post(self, request, organization):
        """
        Create a saved query
        """
        if not features.has('organizations:discover', organization, actor=request.user):
            return self.respond(status=404)
        else:
            serializer = DiscoverSavedQuerySerializer(data=request.data, context={'organization': organization})
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            data = serializer.validated_data
            model = DiscoverSavedQuery.objects.create(organization=organization, name=data['name'], query=data['query'], created_by=request.user if request.user.is_authenticated() else None)
            model.set_projects(data['project_ids'])
            return Response(serialize(model), status=201)