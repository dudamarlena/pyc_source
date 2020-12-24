# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/project_release_setup.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.api.bases.project import ProjectEndpoint, ProjectReleasePermission
from sentry.models import Group, ReleaseCommit, Repository, Deploy
from rest_framework.response import Response

class ProjectReleaseSetupCompletionEndpoint(ProjectEndpoint):
    permission_classes = (
     ProjectReleasePermission,)

    def get(self, request, project):
        """
        Get list with release setup progress for a project
        1. tag an error
        2. link a repo
        3. associate commits
        4. tell sentry about a deploy
        """
        tag = Group.objects.filter(project=project.id, first_release__isnull=False).exists()
        repo = Repository.objects.filter(organization_id=project.organization_id).exists()
        commit = ReleaseCommit.objects.filter(organization_id=project.organization_id, release__projects=project.id).exists()
        deploy = Deploy.objects.filter(organization_id=project.organization_id, release__projects=project.id).exists()
        return Response([{'step': 'tag', 'complete': bool(tag)}, {'step': 'repo', 'complete': bool(repo)}, {'step': 'commit', 'complete': bool(commit)}, {'step': 'deploy', 'complete': bool(deploy)}])