# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/envmanager/workershandler.py
# Compiled at: 2020-05-10 06:49:20
# Size of source mod 2**32: 4390 bytes
"""Exposes a RESTful interface ."""
import uuid
import empower_core.apimanager.apimanager as apimanager

class WorkersHandler(apimanager.APIHandler):
    __doc__ = 'Workers handler.'
    URLS = [
     '/api/v1/workers/?',
     '/api/v1/workers/([a-zA-Z0-9-]*)/?']

    @apimanager.validate(min_args=0, max_args=1)
    def get(self, *args, **kwargs):
        """List the workers.

        Args:

            [0]: the worker id (optional)

        Example URLs:

            GET /api/v1/workers

            [
                {
                    "name":
                        "empower.workers.wifichannelstats.wifichannelstats",
                    "params": {
                        "every": 2000,
                        "project_id": "4cd2bca2-8c28-4e66-9c8a-7cbd1ba4e6f9",
                        "service_id": "0f91e8ad-1c2a-4b06-97f9-e34097c4c1d0"
                    }
                }
            ]

            GET /api/v1/workers/0f91e8ad-1c2a-4b06-97f9-e34097c4c1d0

            {
                "name": "empower.workers.wifichannelstats.wifichannelstats",
                "params": {
                    "every": 2000,
                    "project_id": "4cd2bca2-8c28-4e66-9c8a-7cbd1ba4e6f9",
                    "service_id": "0f91e8ad-1c2a-4b06-97f9-e34097c4c1d0"
                }
            }
        """
        if not args:
            return self.service.env.services
        return self.service.env.services[uuid.UUID(args[0])]

    @apimanager.validate(returncode=201, min_args=0, max_args=1)
    def post(self, *args, **kwargs):
        """Start a new worker.

        Args:

            [0], the service id (optional)

        Request:

            version: protocol version (1.0)
            name: the name of the worker (mandatory)
            params: the list of parmeters to be set (optional)

        Example URLs:

            POST /api/v1/workers
            {
                "version": "1.0",
                "name": "empower.workers.wifichannelstats.wifichannelstats",
                "params": {
                    "every": 5000
                }
            }
        """
        service_id = uuid.UUID(args[0]) if args else None
        params = kwargs['params'] if 'params' in kwargs else {}
        service = self.service.env.register_service(name=(kwargs['name']), params=params,
          service_id=service_id)
        self.set_header('Location', '/api/v1/workers/%s' % service.service_id)

    @apimanager.validate(returncode=204, min_args=1, max_args=1)
    def put(self, *args, **kwargs):
        """Update the configuration of a worker.

        Args:

            [0], the worker id (mandatory)

        Request:

            version: protocol version (1.0)
            params: the list of parmeters to be set (optional)

        Example URLs:

            PUT /api/v1/workers/08e14f40-6ebf-47a0-8baa-11d7f44cc228
            {
                "version": "1.0",
                "params":
                {
                    "every": 5000
                }
            }
        """
        service_id = uuid.UUID(args[0])
        params = kwargs['params'] if 'params' in kwargs else {}
        self.service.env.reconfigure_service(service_id=service_id, params=params)

    @apimanager.validate(returncode=204, min_args=1, max_args=1)
    def delete(self, *args, **kwargs):
        """Stop a worker.

        Args:

            [0], the worker id

        Example URLs:

            DELETE /api/v1/workers/08e14f40-6ebf-47a0-8baa-11d7f44cc228
        """
        service_id = uuid.UUID(args[0])
        self.service.env.unregister_service(service_id=service_id)