# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/base/handler.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = '\n\n  handler base\n  ~~~~~~~~~~~~\n\n  Presents a reasonable base class for a ``Handler`` object, which handles\n  responding to an arbitrary "request" for action. For example, ``Handler``\n  is useful for responding to HTTP requests *or* noncyclical realtime-style\n  requests, and acts as a base class for ``Page`` and ``ServiceHandler``.\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n'
import itertools
from ..core import injection

class Handler(object):
    """ Base class structure for a ``Handler`` of some request or desired action.
      Specifies basic machinery for tracking a ``request`` alongside some form
      of ``response``.

      Also keeps track of relevant ``environ`` (potentially from WSGI) and sets
      up a jump off point for DI-provided tools like logging, config, caching,
      template rendering, etc. """
    config = property(lambda self: {})
    __agent__ = None
    __status__ = 200
    __routes__ = None
    __context__ = None
    __logging__ = None
    __runtime__ = None
    __environ__ = None
    __request__ = None
    __headers__ = None
    __response__ = None
    __callback__ = None
    __content_type__ = None
    __owner__, __metaclass__ = 'Handler', injection.Compound

    def __init__(self, environ=None, start_response=None, runtime=None, request=None, response=None, **context):
        """ Initialize a new ``Handler`` object with proper ``environ`` details and
        inform it of larger world around it.

        ``Handler`` objects (much like ``Runtime`` objects) are designed to be
        usable independently as a WSGI-style callable. Note that the first two
        position parameters of this ``__init__`` are the venerable ``environ``
        and ``start_response`` - dispatching this way is totally possible, but
        providing ``runtime``, ``request`` and ``response`` allow tighter
        integration with the underlying runtime.

        Current execution details (internal to Canteen) are passed as ``kwargs``
          and compounded as new context items are added.

        :param environ: WSGI environment, provided by active runtime. ``dict``
          in standard WSGI format.

        :param start_response: Callable to begin the response cycle. Usually a
          vanilla ``function``.

        :param runtime: Currently-active Canteen runtime. Always an instance of
          :py:class:`canteen.core.runtime.Runtime` or a subclass thereof.

        :param request: Object to use for ``self.request``. Usually an instance
          of :py:class:`werkzeug.wrappers.Request`.

        :param response: Object to use for ``self.response``. Usually an
          instance of :py:class:`werkzeug.wrappers.Response`. """
        self.__runtime__, self.__environ__, self.__callback__ = runtime, environ, start_response
        self.__status__, self.__headers__, self.__content_type__ = 200, {}, 'text/html; charset=utf-8'
        self.__request__, self.__response__, self.__context__ = request, response, context

    routes = property(lambda self: self.__runtime__.routes)
    status = property(lambda self: self.__status__)
    headers = property(lambda self: self.__headers__)
    content_type = property(lambda self: self.__content_type__)
    url_for = link = lambda self, end, **args: self.routes.build(end, args)
    app = runtime = property(lambda self: self.__runtime__)
    environment = environ = property(lambda self: self.__environ__)
    start_response = callback = property(lambda self: self.__callback__)
    session = property(lambda self: self.request.session[0] if self.request.session else None)
    agent = property(lambda self: self.__agent__ if self.__agent__ else setattr(self, '__agent__', self.http.agent.scan(self.request)) or self.__agent__)
    request = property(lambda self: self.__request__ if self.__request__ else setattr(self, '__request__', self.http.new_request(self.__environ__)) or self.__request__)
    response = property(lambda self: self.__response__ if self.__response__ else setattr(self, '__response__', self.http.new_response()) or self.__response__)

    @property
    def template_context(self):
        """ Generate template context to be used in rendering source templates. The
        ``template_context`` accessor is expected to return a ``dict`` of
        ``name=>value`` pairs to present to the template API.

        :returns: ``dict`` of template context. """
        from canteen.rpc import ServiceHandler
        return {'handler': self, 
           'config': getattr(self, 'config', {}), 
           'runtime': self.runtime, 
           'http': {'agent': getattr(self, 'agent', None), 
                    'request': self.request, 
                    'response': self.response}, 
           'wsgi': {'environ': self.environ, 
                    'callback': self.callback, 
                    'start_response': self.start_response}, 
           'cache': {'get': self.cache.get, 
                     'get_multi': self.cache.get_multi, 
                     'set': self.cache.set, 
                     'set_multi': self.cache.set_multi, 
                     'delete': self.cache.delete, 
                     'delete_multi': self.cache.delete_multi, 
                     'clear': self.cache.clear, 
                     'flush': self.cache.flush}, 
           'asset': {'image': self.assets.image_url, 
                     'style': self.assets.style_url, 
                     'script': self.assets.script_url}, 
           'services': {'list': ServiceHandler.services, 
                        'describe': ServiceHandler.describe}, 
           'output': {'render': self.template.render, 
                      'environment': self.template.environment}, 
           'link': self.url_for, 
           'route': {'build': self.url_for, 
                     'resolve': self.http.resolve_route}}

    def respond--- This code section failed: ---

 L. 232         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'status'
                6  POP_JUMP_IF_TRUE     21  'to 21'
                9  LOAD_CONST               200
               12  LOAD_FAST             0  'self'
               15  STORE_ATTR            1  '__status__'
               18  JUMP_FORWARD          0  'to 21'
             21_0  COME_FROM            18  '18'

 L. 233        21  LOAD_FAST             1  'content'
               24  POP_JUMP_IF_FALSE    42  'to 42'
               27  LOAD_FAST             1  'content'
               30  LOAD_FAST             0  'self'
               33  LOAD_ATTR             2  'response'
               36  STORE_ATTR            2  'response'
               39  JUMP_FORWARD          0  'to 42'
             42_0  COME_FROM            39  '39'

 L. 240        42  LOAD_FAST             2  'direct'
               45  POP_JUMP_IF_TRUE    125  'to 125'
               48  LOAD_GLOBAL           3  'setattr'
               51  LOAD_FAST             0  'self'
               54  LOAD_ATTR             2  'response'
               57  LOAD_GLOBAL           4  'isinstance'
               60  LOAD_FAST             0  'self'
               63  LOAD_ATTR             0  'status'
               66  LOAD_GLOBAL           5  'int'
               69  CALL_FUNCTION_2       2  None
               72  POP_JUMP_IF_FALSE    81  'to 81'
               75  LOAD_CONST               'status_code'
               78  JUMP_FORWARD          3  'to 84'
               81  LOAD_CONST               'status'
             84_0  COME_FROM            78  '78'
               84  LOAD_FAST             0  'self'
               87  LOAD_ATTR             0  'status'
               90  CALL_FUNCTION_3       3  None
               93  JUMP_IF_TRUE_OR_POP   128  'to 128'
               96  LOAD_GENEXPR             '<code_object <genexpr>>'
               99  MAKE_FUNCTION_0       0  None
              102  LOAD_FAST             0  'self'
              105  LOAD_ATTR             2  'response'
              108  LOAD_ATTR             2  'response'
              111  GET_ITER         
              112  CALL_FUNCTION_1       1  None
              115  LOAD_FAST             0  'self'
              118  LOAD_ATTR             2  'response'
              121  BUILD_TUPLE_2         2 
              124  RETURN_END_IF    
            125_0  COME_FROM            93  '93'
            125_1  COME_FROM            45  '45'
              125  LOAD_FAST             0  'self'
              128  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_END_IF' instruction at offset 124

    def render(self, template, headers=None, content_type='text/html; charset=utf-8', context=None, _direct=False, **kwargs):
        """ Render a source ``template`` for the purpose of responding to this
        ``Handler``'s request, given ``context`` and proper ``headers`` for
        return.

        ``kwargs`` are taken as extra template context and overlayed onto
        ``context`` before render.

        :param template: Path to template file to serve. ``str`` or ``unicode``
          file path.

        :param headers: Extra headers to send with response. ``dict`` or iter of
          ``(name, value)`` tuples.

        :param content_type: Value to send for ``Content-Type`` header. ``str``,
          defaults to ``text/html; charset=utf-8``.

        :param context: Extra template context to include during render.
          ``dict`` of items, with keys as names that values are bound to in the
          resulting template context.

        :param _direct: Flag indicating that ``self`` should be returned, rather
          than ``self.response``. Bool, defaults to ``False`` as this
          technically breaks WSGI.

        :param kwargs: Additional items to add to the template context.
          Overrides all other sources of context.

        :returns: Rendered template content, added to ``self.response``. """
        from canteen.util import config
        if content_type:
            self.response.mimetype = content_type
        self.response.headers.extend(itertools.chain(iter(self.http.base_headers), self.config.get('http', {}).get('headers', {}).iteritems(), self.headers.iteritems(), (headers or {}).iteritems()))
        _merged_context = dict(itertools.chain(*(i.iteritems() for i in (
         self.template.base_context,
         self.template_context,
         context or {},
         kwargs))))
        self.response.response, self.response.direct_passthrough = self.template.render(self, getattr(self.runtime, 'config', None) or config.Config(), template, _merged_context), True
        return self.respond(direct=_direct)

    def dispatch(self, **url_args):
        """ Dispatch a WSGI request through this ``Handler``. Expected to be an
        HTTP-style (cyclical) dispatch flow.

        :param url_args: Arguments provided from the URI that should be passed
          along to any resulting handler calls.

        :returns: After filling the local response object (at ``self.response``)
          returns it for inspection or reply. """
        self.__response__ = getattr(self, self.request.method)(**url_args) or self.__response__
        return self.__response__

    def __call__(self, url_args, direct=False):
        """ Kick off the local response dispatch process, and run any necessary
        pre/post hooks (named ``prepare`` and ``destroy``, respectively).

        :param url_args: Arguments parsed from URL according to matched route.
          ``dict`` of ``{param: value}`` pairs.

        :param direct: Flag to indicate 'direct' mode, whereby a handler is
          returned instead of a response. Bool, defaults to ``False``, as this
          technically breaks WSGI.

        :returns: ``self.response`` if ``direct`` mode is not active, otherwise
          ``self`` for chainability. """
        if hasattr(self, 'prepare'):
            self.prepare(url_args, direct=direct)
        self.dispatch(**url_args)
        if hasattr(self, 'destroy'):
            self.destroy(self.__response__)
        if not direct:
            return self.__response__
        return self


