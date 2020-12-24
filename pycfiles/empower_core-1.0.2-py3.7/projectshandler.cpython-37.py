# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/projectsmanager/projectshandler.py
# Compiled at: 2020-05-10 06:49:18
# Size of source mod 2**32: 3457 bytes
"""Exposes a RESTful interface ."""
import uuid
import empower_core.apimanager.apimanager as apimanager

class ProjectsHandler(apimanager.APIHandler):
    __doc__ = 'Projects handler'
    URLS = [
     '/api/v1/projects/?',
     '/api/v1/projects/([a-zA-Z0-9-]*)/?']

    @apimanager.validate(min_args=0, max_args=1)
    def get(self, *args, **kwargs):
        """Lists all the projects.

        Args:

            [0], the project id (optional)

        Example URLs:

            GET /api/v1/projects

            [
                {
                    "bootstrap": {
                    },
                    "desc": "Project description",
                    "owner": "foo",
                    "project_id": "52313ecb-9d00-4b7d-b873-b55d3d9ada26",
                }
            ]

            GET /api/v1/projects/52313ecb-9d00-4b7d-b873-b55d3d9ada26

            {
                "bootstrap": {
                },
                "desc": "Project description",
                "owner": "foo",
                "project_id": "52313ecb-9d00-4b7d-b873-b55d3d9ada26",
            }
        """
        if not args:
            return self.service.projects
        return self.service.projects[uuid.UUID(args[0])]

    @apimanager.validate(returncode=201, min_args=0, max_args=1)
    def post(self, *args, **kwargs):
        """Create a new project.

        Args:

            [0], the project id (optional)

        Request:

            version: protocol version (1.0)
            desc: a human-readable description of the project
            owner: the username of the requester
        """
        project_id = uuid.UUID(args[0]) if args else uuid.uuid4()
        project = self.service.create(project_id=project_id, desc=(kwargs['desc']),
          owner=(kwargs['owner']))
        self.set_header('Location', '/api/v1/projects/%s' % project.project_id)

    @apimanager.validate(returncode=204, min_args=1, max_args=1)
    def put(self, *args, **kwargs):
        """Update a project.

        Args:

            [0], the project id (mandatory)

        Request:

            version: protocol version (1.0)
            desc: a human-readable description of the project
        """
        project_id = uuid.UUID(args[0])
        self.service.update(project_id=project_id, desc=(kwargs['desc']))

    @apimanager.validate(returncode=204, min_args=0, max_args=1)
    def delete(self, *args, **kwargs):
        """Delete one or all projects.

        Args:

            [0], the projects id

        Example URLs:

            DELETE /api/v1/projects
            DELETE /api/v1/projects/52313ecb-9d00-4b7d-b873-b55d3d9ada26
        """
        if args:
            self.service.remove(uuid.UUID(args[0]))
        else:
            self.service.remove_all()