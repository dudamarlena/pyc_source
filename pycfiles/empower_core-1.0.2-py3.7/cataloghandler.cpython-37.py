# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/projectsmanager/cataloghandler.py
# Compiled at: 2020-05-10 06:49:18
# Size of source mod 2**32: 2301 bytes
"""Exposes a RESTful interface ."""
import empower_core.apimanager.apimanager as apimanager

class CatalogHandler(apimanager.APIHandler):
    __doc__ = 'Access the applications catalog.'
    URLS = [
     '/api/v1/projects/catalog/?',
     '/api/v1/projects/catalog/(.*)/?']

    @apimanager.validate(min_args=0, max_args=1)
    def get(self, *args, **kwargs):
        """List of available applications

        Example URLs:

             GET /api/v1/projects/catalog

            {
                empower.apps.wifimobilitymanager.wifimobilitymanager: {
                    params: {
                        service_id: {
                            desc: "The unique UUID of the application.",
                            mandatory: true,
                            type: "UUID"
                        },
                        project_id: {
                            desc: "The project on which this app must
                                be executed.",
                            mandatory: true,
                            type: "UUID"
                        },
                        every: {
                            desc: "The control loop period (in ms).",
                            mandatory: false,
                            default: 2000,
                            type: "int"
                        }
                    },
                    name:
                        "empower.apps.wifimobilitymanager.wifimobilitymanager",
                    desc: "A simple Wi-Fi mobility manager."
                }
            }
        """
        if not args:
            return self.service.catalog
        return self.service.catalog[args[0]]