class RealtimeHandler(Handler):
    """ Provides structure for an acyclically-dispatched web handler, meant for
      use in scenarios like WebSockets. Instead of handling things with
      methods like ``GET`` or ``POST``, a ``RealtimeHandler`` can specify
      hooks for two events - ``on_connect`` and ``on_message``.

      The first, ``on_connect``, is dispatched when a realtime connection has
      just been successfully negotiated. It is executed once the application
      is ready to return an ``HTTP/1.1 Upgrade`` response, so that the
      developer has a chance to specify subprotocols/extensions/etc.

      The second hook, ``on_message``, is dispatched each time an established
      connection receives a message from the client. It takes two parameters -
      the ``message`` itself and whether it is ``binary`` or not. """
    __socket__ = None

    def dispatch(self, **url_args):
        """ Adapt regular handler dispatch to support an acyclic/realtime-style
        dispatch scheme. Accepts same arguments as ``super`` definition, but
        dispatches *realtime*-style messages like ``on_connect`` and
        ``on_message``, so long as the request looks like a WebSocket upgrade.

        :param url_args: Arguments provided from the URI that should be passed
          along to any resulting handler calls.

        :returns: After filling the local response object (at ``self.response``)
          returns it for inspection or reply. """
        if self.realtime.hint not in self.environ:
            return super(RealtimeHandler, self).dispatch(**url_args)
        try:
            self.__socket__ = self.realtime.on_connect(self)
            self.realtime.on_message(self, self.__socket__)
        except NotImplementedError:
            return self.error(400)

    @staticmethod
    def terminate(graceful=True):
        """ Terminate the currently-active ``RealtimeSocket`` communication
        channel.

        :param graceful: ``bool`` parameter, whether to end the connection
          gracefully or not.

        :returns: ``TERMINATE`` sentinel, to be yielded so the connection can be
          terminated. """
        from canteen.logic import realtime
        if graceful:
            return realtime.TERMINATE
        raise realtime.TerminateSocket(graceful=False)

    @staticmethod
    def on_connect():
        """ Hook function that is dispatched upon successful handshake for a
        realtime-style connection between a client and this server. Local
        handler should be prepared by this point with all information necessary
        to satisfy messages.

        Implementors are expected to provide a method that makes use of object-
        level context (i.e. not a static or classmethod).

        :returns: ``NotImplemented`` by default, which simply indicates that
          the implementor elects not to run code ``on_connect``. """
        return NotImplemented

    def on_message(self, message, binary):
        """ Hook that is dispatched per message sent from a live client. Called
        subsequent to a connection being properly established from a previous
        call to ``on_connect``.

        :param message: WebSocket message passed from the client.

        :param binary: ``bool`` flag - ``True`` if ``message`` is binary,
          ``False`` otherwise.

        :raises NotImplementedError: By default, since not many people use
          WebSockets and there's no such thing as a ``400`` without HTTP. :)

        :returns: Not expected to return anything. If a return is used, any
          value or iterable of values will be collapsed and sent to the client.
          Optionally, the developer may implement ``on_message`` as a coroutine-
          style Python generator, in which case new messages will be ``sent``
          in from the client and messages to the client can be yielded upwards
          to be sent. """
        raise NotImplementedError('Handler "%s" fails to implement hook `on_message` so it does not support realtime-style communications.' % repr(self))

    @staticmethod
    def on_close(graceful):
        """ Hook function that is dispatched upon closure of an existing realtime
        communications session.

        :param graceful: ``bool`` parameter indicating whether the connection
          was closed gracefully (i.e. electively) or because of some error
          condition.

        :returns: ``NotImplemented`` by default, which simply indicates that
          the implementor elects not to run code ``on_connect``. """
        return NotImplemented


__all__ = (
 'Handler',)