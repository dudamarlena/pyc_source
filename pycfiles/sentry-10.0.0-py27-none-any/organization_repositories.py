# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_repositories.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework.response import Response
from sentry.api.base import DocSection
from sentry.api.bases.organization import OrganizationEndpoint, OrganizationRepositoryPermission
from sentry.api.paginator import OffsetPaginator
from sentry.api.serializers import serialize
from sentry.constants import ObjectStatus
from sentry.models import Integration, Repository
from sentry.plugins import bindings
from sentry.utils.sdk import capture_exception

class OrganizationRepositoriesEndpoint(OrganizationEndpoint):
    doc_section = DocSection.ORGANIZATIONS
    permission_classes = (OrganizationRepositoryPermission,)

    def get(self, request, organization):
        """
        List an Organization's Repositories
        ```````````````````````````````````

        Return a list of version control repositories for a given organization.

        :pparam string organization_slug: the organization short name
        :auth: required
        """
        queryset = Repository.objects.filter(organization_id=organization.id)
        status = request.GET.get('status', 'active')
        if status == 'active':
            queryset = queryset.filter(status=ObjectStatus.VISIBLE)
        else:
            if status == 'deleted':
                queryset = queryset.exclude(status=ObjectStatus.VISIBLE)
            elif status == 'unmigratable':
                integrations = Integration.objects.filter(organizationintegration__organization=organization, organizationintegration__status=ObjectStatus.ACTIVE, provider__in=('bitbucket',
                                                                                                                                                                                 'github',
                                                                                                                                                                                 'vsts'), status=ObjectStatus.ACTIVE)
                repos = []
                for i in integrations:
                    try:
                        repos.extend(i.get_installation(organization.id).get_unmigratable_repositories())
                    except Exception:
                        capture_exception()
                        continue

                return Response(serialize(repos, request.user))
            if status:
                queryset = queryset.none()
        return self.paginate(request=request, queryset=queryset, order_by='name', on_results=lambda x: serialize(x, request.user), paginator_cls=OffsetPaginator)

    def post(self, request, organization):
        if not request.user.is_authenticated():
            return Response(status=401)
        else:
            provider_id = request.data.get('provider')
            if provider_id is not None and provider_id.startswith('integrations:'):
                try:
                    provider_cls = bindings.get('integration-repository.provider').get(provider_id)
                except KeyError:
                    return Response({'error_type': 'validation'}, status=400)

                provider = provider_cls(id=provider_id)
                return provider.dispatch(request, organization)
            try:
                provider_cls = bindings.get('repository.provider').get(provider_id)
            except KeyError:
                return Response({'error_type': 'validation'}, status=400)

            provider = provider_cls(id=provider_id)
            return provider.dispatch(request, organization)