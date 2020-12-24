# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/py/capuchin/capuchin/web.py
# Compiled at: 2015-01-26 14:44:03
# Size of source mod 2**32: 5424 bytes
__doc__ = '``capuchin`` is a simple wrapper around the tornado framework that\nprovides a few built-in endpoints (/ping, /status, /time) and also\nsome endpoint signing functions/wrappers.\n\nHere is a simple service example app::\n\n    import capuchin.web\n\n    class TestHandler(tornado.web.RequestHandler):\n            def get(self):\n                    self.write("hola")\n\n    def test_job():\n            print("did some job")\n\n    if __name__ == "__main__":\n            c = capuchin.web.Application([\n                    (r"/test", TestHandler),\n            ])\n            c.add_status_job("Test Job", 5, test_job)\n            c.listen()\n'
import os, tornado.ioloop, tornado.web
from capuchin.handlers import StatusHandler, PingHandler, TimeHandler

class Application(tornado.web.Application):
    """Application"""

    def __init__(self, handlers=None, **settings):
        try:
            port_str = os.environ.get('PORT', '8080')
            self.port = int(port_str)
        except ValueError:
            self.port = 8080

        self.address = os.environ.get('HOST', '0.0.0.0')
        self.key = os.environ.get('KEY')
        self._endpoint = os.environ.get('ENDPOINT')
        self._jobs = []
        all_handlers = [
         (
          '/status', StatusHandler, dict(jobs_func=self.jobs)),
         (
          '/ping', PingHandler),
         (
          '/time', TimeHandler)]
        if handlers:
            all_handlers = all_handlers + handlers
        super(Application, self).__init__(all_handlers, **settings)

    def jobs(self):
        """Generator that yields each status job.
        """
        for job in self._jobs:
            yield job

    def add_status_job(self, name, timeout_ms, job_func):
        """Adds the given status job to the collection of jobs.
        """
        self._jobs.append((name, timeout_ms, job_func))

    def add_handlers(self, host_pattern, host_handlers):
        """Appends the given handlers to the collection.
        """
        host_handlers = prefix_handlers(self._endpoint, host_handlers)
        super(Application, self).add_handlers(host_pattern, host_handlers)

    def listen(self):
        """Starts an HTTP server on the on the host/port specified
        from the "HOST" and "PORT" environment variables.
        """
        if self.address:
            listening_on = '{}:{}'.format(self.address, self.port)
            super(Application, self).listen(self.port, address=self.address)
        else:
            listening_on = 'port {}'.format(self.port)
            super(Application, self).listen(self.port)
        print('[capuchin] listening on ' + listening_on)
        tornado.ioloop.IOLoop.instance().start()


def prefix_handlers(endpoint, handlers):
    """Prepends each handlers route with the given endpoint.

    eg.

    Given:
        endpoint    = /sweet+service/1.0
        handlers[0] = (r"/people, PeopleHandler)
    ------
    Result:
        handlers[0] = (r"/sweet+service/1.0/people", PeopleHandler)
    """
    if not endpoint:
        endpoint = '/'
    for i, handler in enumerate(handlers):
        path = handler[0]
        if path[0] == '/':
            path = path[1:]
        handlers[i] = (
         endpoint + path,) + handler[1:]

    return handlers