# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/datastore_viewer/presentation/ui/html.py
# Compiled at: 2020-03-28 06:49:22
# Size of source mod 2**32: 548 bytes
import os
from logging import getLogger
import flask.views
logger = getLogger(__name__)

class DashboardView(flask.views.MethodView):

    def get(self, path=None):
        return flask.render_template('datastore_viewer/index.html')


class ServeStaticFileView(flask.views.MethodView):

    def get(self, path):
        directory = os.path.join(os.path.dirname(__file__), '..', 'template', 'datastore_viewer', 'static')
        logger.info(f"call ServeStaticFileView, {directory} {path}")
        return flask.send_from_directory(directory, path)