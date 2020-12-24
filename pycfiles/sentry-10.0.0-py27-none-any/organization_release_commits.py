# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_release_commits.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.api.base import DocSection
from sentry.api.bases.organization import OrganizationReleasesBaseEndpoint
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.api.serializers import serialize
from sentry.models import Release, ReleaseCommit

class OrganizationReleaseCommitsEndpoint(OrganizationReleasesBaseEndpoint):
    doc_section = DocSection.RELEASES

    def get(self, request, organization, version):
        """
        List an Organization Release's Commits
        ``````````````````````````````````````

        Retrieve a list of commits for a given release.

        :pparam string organization_slug: the slug of the organization the
                                          release belongs to.
        :pparam string version: the version identifier of the release.
        :auth: required
        """
        try:
            release = Release.objects.distinct().get(organization_id=organization.id, projects__in=self.get_projects(request, organization), version=version)
        except Release.DoesNotExist:
            raise ResourceDoesNotExist

        queryset = ReleaseCommit.objects.filter(release=release).select_related('commit', 'commit__author')
        return self.paginate(request=request, queryset=queryset, order_by='order', on_results=lambda x: serialize([ rc.commit for rc in x ], request.user))