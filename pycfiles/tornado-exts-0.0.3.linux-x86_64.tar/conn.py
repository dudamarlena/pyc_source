# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tornado_extensions/sockjs/conn.py
# Compiled at: 2013-09-03 05:36:04
import sockjs.tornado, simplejson as json, logging
log = logging.getLogger()
logging.getLogger().setLevel(logging.DEBUG)

class BaseSockJSConnection(sockjs.tornado.SockJSConnection):
    """
    Base socket class that shape logic and protocol how each socket connection
    will be served by sockjs server.
    """
    _middlewares = None

    def on_message(self, message):
        """
        Facade method that is responsible for handling new message. Each method
        in Comet is json-like that consists of two parts.

        Notes
        -----
        Method is responsible for handling `name` part of `message` to find
        responsible event handler and call it with `args` part of `message`

        Parameters
        ----------
        message : json-like
            New incoming message to comet server.

        Examples
        --------

        >>>
        {
          'name': 'addChatMessage'
          'args': *({'message': 'hi', 'token': '21312', 'to': 10000008})
        }

        """
        data = json.loads(message)
        event, args = data['name'], data['args']
        log.debug(('ARGS {}').format(args))
        assert event not in ('open', 'close', 'message'), 'Already reserved events!'
        assert isinstance(args, list), 'args param must be a list'
        f = getattr(self, ('on_{}').format(event), None)
        if f and callable(f):
            if len(args) == 1 and isinstance(args[0], dict):
                f(**args[0])
            else:
                f(*args)
        else:
            log.error('event handler')
        return