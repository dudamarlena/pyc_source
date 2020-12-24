# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/control/rest/flask_server.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1263 bytes
import flask, werkzeug.serving
from werkzeug.datastructures import ImmutableOrderedMultiDict
from ...util import log
from ...util.threads import runnable
from ...animation.remote import opener

class OrderedFlask(flask.Flask):

    class request_class(flask.Request):
        parameter_storage_class = ImmutableOrderedMultiDict


class FlaskServer(runnable.LoopThread):
    OPEN_DELAY = 1

    def __init__(self, port, external_access, open_page, **kwds):
        super().__init__()
        self.port = port
        self.hostname = '0.0.0.0' if external_access else 'localhost'
        self.app = OrderedFlask(__name__, **kwds)
        self.open_page = open_page

    def run_once(self):
        if self.open_page:
            opener.raw_opener('localhost', self.port, self.OPEN_DELAY)
        werkzeug.serving.run_simple(self.hostname, self.port, self.app)
        super().stop()

    def stop(self):

        def error():
            log.error('Unable to shut down REST server on port %d', self.port)

        super().stop()
        try:
            flask.request.environ.get('werkzeug.server.shutdown', error)()
        except Exception:
            log.debug('Exception shutting werkzeug down')