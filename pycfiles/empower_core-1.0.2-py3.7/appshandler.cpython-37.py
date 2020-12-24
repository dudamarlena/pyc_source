# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/projectsmanager/appshandler.py
# Compiled at: 2020-05-10 06:49:19
# Size of source mod 2**32: 5352 bytes
"""Exposes a RESTful interface ."""
import uuid
import empower_core.apimanager.apimanager as apimanager

class AppsHandler(apimanager.APIHandler):
    __doc__ = 'Applications handler.'
    URLS = [
     '/api/v1/projects/([a-zA-Z0-9-]*)/apps/?',
     '/api/v1/projects/([a-zA-Z0-9-]*)/apps/([a-zA-Z0-9-]*)/?']

    @apimanager.validate(min_args=1, max_args=2)
    def get(self, *args, **kwargs):
        """List the apps.

        Args:

            [0]: the project id (mandatory)
            [1]: the app id (optional)

        Example URLs:

            GET /api/v1/projects/52313ecb-9d00-4b7d-b873-b55d3d9ada26/apps

            [
                {
                    "counters": {},
                    "name":
                        "empower.apps.wifimobilitymanager.wifimobilitymanager",
                    "params": {
                        "every": 2000,
                        "project_id": "52313ecb-9d00-4b7d-b873-b55d3d9ada26",
                        "service_id": "7069c865-8849-4840-9d96-e028663a5dcf"
                    },
                    "stats": {
                        "last_run": "2019-08-23 09:45:20.234651"
                    }
                }
            ]

            GET /api/v1/projects/52313ecb-9d00-4b7d-b873-b55d3d9ada26/apps/
                7069c865-8849-4840-9d96-e028663a5dcf

            {
                "counters": {},
                "name": "empower.apps.wifimobilitymanager.wifimobilitymanager",
                "params": {
                    "every": 2000,
                    "project_id": "52313ecb-9d00-4b7d-b873-b55d3d9ada26",
                    "service_id": "7069c865-8849-4840-9d96-e028663a5dcf"
                },
                "stats": {
                    "last_run": "2019-08-23 09:47:04.361268"
                }
            }
        """
        project_id = uuid.UUID(args[0])
        project = self.service.projects[project_id]
        if len(args) == 1:
            return project.services
        return project.services[uuid.UUID(args[1])]

    @apimanager.validate(returncode=201, min_args=1, max_args=2)
    def post(self, *args, **kwargs):
        """Start a new app.

        Args:

            [0]: the project id (mandatory)

        Request:

            version: protocol version (1.0)
            params: the list of parmeters to be set

        Example URLs:

            POST /api/v1/projects/52313ecb-9d00-4b7d-b873-b55d3d9ada26/apps

            {
                "version": "1.0",
                "name": "empower.apps.wifimobilitymanager.wifimobilitymanager",
                "params": {
                    "every": 5000
                }
            }
        """
        project_id = uuid.UUID(args[0])
        project = self.service.projects[project_id]
        service_id = uuid.UUID(args[1]) if len(args) > 1 else None
        params = kwargs['params'] if 'params' in kwargs else {}
        service = project.register_service(name=(kwargs['name']), params=params,
          service_id=service_id)
        self.set_header('Location', '/api/v1/projects/%s/apps/%s' % (
         project.project_id, service.service_id))

    @apimanager.validate(returncode=204, min_args=2, max_args=2)
    def put(self, *args, **kwargs):
        """Update the configuration of an applications.

        Args:

            [0]: the project id (mandatory)
            [1]: the app id (mandatory)

        Request:

            version: protocol version (1.0)
            params: the list of parmeters to be set

        Example URLs:

            PUT /api/v1/projects/52313ecb-9d00-4b7d-b873-b55d3d9ada26/apps/
                7069c865-8849-4840-9d96-e028663a5dcf

            {
                "version": "1.0",
                "params": {
                    "every": 5000
                }
            }
        """
        project_id = uuid.UUID(args[0])
        project = self.service.projects[project_id]
        service_id = uuid.UUID(args[1])
        params = kwargs['params'] if 'params' in kwargs else {}
        project.reconfigure_service(service_id, params)

    @apimanager.validate(returncode=204, min_args=2, max_args=2)
    def delete(self, *args, **kwargs):
        """Stop an app.

        Args:

            [0]: the project id (mandatory)
            [1]: the app id (mandatory)

        Example URLs:

            DELETE /api/v1/projects/52313ecb-9d00-4b7d-b873-b55d3d9ada26/apps/
                7069c865-8849-4840-9d96-e028663a5dcf
        """
        project_id = uuid.UUID(args[0])
        project = self.service.projects[project_id]
        service_id = uuid.UUID(args[1])
        project.unregister_service(service_id)