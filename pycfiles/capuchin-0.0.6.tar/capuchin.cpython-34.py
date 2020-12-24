# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/py/capuchin/capuchin/capuchin.py
# Compiled at: 2015-01-26 14:36:39
# Size of source mod 2**32: 5411 bytes
"""``capuchin`` is a simple wrapper around the tornado framework that
provides a few built-in endpoints (/ping, /status, /time) and also
some endpoint signing functions/wrappers.

Here is a simple service example app::

    import capuchin

    class TestHandler(tornado.web.RequestHandler):
            def get(self):
                    self.write("hola")

    def test_job():
            print("did some job")

    if __name__ == "__main__":
            c = capuchin.web.Application([
                    (r"/test", TestHandler),
            ])
            c.add_status_job("Test Job", 5, test_job)
            c.listen()
"""
import os, tornado.ioloop, tornado.web
from handlers import StatusHandler, PingHandler, TimeHandler

class Application(tornado.web.Application):
    __doc__ = 'tornado Application instance that auto-prepends each route\n    with an endpoint set from the environment.\n\n    eg. if the endpoint is `/myservice/1.0`, then the /ping route would be set as:\n        `myservice/1.0/ping`\n\n    Also includes built-in endpoints for the following:\n        - /status (invokes each status job and writes the result as JSON)\n        - /ping   (returns a 200 OK with `pong` as the body)\n        - /time   (returns the servers current UTC time)\n    '

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