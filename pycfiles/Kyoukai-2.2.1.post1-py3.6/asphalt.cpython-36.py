# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kyoukai/asphalt.py
# Compiled at: 2017-09-29 12:38:41
# Size of source mod 2**32: 8722 bytes
"""
Asphalt wrappers for Kyoukai.
"""
import abc, importlib, logging, socket, ssl as py_ssl
from functools import partial
from asphalt.core import resolve_reference, Context
from asphalt.core.component import Component
from asphalt.core.event import Signal, Event
from werkzeug.routing import Rule
from werkzeug.wrappers import Request, Response
from kyoukai.blueprint import Blueprint
from kyoukai.route import Route

class ConnectionMadeEvent(Event):
    __doc__ = '\n    Dispatched when a connection is made to the server.\n\n    This does NOT fire when using WSGI workers.\n\n    This has the protocol as the ``protocol`` attribute.\n    '

    def __init__(self, source, topic, *, protocol):
        super().__init__(source, topic)
        self.protocol = protocol


class ConnectionLostEvent(ConnectionMadeEvent):
    __doc__ = '\n    Dispatched when a connection is lost from the server.\n\n    This does NOT fire when using WSGI workers.\n\n    This has the protocol as the ``protocol`` attribute.\n    '


class CtxEvent(Event):

    def __init__(self, source, topic, *, ctx):
        super().__init__(source, topic)
        self.ctx = ctx


class RouteMatchedEvent(CtxEvent):
    __doc__ = '\n    Dispatched when a route is matched.\n\n    This has the context as the ``ctx`` attribute, and the route can be accessed via ``ctx.route``.\n    '


class RouteInvokedEvent(CtxEvent):
    __doc__ = '\n    Dispatched when a route is invoked.\n\n    This has the context as the ``ctx`` attribute.\n    '


class RouteReturnedEvent(CtxEvent):
    __doc__ = '\n    Dispatched after a route has returned.\n\n    This has the context as the ``ctx`` attribute and the response as the ``result`` attribute.\n    '

    def __init__(self, source, topic, *, ctx, result):
        super().__init__(source, topic, ctx=ctx)
        self.result = result


class KyoukaiBaseComponent(Component, metaclass=abc.ABCMeta):
    __doc__ = '\n    The base class for any component used by Kyoukai.\n\n    This one does not create a Server instance; it should be used when you are using a different \n    HTTP server backend.\n    '
    connection_made = Signal(ConnectionMadeEvent)
    connection_lost = Signal(ConnectionLostEvent)

    def __init__(self, app, ip: str='127.0.0.1', port: int=4444, **cfg):
        from kyoukai.app import Kyoukai
        if not isinstance(app, Kyoukai):
            app = resolve_reference(app)
        self.app = app
        self.ip = ip
        self.port = port
        self.cfg = cfg
        self.server = None
        self.base_context = None
        self.backend = self.cfg.get('backend', 'kyoukai.backends.httptools_')
        self.logger = logging.getLogger('Kyoukai')
        self._server_name = app.server_name or socket.getfqdn()

    @abc.abstractmethod
    async def start(self, ctx: Context):
        """
        Overridden in subclasses to spawn a new server.
        """
        pass

    def get_server_name(self):
        """
        :return: The server name of this app.
        """
        return self.app.server_name or self._server_name

    def get_protocol(self, ctx: Context, serv_info: tuple):
        """
        Gets the protocol to use for this webserver.
        """
        if not hasattr(self, '_cached_mod'):
            mod = importlib.import_module(self.backend)
            self._cached_mod = mod
        server = getattr(self._cached_mod, self._cached_mod.PROTOCOL_CLASS)
        proto = server(self, ctx, *serv_info)
        ctx.protocol = proto
        return proto


class KyoukaiComponent(KyoukaiBaseComponent):
    __doc__ = '\n    A component for Kyoukai.\n    This includes the built-in HTTP server.  \n    \n    .. versionchanged:: 2.2\n    \n        Passing ``run_server`` as False will not run the inbuilt web server.\n    '
    connection_made = Signal(ConnectionMadeEvent)
    connection_lost = Signal(ConnectionLostEvent)

    def __init__(self, app, ip='127.0.0.1', port=4444, **cfg):
        """
        Creates a new component.

        :param app: The application object to use.
            This can either be the real application object, or a string that resolves to a             reference for the real application object.

        :param ip: If using the built-in HTTP server, the IP to bind to.
        :param port: If using the built-in HTTP server, the port to bind to.
        :param cfg: Additional configuration.
        """
        (super().__init__)(app, ip, port, **cfg)
        self.app.config.update(self.cfg)
        for key, value in cfg.items():
            setattr(self, key, value)

    def get_server_name(self):
        """
        :return: The server name of this app.
        """
        return self.app.server_name or self._server_name

    async def start(self, ctx: Context):
        """
        Starts the webserver if required.

        :param ctx: The base context.
        """
        self.base_context = ctx
        ssl_context = None
        if self.cfg.get('ssl', {}):
            ssl = self.cfg['ssl']
            if ssl.get('enabled') is True:
                ssl_context = py_ssl.create_default_context(py_ssl.Purpose.CLIENT_AUTH)
                ssl_context.set_ciphers('ECDH+CHACHA20:ECDH+CHACHA20:ECDH+AES128:RSA+AES128:ECDH+AES256:RSA+AES256:ECDH+3DES:RSA+3DES:!aNULL:!eNULL:!MD5:!DSS:!RC4')
                ssl_context.load_cert_chain(certfile=(ssl['ssl_certfile']), keyfile=(ssl['ssl_keyfile']))
                if self.cfg.get('http2', False) is True:
                    ssl_context.set_alpn_protocols(['h2'])
                    try:
                        ssl_context.set_npn_protocols(['h2'])
                    except NotImplementedError:
                        pass

                self.logger.info('Using HTTP over TLS.')
        if self.cfg.get('run_server', True) is True:
            protocol = partial(self.get_protocol, ctx, (self._server_name, self.port))
            self.app.finalize()
            self.server = await self.app.loop.create_server(protocol, (self.ip), (self.port), ssl=ssl_context)
            self.logger.info('Kyoukai serving on {}:{}.'.format(self.ip, self.port))


class HTTPRequestContext(Context):
    __doc__ = '\n    The context subclass passed to all requests within Kyoukai.\n    '
    route_matched = Signal(RouteMatchedEvent)
    route_invoked = Signal(RouteInvokedEvent)
    route_completed = Signal(RouteReturnedEvent)

    def __init__(self, parent, request):
        super().__init__(parent)
        self.app = None
        self.request = request
        self.params = None
        self.route = None
        self.bp = None
        self.rule = None
        self.environ = self.request.environ
        self.proto = None

    def url_for(self, endpoint: str, *, method: str=None, **kwargs):
        """
        A context-local version of ``url_for``.

        For more information, see the documentation on :meth:`~.Blueprint.url_for`.
        """
        return (self.app.url_for)(self.environ, endpoint, method=method, **kwargs)