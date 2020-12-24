# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/django_request_mapping/decorator.py
# Compiled at: 2020-03-29 00:01:48
# Size of source mod 2**32: 4387 bytes
"""
@author: sazima
@time: 2019/8/9 下午20:03
@desc:
"""
import inspect, logging
from functools import update_wrapper, partial
from django.utils.decorators import classonlymethod
from django.views import View
from django.views.decorators.csrf import csrf_exempt
logger = logging.getLogger('request_mapping.decorator')

def request_mapping(value: str, method: str='get', path_type: str='path'):
    """
    :param value: The path mapping URIs (e.g. "/myPath.do")
    :param method:  The HTTP request methods to map to, narrowing the primary mapping:
     get, post, head, options, put, patch, delete, trace
    :param path_type: path or re_path
    """

    def get_func(o, v):
        setattr(o, 'request_mapping', RequestMapping(v, method, path_type))
        if inspect.isclass(o):
            if not value.startswith('/'):
                logger.warning('values should startswith / ')
            o.as_view = as_view
        return o

    return partial(get_func, v=value)


@classonlymethod
def as_view(cls, actions=None, **initkwargs):
    """
    Because of the way class based views create a closure around the
    instantiated view, we need to totally reimplement `.as_view`,
    and slightly modify the view function that is created and returned.
    """
    cls.name = None
    cls.description = None
    cls.suffix = None
    cls.detail = None
    cls.basename = None
    if not actions:
        raise TypeError("The `actions` argument must be provided when calling `.as_view()` on a ViewSet. For example `.as_view({'get': 'list'})`")
    for key in initkwargs:
        if key in cls.http_method_names:
            raise TypeError("You tried to pass in the %s method name as a keyword argument to %s(). Don't do that." % (
             key, cls.__name__))
        if not hasattr(cls, key):
            raise TypeError('%s() received an invalid keyword %r' % (
             cls.__name__, key))

    if 'name' in initkwargs:
        if 'suffix' in initkwargs:
            raise TypeError('%s() received both `name` and `suffix`, which are mutually exclusive arguments.' % cls.__name__)

    def view(request, *args, **kwargs):
        self = cls(**initkwargs)
        self.action_map = actions
        for method, action in actions.items():
            handler = getattr(self, action)
            setattr(self, method, handler)

        if hasattr(self, 'get'):
            if not hasattr(self, 'head'):
                self.head = self.get
        self.request = request
        self.args = args
        self.kwargs = kwargs
        return (self.dispatch)(request, *args, **kwargs)

    update_wrapper(view, cls, updated=())
    update_wrapper(view, (cls.dispatch), assigned=())
    view.cls = cls
    view.initkwargs = initkwargs
    view.actions = actions
    return csrf_exempt(view)


class RequestMapping:

    def __init__(self, value: str, method: str, path_type: str):
        self.value = value
        self.method = method
        self.path_type = path_type