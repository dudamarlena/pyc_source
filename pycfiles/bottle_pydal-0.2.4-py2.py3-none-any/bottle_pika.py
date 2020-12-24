# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/bottle_pika.py
# Compiled at: 2013-08-03 14:48:45
__doc__ = "\nBottle-Pika is a plugin that integrates Pika (AMQP) with your Bottle\napplication. It automatically connects to AMQP at the beginning of a\nrequest, passes the channel to the route callback and closes the\nconnection and channel afterwards.\n\nTo automatically detect routes that need a channel, the plugin\nsearches for route callbacks that require a `mq` keyword argument\n(configurable) and skips routes that do not. This removes any overhead for\nroutes that don't need a message queue.\n\nThis plugin was originally based on the bottle-mysql plugin found at:\n  https://pypi.python.org/pypi/bottle-mysql\n\nUsage Example::\n\n    import bottle\n    import bottle_pika\n    import pika\n\n    app = bottle.Bottle()\n    pika_plugin = bottle_pika.Plugin(pika.URLParameters('amqp://localhost/'))\n    app.install(pika_plugin)\n\n    @app.route('/hello')\n    def hello(mq):\n        mq.basic_publish(...)\n        return HTTPResponse(status=200)\n\nSee pika documentation on channels for more information:\n  http://pika.readthedocs.org/en/latest/modules/channel.html#pika.channel.Channel\n\n"
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