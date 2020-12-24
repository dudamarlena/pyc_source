# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/bottle_pika.py
# Compiled at: 2013-08-03 14:48:45
"""
Bottle-Pika is a plugin that integrates Pika (AMQP) with your Bottle
application. It automatically connects to AMQP at the beginning of a
request, passes the channel to the route callback and closes the
connection and channel afterwards.

To automatically detect routes that need a channel, the plugin
searches for route callbacks that require a `mq` keyword argument
(configurable) and skips routes that do not. This removes any overhead for
routes that don't need a message queue.

This plugin was originally based on the bottle-mysql plugin found at:
  https://pypi.python.org/pypi/bottle-mysql

Usage Example::

    import bottle
    import bottle_pika
    import pika

    app = bottle.Bottle()
    pika_plugin = bottle_pika.Plugin(pika.URLParameters('amqp://localhost/'))
    app.install(pika_plugin)

    @app.route('/hello')
    def hello(mq):
        mq.basic_publish(...)
        return HTTPResponse(status=200)

See pika documentation on channels for more information:
  http://pika.readthedocs.org/en/latest/modules/channel.html#pika.channel.Channel

"""
__version__ = '0.1.0'
__license__ = 'MIT'
import inspect, pika
from bottle import HTTPResponse, HTTPError, PluginError

class PikaPlugin(object):
    """
    This plugin passes a amqp channel to route callbacks
    that accept a `mq` keyword argument. If a callback does not expect
    such a parameter, no connection is made. You can override the connection
    settings on a per-route basis.
    """

    def __init__(self, params, keyword='mq'):
        self.params = params
        self.keyword = keyword

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, PikaPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError('Found another pika plugin with conflicting settings (non-unique keyword).')

    def apply(self, callback, context):
        conf = context['config'].get('pika') or {}
        params = conf.get('params', self.params)
        keyword = conf.get('keyword', self.keyword)
        args = inspect.getargspec(context['callback'])[0]
        if keyword not in args:
            return callback

        def wrapper(*args, **kwargs):
            con = None
            try:
                con = pika.BlockingConnection(params)
                mq = con.channel()
            except HTTPResponse as e:
                raise HTTPError(500, 'AMQP Error', e)

            kwargs[keyword] = mq
            try:
                try:
                    rv = callback(*args, **kwargs)
                except HTTPError as e:
                    raise
                except HTTPResponse as e:
                    raise

            finally:
                if con:
                    con.close()

            return rv

        return wrapper


Plugin = PikaPlugin