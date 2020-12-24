# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jceciliano/coding/Lantern/lantern-flask/.virtualenv/lib/python3.6/site-packages/lantern_flask/controllers/application_controller.py
# Compiled at: 2018-11-30 11:45:11
# Size of source mod 2**32: 803 bytes
from lantern_flask import settings

class ApplicationController(object):
    __doc__ = ' Allow us to easily fetch cognito parsed data \n    '

    def __init__(self, debug=False):
        self.debug = debug if debug else settings.get('LOCAL_USER', False)

    def get_app_id(self, request, required=True):
        """ Returns the app_id value sent in the request headers
            Parameters:
                - request: required, active HTTP request
                - required: (default=True) if set to True and no app_id foud a ValueError will be raised
        """
        if not request:
            raise Exception('You have to specify a valid `request` parameter (inside a http request)')
        app_id_value = request.headers.get('app_id', None)
        return app_id_value