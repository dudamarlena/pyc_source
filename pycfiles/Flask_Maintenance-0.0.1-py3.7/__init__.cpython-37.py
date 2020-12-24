# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\flask_maintenance\__init__.py
# Compiled at: 2019-07-07 01:58:20
# Size of source mod 2**32: 1201 bytes
import os
from flask import abort, current_app, _app_ctx_stack, _request_ctx_stack, request
__all__ = [
 'Maintenance']

class Maintenance:
    __doc__ = '\n    Add Maintenance mode feature to your flask application.\n    '

    def __init__(self, app=None):
        """
        :param app:
            Flask application object.
        """
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initalizes the application with the extension.

        :param app:
            Flask application object.
        """
        app.before_request_funcs.setdefault(None, []).append(self._handler)

    def _handler(self):
        """
        Maintenance mode handler.
        """
        actx = _app_ctx_stack.top
        rctx = _request_ctx_stack.top
        if actx:
            if rctx:
                if request.endpoint != 'static':
                    ins_path = os.path.join(current_app.instance_path, 'under_maintenance')
                    if os.path.exists(ins_path):
                        if os.path.isfile(ins_path):
                            abort(503)