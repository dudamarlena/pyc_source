# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/khvn/.virtualenvs/rakomon/lib/python3.4/site-packages/rakomon/endpoint.py
# Compiled at: 2017-04-06 11:36:32
# Size of source mod 2**32: 576 bytes
import tornado.ioloop, tornado.web
from . import settings, monitor

class MonitorHandler(tornado.web.RequestHandler):

    def initialize(self, mon):
        self.monitor = mon

    def get(self):
        self.write(self.monitor.values)


def run(handler=MonitorHandler, mon=monitor.default(), config=settings.ENDPOINT_CONFIG.copy(), **kwargs):
    config.update(kwargs)
    app = tornado.web.Application((
     (
      config['url_path'], handler, dict(monitor=mon)),))
    app.listen(config['port'], address=config['address'])
    tornado.ioloop.current().start()