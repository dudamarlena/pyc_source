# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_pinned_searches.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework import serializers
from rest_framework.response import Response
from django.db.models import Q
from django.utils import six
from sentry.api.bases.organization import OrganizationEndpoint, OrganizationPinnedSearchPermission
from sentry.api.serializers import serialize
from sentry.models import SavedSearch
from sentry.models.search_common import SearchType
PINNED_SEARCH_NAME = 'My Pinned Search'

class OrganizationSearchSerializer(serializers.Serializer):
    type = serializers.IntegerField(required=True)
    query = serializers.CharField(required=True)

    def validate_type(self, value):
        try:
            SearchType(value)
        except ValueError as e:
            raise serializers.ValidationError(six.text_type(e))

        return value


class OrganizationPinnedSearchEndpoint(OrganizationEndpoint):
    permission_classes = (
     OrganizationPinnedSearchPermission,)

    def put(self, request, organization):
        serializer = OrganizationSearchSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.validated_data
            SavedSearch.objects.create_or_update(organization=organization, name=PINNED_SEARCH_NAME, owner=request.user, type=result['type'], values={'query': result['query']})
            pinned_search = SavedSearch.objects.get(organization=organization, owner=request.user, type=result['type'])
            try:
                existing_search = SavedSearch.objects.filter(Q(organization=organization, owner__isnull=True) | Q(is_global=True), type=result['type'], query=result['query'])[:1].get()
            except SavedSearch.DoesNotExist:
                pass
            else:
                pinned_search = existing_search
                existing_search.is_pinned = True

            return Response(serialize(pinned_search, request.user), status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, organization):
        try:
            search_type = SearchType(int(request.data.get('type', 0)))
        except ValueError as e:
            return Response({'detail': 'Invalid input for `type`. Error: %s' % six.text_type(e)}, status=400)

        SavedSearch.objects.filter(organization=organization, owner=request.user, type=search_type.value).delete()
        return Response(status=204)