# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/projectsmanager/appcallbackhandler.py
# Compiled at: 2020-05-10 06:49:20
# Size of source mod 2**32: 4029 bytes
"""Exposes a RESTful interface ."""
import uuid
import empower_core.apimanager.apimanager as apimanager

class AppCallbacksHandler(apimanager.APIHandler):
    __doc__ = 'Apps handler.'
    URLS = [
     '/api/v1/projects/([a-zA-Z0-9-]*)/apps/([a-zA-Z0-9-]*)/callbacks/?',
     '/api/v1/projects/([a-zA-Z0-9-]*)/apps/([a-zA-Z0-9-]*)/callbacks/([a-z]*)/?']

    @apimanager.validate(min_args=2, max_args=3)
    def get(self, *args, **kwargs):
        """List the callback.

        Args:

            [0]: the project id (mandatory)
            [1]: the app id (optional)
            [2]: the callback (optional)

        Example URLs:

            GET /api/v1/projects/52313ecb-9d00-4b7d-b873-b55d3d9ada26/apps/
                0f91e8ad-1c2a-4b06-97f9-e34097c4c1d0/callbacks
            {
                default: {
                    type: "url",
                    name: "default",
                    callback: "http://www.domain.io/resource"
                }
            }

            GET /api/v1/projects/52313ecb-9d00-4b7d-b873-b55d3d9ada26/apps/
                0f91e8ad-1c2a-4b06-97f9-e34097c4c1d0/callbacks/default

            {
                type: "url",
                name: "default",
                callback: "http://www.domain.io/resource"
            }
        """
        project_id = uuid.UUID(args[0])
        project = self.service.projects[project_id]
        service_id = uuid.UUID(args[1])
        service = project.services[service_id]
        if len(args) == 2:
            return service.callbacks
        return service.callbacks[args[2]]

    @apimanager.validate(returncode=201, min_args=2, max_args=2)
    def post(self, *args, **kwargs):
        """Add a callback.

        Args:

            [0]: the project id (mandatory)
            [1]: the app id (mandatory)

        Request:

            version: protocol version (1.0)
            name: the name of the callback (mandatory)
            callback: the callback URL (mandatory)

        Example URLs:

            POST /api/v1/workers
            {
                "version": "1.0",
                "name": "default",
                "callback_type": "rest"
                "callback": "http://www.domain.io/resource"
            }
        """
        project_id = uuid.UUID(args[0])
        project = self.service.projects[project_id]
        service_id = uuid.UUID(args[1])
        service = project.services[service_id]
        service.add_callback(name=(kwargs['name']), callback_type=(kwargs['callback_type']),
          callback=(kwargs['callback']))
        self.set_header('Location', '/api/v1/projects/%s/apps/%s/callback/%s' % (
         project_id, service_id, kwargs['name']))

    @apimanager.validate(returncode=204, min_args=3, max_args=3)
    def delete(self, *args, **kwargs):
        """Stop a worker.

        Args:

            [0]: the project id (mandatory)
            [1]: the app id (mandatory)
            [2]: the callback (mandatory)

        Example URLs:

            DELETE /api/v1/workers/08e14f40-6ebf-47a0-8baa-11d7f44cc228/default
        """
        project_id = uuid.UUID(args[0])
        project = self.service.projects[project_id]
        service_id = uuid.UUID(args[1])
        service = project.services[service_id]
        service.rem_callback(name=(args[2]))