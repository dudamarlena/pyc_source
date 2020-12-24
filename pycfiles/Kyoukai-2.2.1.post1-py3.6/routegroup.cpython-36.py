# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kyoukai/routegroup.py
# Compiled at: 2017-09-29 12:38:41
# Size of source mod 2**32: 7738 bytes
"""
Route groups are classes that allow you to group a set of routes together.

.. currentmodule:: kyoukai.routegroup
"""
import collections, inspect, typing

def get_rg_bp(group: 'RouteGroup'):
    """
    Gets the :class:`~.Blueprint` created from a :class:`~.RouteGroup`.
    """
    return getattr(group, '_{0.__name__}__blueprint'.format(type(group)))


class RouteGroupType(type):
    __doc__ = '\n    The metaclass for a route group.\n    \n    This is responsible for passing the keyword arguments to the metaclass.\n    '

    def __new__(mcs, name, bases, class_body, **kwargs):
        return super().__new__(mcs, name, bases, class_body)

    def __init__(self, name, bases, class_body, **kwargs):
        super().__init__(name, bases, class_body)
        self._bp_kwargs = kwargs

    def _init_blueprint(self, obb):
        """
        Initializes the Blueprint used by this route group.
        
        :param obb: The route group instance to intialize. 
        """
        from kyoukai.blueprint import Blueprint
        bp = Blueprint((self.__name__), **self._bp_kwargs)
        for name, value in inspect.getmembers(obb):
            if not hasattr(value, '__func__'):
                pass
            else:
                func = value.__func__
                if getattr(func, 'in_group', False) is True:
                    pass
            if func.rg_delegate == 'route':
                rtt = (bp.wrap_route)(value, **func.route_kwargs)
                rtt.routes = func.routes
                rtt.bp = bp
                for type_, hooks in func.route_hooks.items():
                    for hook in hooks:
                        rtt.add_hook(type_, hook)

                bp.routes.append(rtt)
            else:
                if func.rg_delegate == 'errorhandler':
                    for code in func.errorhandler_codes:
                        bp.add_errorhandler(value, code)

                else:
                    if func.rg_delegate == 'hook':
                        bp.add_hook(func.hook_type, value)

        setattr(obb, '_{.__name__}__blueprint'.format(self), bp)

    def __call__(self, *args, **kwargs):
        obb = object.__new__(self)
        (obb.__init__)(*args, **kwargs)
        self._init_blueprint(obb)
        return obb


def route(url: str, methods: typing.Iterable[str]=('GET', 'HEAD'), **kwargs):
    """
    A companion function to the RouteGroup class. This follows :meth:`.Blueprint.route` in 
    terms of arguments, and marks a function as a route inside the class.
    
    This will return the original function, with some attributes attached:
    
        - ``in_group``: Marks the function as in the route group.
        - ``rg_delegate``: Internal. The type of function inside the group this is.
        - ``route_kwargs``: Keyword arguments to provide to ``wrap_route``.
        - ``route_url``: The routing URL to provide to ``add_route``.
        - ``route_methods``: The methods for the route.
        - ``route_hooks``: A defaultdict of route-specific hooks.
        
    Additionally, the following methods are added.
    
        - ``hook``: A decorator that adds a hook of type ``type_``.
        - ``before_request``: A decorator that adds a ``pre`` hook.
        - ``after_request``: A decorator that adds a ``post`` hook.
    
    .. versionadded:: 2.1.1
    
    .. versionchanged:: 2.1.3
    
        Added the ability to add route-specific hooks.
        
    .. versionchanged:: 2.2.0
        
        Now accepts an already edited function as the function to decorate - this will add a new         routing url and method pair to the :attr:`.Route.routes`.

    .. versionchanged:: 2.2.2

        Default methods changed to GET and HEAD.
    
    :param url: The routing URL of the route.
    :param methods: An iterable of methods for the route.
    """

    def inner(func):
        func.in_group = True
        func.rg_delegate = 'route'
        func.route_kwargs = kwargs
        try:
            func.routes.append((url, methods))
        except AttributeError:
            func.routes = [
             (
              url, methods)]

        if not hasattr(func, 'route_hooks'):
            func.route_hooks = collections.defaultdict(lambda : [])

            def hook(type_):

                def _inner2(hookfunc):
                    func.route_hooks[type_].append(hookfunc)
                    return hookfunc

                return _inner2

            func.hook = hook
            func.before_request = hook('pre')
            func.after_request = hook('post')
        return func

    return inner


def errorhandler(startcode: int, endcode: int=None, step: int=None):
    """
    A companion function to the RouteGroup class. This follows :meth:`.Blueprint.errorhandler` in 
    terms of arguments. 
    
    :param startcode: The error code to handle, for example 404.
        This also represents the start of an error range, if endcode is not None.
    :param endcode: The end of the error code range to handle. Error handlers will be added
        for all requests between startcode and endcode.
    :param step: The step for the error handler range.
    """

    def inner(func):
        func.in_group = True
        func.rg_delegate = 'errorhandler'
        if endcode is None:
            codes = [
             startcode]
        else:
            codes = range(startcode, endcode, step or 1)
        for code in codes:
            try:
                func.errorhandler_codes.append(code)
            except AttributeError:
                func.errorhandler_codes = [
                 code]

        return func

    return inner


def hook(type_: str):
    """
    Marks a function as a hook.
    
    :param type_: The type of hook to mark. 
    """

    def inner(func):
        func.in_group = True
        func.rg_delegate = 'hook'
        func.hook_type = type_
        return func

    return inner


def before_request(func):
    """
    Helper decorator to mark a function as a pre-request hook. 
    """
    return hook('pre')(func)


def after_request(func):
    """
    Helper decorator to mark a function as a post-request hook. 
    """
    return hook('post')(func)


class RouteGroup(object, metaclass=RouteGroupType):
    __doc__ = '\n    A route group is a class that contains multiple methods that are decorated with the route \n    decorator. They produce a blueprint that can be added to the tree that includes all methods \n    in the route group.\n     \n    .. code-block:: python\n    \n        class MyGroup(RouteGroup, prefix="/api/v1"):\n            def __init__(self, something: str):\n                self.something = something\n                \n            @route("/ping")\n            async def ping(self, ctx: HTTPRequestContext):\n                return \'{"response": self.something}\'\n                \n    Blueprint parameters can be passed in the class call.\n    \n    To add the route group as a blueprint, use \n    :meth:`.Blueprint.add_route_group(MyGroup, *args, **kwargs)`.\n    '