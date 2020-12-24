# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/envmanager/envhandler.py
# Compiled at: 2020-05-10 06:49:22
# Size of source mod 2**32: 1394 bytes
"""Exposes a RESTful interface ."""
import empower_core.apimanager.apimanager as apimanager

class EnvHandler(apimanager.APIHandler):
    __doc__ = 'Access the system services.'
    URLS = [
     '/api/v1/env/?']

    @apimanager.validate(min_args=0, max_args=1)
    def get(self, *args, **kwargs):
        """Get environment

        Example URLs:

             GET /api/v1/env

            {
                "empower.managers.envmanager.envmanager": {
                    "name": "empower.managers.envmanager.envmanager",
                    "params": {
                        "service_id": "b7d872a2-fee1-442e-b6d9-f33e5ce9fca1",
                        "every": -1
                    }
                }
            }
        """
        return self.service.env