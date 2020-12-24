# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/projectsmanager/projectsmanager.py
# Compiled at: 2020-05-10 08:04:31
# Size of source mod 2**32: 3483 bytes
"""Projects manager."""
from empower_core.launcher import srv_or_die
from empower_core.service import EService
from empower_core.projectsmanager.project import Project
from empower_core.projectsmanager.appcallbackhandler import AppCallbacksHandler
from empower_core.projectsmanager.cataloghandler import CatalogHandler
from empower_core.projectsmanager.appshandler import AppsHandler
from empower_core.projectsmanager.projectshandler import ProjectsHandler

class ProjectsManager(EService):
    __doc__ = 'Projects manager.'
    HANDLERS = [
     CatalogHandler, AppsHandler, ProjectsHandler,
     AppCallbacksHandler]
    PROJECT_IMPL = Project
    projects = {}

    def start(self):
        super().start()
        for project in self.PROJECT_IMPL.objects.all():
            self.projects[project.project_id] = project
            self.projects[project.project_id].start_services()

    @property
    def catalog(self):
        """Return available apps."""
        return dict()

    def create(self, desc, project_id, owner):
        """Create new project."""
        if project_id in self.projects:
            raise ValueError('Project %s already defined' % project_id)
        accounts_manager = srv_or_die('accountsmanager')
        if owner not in accounts_manager.accounts:
            raise KeyError('Username %s not found' % owner)
        project = self.PROJECT_IMPL(project_id=project_id, desc=desc,
          owner=owner)
        project.save()
        self.projects[project_id] = project
        self.projects[project_id].start_services()
        return self.projects[project_id]

    def update(self, project_id, desc):
        """Update project."""
        if project_id not in self.projects:
            raise KeyError('Project %s not found' % project_id)
        project = self.projects[project_id]
        try:
            project.desc = desc
            project.save()
        finally:
            project.refresh_from_db()

        return self.projects[project_id]

    def remove_all(self):
        """Remove all projects."""
        for project_id in list(self.projects):
            self.remove(project_id)

    def remove(self, project_id):
        """Remove project."""
        if project_id not in self.projects:
            raise KeyError('Project %s not registered' % project_id)
        project = self.projects[project_id]
        self.projects[project_id].stop_services()
        project.delete()
        del self.projects[project_id]


def launch(context, service_id):
    """ Initialize the module. """
    return ProjectsManager(context=context, service_id=service_id)