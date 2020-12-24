# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kyoukai/app.py
# Compiled at: 2018-02-07 20:03:19
# Size of source mod 2**32: 15848 bytes
"""
The core application.
"""
import asyncio, logging, traceback
from asphalt.core import Context, run_application
from werkzeug.exceptions import NotFound, MethodNotAllowed, HTTPException, InternalServerError, BadRequestKeyError
from werkzeug.routing import RequestRedirect, Map
from werkzeug.wrappers import Request, Response
from kyoukai.asphalt import HTTPRequestContext
from kyoukai.blueprint import Blueprint
__version__ = '2.2.1.post1'
version_format = 'Kyoukai/{}'.format(__version__)
logger = logging.getLogger('Kyoukai')

class Kyoukai(object):
    __doc__ = '\n    The Kyoukai type is the core of the Kyoukai framework, and the core of your web application \n    based upon the Kyoukai framework. It acts as a central router and request processor that \n    takes in requests from the protocols and returns responses.\n\n    The application name is currently unused, but it is good practice to set it correctly anyway in \n    case it is used in future editions of Kyoukai.\n\n    You normally create an application instance inside your component file, like so:\n\n    .. code-block:: python\n\n        from kyoukai.app import Kyoukai\n\n        ... # setup code\n\n        kyk = Kyoukai("my_app")\n        kyk.register_blueprint(whatever)\n\n        ... # other setup\n\n        class MyContainer(ContainerComponent):\n            async def start(self, ctx):\n                self.add_component(\'kyoukai\', KyoukaiComponent, ip="127.0.0.1", port=4444,\n                                   app="app:app")\n\n    Of course, you can also embed Kyoukai inside another app, by awaiting :meth:`Kyoukai.start`.\n    '
    request_class = Request
    response_class = Response

    def __init__(self, application_name: str, *, server_name: str=None, **kwargs):
        r"""
        :param application_name: The name of the application that is being created. This is \ 
            passed to the :class:`.Blueprint` being created as the root blueprint.  
            
            This is used in ``url_for``, for example, to get the endpoint of routes registered to             the root Blueprint.
            
        :param server_name: Keyword-only. The SERVER_NAME to use inside the fake WSGI environment             created for ``url_for``, if applicable.
            
        :param host_matching: Should host matching be enabled? This will be implicitly True if             ``host`` is not None.
            
        :param host: The host used for host matching, to be passed to the root Blueprint.
            By default, no host is used, so all hosts are matched on the root Blueprint.
            
        :param application_root: Keyword-only. The APPLICATION_ROOT to use inside the fake WSGI \ 
            environment created for ``url_for``, if applicable.
        
        :param loop: Keyword-only. The asyncio event loop to use for this app. If no loop is \ 
            specified it, will be automatically fetched using :meth:`asyncio.get_event_loop`.
        
        :param request_class: Keyword-only. The custom request class to instantiate requests with.
        :param response_class: Keyword-only. The custom response class to instantiate responses \ 
            with.

        :param context_class: Keyword-only. The :class:`.Context` subclass to use when creating a             context. Defaults to :class:`.HTTPRequestContext`.
        """
        self.name = application_name
        self.server_name = server_name
        self.loop = kwargs.pop('loop', None)
        if not self.loop:
            self.loop = asyncio.get_event_loop()
        self._root_bp = Blueprint(application_name, host=(kwargs.get('host')), host_matching=(kwargs.get('host_matching', False)))
        self.component = None
        self.request_class = kwargs.pop('request_class', self.request_class)
        self.response_class = kwargs.pop('response_class', self.response_class)
        self.context_class = kwargs.pop('context_class', HTTPRequestContext)
        self.debug = False
        self.config = kwargs

    @property
    def root(self) -> Blueprint:
        """
        :return: The root Blueprint for the routing tree.
        """
        return self._root_bp

    def register_blueprint(self, child: Blueprint):
        """
        Registers a child blueprint to this app's root Blueprint.

        This will set up the Blueprint tree, as well as setting up the routing table when finalized.
        
        :param child: The child Blueprint to add. This must be an instance of :class:`~.Blueprint`.
        """
        return self.root.add_child(child)

    def finalize(self, **map_options) -> Map:
        """
        Finalizes the app and blueprints.

        This will calculate the current :class:`werkzeug.routing.Map` which is required for 
        routing to work.
        
        :param map_options: The options to pass to the Map for routing.
        """
        self.debug = self.config.get('debug', False)
        return (self.root.finalize)(**map_options)

    def __getattr__(self, item: str) -> object:
        """
        Override for __getattr__ to allow transparent mirroring onto the root Blueprint.

        For example, this allows doing ``@app.route`` instead of ``@app.root.route``.
        """
        if item in ('route', 'errorhandler', 'add_errorhandler', 'add_route', 'wrap_route',
                    'url_for', 'before_request', 'add_hook', 'after_request', 'add_route_group'):
            return getattr(self.root, item)
        raise AttributeError("'{.__class__.__name__}' object has no attribute {}".format(self, item))

    def log_route(self, request: Request, code: int):
        """
        Logs a route invocation.

        :param request: The request produced.
        :param code: The response code of the route.
        """
        fmtted = '{} {} - {}'.format(request.method, request.path, code)
        logger.info(fmtted)

    async def handle_httpexception(self, ctx: HTTPRequestContext, exception: HTTPException, environ: dict=None) -> Response:
        """
        Handle a HTTP Exception.

        :param ctx: The context of the request.
        :param exception: The HTTPException to handle.
        :param environ: The fake WSGI environment.
        
        :return: A :class:`werkzeug.wrappers.Response` that handles this response.
        """
        bp = ctx.bp or self.root
        if environ is None:
            environ = ctx.environ
        else:
            cbl = lambda environ: Response('Internal server error during processing. Report this.', status=500)
            error_handler = bp.get_errorhandler(exception)
            if not error_handler:
                error_handler = self.root.get_errorhandler(exception)
                if not error_handler:
                    cbl = exception.get_response
            else:
                try:
                    res = await error_handler.invoke(ctx, args=(exception,))
                    cbl = lambda environ: res
                except HTTPException as e:
                    logger.warning('Error handler function raised another error, using the response from that...')
                    cbl = e.get_response
                except Exception as e:
                    logger.exception('Error in error handler!')
                    cbl = InternalServerError(e).get_response

        try:
            result = cbl(environ=environ)
        except Exception:
            logger.critical(('Whilst handling a {}, response.get_response ({}) raised exception'.format(exception.code, cbl)),
              exc_info=True)
            result = Response('Critical server error. Your application is broken.', status=500)

        if result.status_code != exception.code:
            logger.warning('Error handler {} returned code {} when exception was code {}...'.format(error_handler.callable_repr, result.status_code, exception.code))
            return result

    async def process_request(self, request: Request, parent_context: Context) -> Response:
        r"""
        Processes a Request and returns a Response object.

        This is the main processing method of Kyoukai, and is meant to be used by one of the HTTP 
        server backends, and not by client code.

        :param request:             The :class:`werkzeug.wrappers.Request` object to process.
            A new :class:`~.HTTPRequestContext` will be provided to wrap this request inside of \ 
            to client code.

        :param parent_context:             The :class:`asphalt.core.Context` that is the parent context for this particular app. 
            It will be used as the parent for the HTTPRequestContext.

        :return: A :class:`werkzeug.wrappers.Response` object that can be written to the client \ 
            as a response.
        """
        if not self.root.finalized:
            raise RuntimeError('App was not finalized')
        ctx = self.context_class(parent_context, request)
        ctx.app = self
        async with ctx:
            try:
                matched, params, rule = self.root.match(request.environ)
                ctx.params = params
                ctx.rule = rule
            except NotFound as e:
                self.log_route(ctx.request, 404)
                logger.debug('Could not resolve route for {request.path}.'.format(request=request))
                return await self.handle_httpexception(ctx, e, request.environ)
            except MethodNotAllowed as e:
                self.log_route(ctx.request, 405)
                logger.debug('Could not resolve valid method for {request.path} ({request.method})'.format(request=request))
                return await self.handle_httpexception(ctx, e, request.environ)
            except RequestRedirect as e:
                self.log_route(ctx.request, 307)
                e.code = 307
                return e.get_response(request.environ)
            else:
                ctx.route_matched.dispatch(ctx=ctx)
            ctx.route = matched
            ctx.bp = ctx.route.bp
            result = None
            try:
                try:
                    ctx.route_invoked.dispatch(ctx=ctx)
                    if ctx.request.method.upper() == 'OPTIONS':
                        result = Response(status=204)
                        result.headers['Allow'] = ','.join(x for x in ctx.rule.methods if x != 'OPTIONS')
                    else:
                        result = await matched.invoke(ctx, params=params)
                except BadRequestKeyError as e:
                    logger.info(('BadRequestKeyError: {}'.format(' '.join(e.args))), exc_info=True)
                    result = await self.handle_httpexception(ctx, e, request.environ)
                except HTTPException as e:
                    fmtted = traceback.format_exception(type(e), e, e.__traceback__)
                    logger.debug(''.join(fmtted))
                    logger.info('Hit HTTPException ({}) inside function, delegating.'.format(str(e)))
                    result = await self.handle_httpexception(ctx, e, request.environ)
                except Exception as e:
                    logger.exception('Unhandled exception in route function')
                    new_e = InternalServerError()
                    new_e.__cause__ = e
                    result = await self.handle_httpexception(ctx, new_e, request.environ)
                else:
                    ctx.route_completed.dispatch(ctx=ctx, result=result)
            finally:
                if result:
                    self.log_route(ctx.request, result.status_code)

            result.headers['Server'] = version_format
            if not isinstance(result.response, (bytes, str, list)):
                result.set_data(str(result.response))
            result.headers['X-Powered-By'] = version_format
            return result

    async def start(self, ip: str='127.0.0.1', port: int=4444, *, component=None, base_context: Context=None):
        """
        Runs the Kyoukai component asynchronously.

        This will bypass Asphalt's default runner, and allow you to run your app easily inside 
        something else, for example.

        :param ip: The IP of the built-in server.
        :param port: The port of the built-in server.
        :param component: The component to start the app with. This should be an instance of             :class:`~.KyoukaiComponent`.
                    
        :param base_context: The base context that the HTTPRequestContext should be started with.
        """
        if not base_context:
            base_context = Context()
        else:
            if not component:
                from kyoukai.asphalt import KyoukaiComponent
                self.component = KyoukaiComponent(self, ip, port)
            else:
                self.component = component
        await self.component.start(base_context)

    def run(self, ip: str='127.0.0.1', port: int=4444, *, component=None):
        """
        Runs the Kyoukai server from within your code.

        This is not normally invoked - instead Asphalt should invoke the Kyoukai component.
        However, this is here for convenience.
        """
        if not component:
            from kyoukai.asphalt import KyoukaiComponent
            component = KyoukaiComponent(self, ip, port)
        run_application(component)