# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/mediators/plugins/migrator.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.mediators import Mediator, Param
from sentry.models import Repository
from sentry.plugins import plugins
from sentry.utils.cache import memoize

class Migrator(Mediator):
    integration = Param('sentry.models.integration.Integration')
    organization = Param('sentry.models.organization.Organization')

    def call(self):
        for project in self.projects:
            for plugin in plugins.for_project(project):
                if plugin.slug != self.integration.provider:
                    continue
                if self.all_repos_migrated(plugin.slug):
                    self.disable_for_all_projects(plugin)

    def all_repos_migrated(self, provider):
        provider = 'visualstudio' if provider == 'vsts' else provider
        return all(r.integration_id is not None for r in self.repos_for_provider(provider))

    def disable_for_all_projects(self, plugin):
        for project in self.projects:
            try:
                self.log(at='disable', project=project.slug, plugin=plugin.slug)
                plugin.disable(project=project)
            except NotImplementedError:
                pass

    def repos_for_provider(self, provider):
        return filter(lambda r: r.provider == provider, self.repositories)

    @property
    def repositories(self):
        return Repository.objects.filter(organization_id=self.organization.id)

    @memoize
    def projects(self):
        return list(self.organization.project_set.all())

    @property
    def plugins(self):
        return [ plugins.configurable_for_project(project) for project in self.projects ]

    @property
    def _logging_context(self):
        return {'org': self.organization.slug, 
           'integration_id': self.integration.id, 
           'integration_provider': self.integration.provider}