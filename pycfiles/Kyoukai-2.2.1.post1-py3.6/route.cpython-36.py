# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kyoukai/route.py
# Compiled at: 2017-09-29 12:38:41
# Size of source mod 2**32: 10210 bytes
"""
Routes are wrapped function objects that are called upon a HTTP request.
"""
import collections, inspect, types, typing
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Rule, Submount
from werkzeug.wrappers import Response
from kyoukai.util import wrap_response

class Route(object):
    __doc__ = '\n    A route object is a wrapped function.\n    They invoke this function when invoked on routing and calling.\n    '

    def __init__(self, function, *, reverse_hooks: bool=False, should_invoke_hooks: bool=True, do_argument_checking: bool=True, endpoint: str=None):
        """        
        :param function: The underlying callable.
            This can be a function, or any other callable.

        :param reverse_hooks: If the request hooks should be reversed for this request (i.e child          to parent.)
        
        :param should_invoke_hooks: If request hooks should be invoked.
            This is automatically False for error handlers.
        
        :param do_argument_checking: If argument type and name checking is enabled for this route.
        
        :param endpoint: The custom endpoint for this route.
        """
        if not callable(function):
            raise TypeError('Route arg must be callable')
        self._callable = function
        self.do_argument_checking = do_argument_checking
        self.bp = None
        self.routes = []
        self.endpoint = endpoint
        self.reverse_hooks = reverse_hooks
        self.should_invoke_hooks = should_invoke_hooks
        self.hooks = {}

    @property
    def callable_repr(self):
        return repr(self._callable)

    def add_path(self, url: str, methods: typing.Sequence[str]=('GET', 'HEAD')):
        """
        Adds a path to the current set of paths for this route.

        :param url: The routing URL to add.
        :param methods: An iterable of methods to use for this path.

        The URL and methods will be added as a pair.
        """
        self.routes.append((url, methods))
        return self

    def get_submount(self) -> Submount:
        """
        :return: A submount that represents this route.
        
        .. versionadded:: 2.2.0

        .. versionchanged:: 2.x.x

            Changed from getting a list of rules to a single submount object.
        """
        rules = []
        for url, methods in self.routes:
            methods = list(methods)
            if 'OPTIONS' not in methods:
                methods.append('OPTIONS')
            rule = Rule(url, methods=methods, host=(self.bp.host if self.bp is not None else None),
              endpoint=(self.get_endpoint_name()))
            rules.append(rule)

        submount = Submount('', rules)
        return submount

    def get_endpoint_name(self, bp=None) -> str:
        """
        Gets the endpoint name for this route.
        
        :param bp: The :class:`.Blueprint` to use for name calculation.
        :return: The endpoint that can be used.
        """
        if self.endpoint is not None:
            return self.endpoint
        else:
            if bp is not None:
                prefix = bp.name
            else:
                prefix = self.bp.name if self.bp else ''
            return '{}.{}'.format(prefix, self._callable.__name__)

    async def invoke_function(self, ctx, pre_hooks: list, post_hooks: list, params):
        """
        Invokes the underlying callable.
        This is for use in chaining routes.

        :param ctx: The :class:`~.HTTPRequestContext` to use for this route.
        :param pre_hooks: A list of hooks to call before the route is invoked.
        :param post_hooks: A list of hooks to call after the route is invoked.
        :param params: The parameters to pass to the function.
        :return: The result of the invoked function.
        """
        try:
            if self.should_invoke_hooks:
                for hook in pre_hooks:
                    _ = await hook(ctx)
                    if _ is not None:
                        ctx = _

            else:
                if isinstance(params, collections.Mapping):
                    result = (self._callable)(ctx, **params)
                else:
                    result = (self._callable)(ctx, *params)
            if inspect.isawaitable(result):
                result = await result
            result = wrap_response(result, ctx.app.response_class)
        except HTTPException as e:
            raise e
        else:
            if self.should_invoke_hooks:
                for hook in post_hooks:
                    _ = await hook(ctx, result)
                    if _ is not None:
                        result = _

            return result

    def check_route_args(self, params: dict=None):
        """
        Checks the arguments for a route.

        :param params: The parameters passed in, as a dict.
        :raises TypeError: If the arguments passed in were not correct.
        """
        sig = inspect.signature((self._callable), follow_wrapped=True)
        f_nargs = len(sig.parameters) - 1
        if f_nargs < 0:
            raise TypeError('Route functions must take ctx argument')
        if f_nargs != len(params):
            raise TypeError('Route takes {} args, passed in {} instead'.format(f_nargs, len(params)))
        for n, (name, arg) in enumerate(sig.parameters.items()):
            if n == 0:
                pass
            else:
                if isinstance(self._callable, types.MethodType):
                    if n == 1:
                        continue
                else:
                    assert isinstance(arg, inspect.Parameter)
                    if arg.name not in params:
                        raise ValueError('Argument {} not found in args for callable {}'.format(arg.name, self._callable.__name__))
                value = params[arg.name]
                if arg.annotation is None or arg.annotation is inspect.Parameter.empty:
                    pass
                else:
                    if not isinstance(value, arg.annotation):
                        raise TypeError('Argument {} must be type {} (got type {})'.format(arg.name, arg.annotation, type(value)))

    def add_hook(self, type_: str, hook):
        """
        Adds a hook to the current Route.

        :param type_: The type of hook to add (currently "pre" or "post").
        :param hook: The callable function to add as a hook.
        """
        if type_ not in self.hooks:
            self.hooks[type_] = []
        self.hooks[type_].append(hook)
        return hook

    def get_hooks(self, type_: str):
        """
        Gets the hooks for the current Route for the type.
        
        :param type_: The type to get. 
        :return: A list of callables.
        """
        return self.hooks.get(type_, [])

    def before_request(self, func):
        """
        Convenience decorator to add a pre-request hook.
        """
        return self.add_hook(type_='pre', hook=func)

    def after_request(self, func):
        """
        Convenience decorator to add a post-request hook.
        """
        return self.add_hook(type_='post', hook=func)

    async def invoke(self, ctx, args: typing.Iterable[typing.Any]=(), params: typing.Container=None) -> Response:
        """
        Invokes a route.
        This will run the underlying function.
        
        :param ctx: The :class:`~.HTTPRequestContext` which is used in this request.
        :param args: Any args to expand into the function.
        :param params: Any keyword params that are used in this request.

        :return: The result of the route's function.
        """
        if params is None:
            params = {}
        else:
            ctx.route = self
            if not params:
                params = {}
            elif self.do_argument_checking and not args:
                self.check_route_args(params)
            else:
                params = list(args) + list(params.values())
            pre_hooks = self.bp.get_hooks('pre').copy()
            if self.reverse_hooks:
                pre_hooks = list(reversed(pre_hooks))
            post_hooks = self.bp.get_hooks('post').copy()
            if self.reverse_hooks:
                post_hooks = list(reversed(post_hooks))
        pre_hooks += self.get_hooks('pre').copy()
        post_hooks += self.get_hooks('post').copy()
        return await self.invoke_function(ctx, pre_hooks, post_hooks, params)