# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/integrations/repositories.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.constants import ObjectStatus
from sentry.models import Repository

class RepositoryMixin(object):
    repo_search = False

    def get_repositories(self, query=None):
        """
        Get a list of availble repositories for an installation

        >>> def get_repositories(self):
        >>>     return self.get_client().get_repositories()

        return [{
            'name': display_name,
            'identifier': external_repo_id,
        }]

        The shape of the `identifier` should match the data
        returned by the integration's
        IntegrationRepositoryProvider.repository_external_slug()
        """
        raise NotImplementedError

    def get_unmigratable_repositories(self):
        return []

    def reinstall_repositories(self):
        """
        reinstalls repositories associated with the integration
        """
        organizations = self.model.organizations.all()
        Repository.objects.filter(organization_id__in=organizations.values_list('id', flat=True), provider='integrations:%s' % self.model.provider, integration_id=self.model.id).update(status=ObjectStatus.VISIBLE)

    def has_repo_access(self, repo):
        raise NotImplementedError