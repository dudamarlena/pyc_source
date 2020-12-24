# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/envmanager/workercallbackshandler.py
# Compiled at: 2020-05-10 06:49:21
# Size of source mod 2**32: 3455 bytes
"""Exposes a RESTful interface ."""
import uuid
import empower_core.apimanager.apimanager as apimanager

class WorkerCallbacksHandler(apimanager.APIHandler):
    __doc__ = 'Workers handler.'
    URLS = [
     '/api/v1/workers/([a-zA-Z0-9-]*)/callbacks/?',
     '/api/v1/workers/([a-zA-Z0-9-]*)/callbacks/([a-z]*)/?']

    @apimanager.validate(min_args=1, max_args=2)
    def get(self, *args, **kwargs):
        """List the callback.

        Args:

            [0]: the worker id (mandatory)
            [1]: the callback (optional)

        Example URLs:

            GET /api/v1/workers/0f91e8ad-1c2a-4b06-97f9-e34097c4c1d0/callbacks
            {
                default: {
                    type: "url",
                    name: "default",
                    callback: "http://www.domain.io/resource"
                }
            }

            GET /api/v1/workers/0f91e8ad-1c2a-4b06-97f9-e34097c4c1d0/
                callbacks/default

            {
                type: "url",
                name: "default",
                callback: "http://www.domain.io/resource"
            }
        """
        service_id = uuid.UUID(args[0])
        service = self.service.env.services[service_id]
        if len(args) == 1:
            return service.callbacks
        return service.callbacks[args[1]]

    @apimanager.validate(returncode=201, min_args=1, max_args=1)
    def post(self, *args, **kwargs):
        """Add a callback.

        Args:

            [0]: the worker id (mandatory)

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
        service_id = uuid.UUID(args[0])
        service = self.service.env.services[service_id]
        service.add_callback(name=(kwargs['name']), callback_type=(kwargs['callback_type']),
          callback=(kwargs['callback']))
        self.set_header('Location', '/api/v1/workers/%s/callback/%s' % (
         service.service_id, kwargs['name']))

    @apimanager.validate(returncode=204, min_args=2, max_args=2)
    def delete(self, *args, **kwargs):
        """Stop a worker.

        Args:

            [0]: the worker id (mandatory)
            [1]: the callback (mandatory)

        Example URLs:

            DELETE /api/v1/workers/08e14f40-6ebf-47a0-8baa-11d7f44cc228/default
        """
        service_id = uuid.UUID(args[0])
        service = self.service.env.services[service_id]
        service.rem_callback(name=(args[1]))