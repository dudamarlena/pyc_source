# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_search_details.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry import analytics
from sentry.api.bases.organization import OrganizationEndpoint, OrganizationSearchPermission
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.models import SavedSearch
from sentry.models.search_common import SearchType

class OrganizationSearchDetailsEndpoint(OrganizationEndpoint):
    permission_classes = (
     OrganizationSearchPermission,)

    def delete(self, request, organization, search_id):
        """
        Delete a saved search

        Permanently remove a saved search.

            {method} {path}

        """
        try:
            search = SavedSearch.objects.get(owner__isnull=True, organization=organization, id=search_id)
        except SavedSearch.DoesNotExist:
            raise ResourceDoesNotExist

        search.delete()
        analytics.record('organization_saved_search.deleted', search_type=SearchType(search.type).name, org_id=organization.id, query=search.query)
        return Response(status=204)