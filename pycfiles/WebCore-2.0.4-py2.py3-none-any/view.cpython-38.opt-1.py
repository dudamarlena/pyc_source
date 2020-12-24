# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/core/view.py
# Compiled at: 2020-05-11 19:05:16
# Size of source mod 2**32: 6026 bytes
"""The WebCore view registry.

WebCore uses a registry of callables to transform values returned by controllers for use as a response. This
translation process is used to support the built-in types (see the `base` extension) and can be extended by your
own application to support additional types.  This is effectively the "view" component of Model-View-Controller.

A view handler takes the result of calling a controller endpoint and applies the result to the response. It can be
as simple as a bare function that accepts the current `RequestContext` instance plus the value returned by the
endpoint, and either returns a truthy value to indicate successful handling, or a falsy value to indicate that this
view handler could not handle the result. The simplest case is a handler that always "passes the buck" and handles
nothing:

        def ignore(context, result):
                pass

Slightly more useful would be to assign the result directly to the response:

        def stringy(context, result):
                context.response.text = result
                return True

As an example pulled from the "template" extension, you can use an "exit early" strategy to selectively handle
subsets of the type your view is registered against, such as only handling 2-tuples with a specific first value:

        def json(context, result):
                from json import dumps
                if len(result) != 2 or result[0] != 'json':
                        return
                context.response.text = dumps(result)
                return True

A view may go so far as to wholly replace the `context.response` object; any callable WSGI application can be
utilized as such. Cooperative response construction is _strongly_ preferred, however.

If you frequently hand back serialized data, you may be able to simplify your controller code and reduce
boilerplate by simply returning your model instances.  By registering a view handler for your model class you can
implement the serialization in a single, centralized location, making security and testing much easier.

When a controller raises an `HTTPError` subclass it is treated as the return value.  As such you can take specific
action on any given error by registering a view handler for the specific exception subclass (i.e. `HTTPNotFound`),
such as rendering a pretty error page.  By default these exceptions are treated as a WSGI application and are
directly used as the response, but only if no more specific handlers are registered.
"""
from __future__ import unicode_literals
from webob.multidict import MultiDict
from marrow.package.canonical import name
from marrow.package.host import PluginManager
from .compat import py3, pypy
log = __import__('logging').getLogger(__name__)

class WebViews(PluginManager):
    __doc__ = 'A `PluginManager` subclass to manage and search plugin and manually-registered views.\n\t\n\tThis extends plugin naming to support multiple candidates per name, overrides manual registration to log some\n\tuseful messages, and makes instances callable. Executing a `WebViews` instance passing in an object will\n\tproduce a generator yielding candidate views registered to handle that type of object.\n\t'
    __isabstractmethod__ = False

    def __init__(self, ctx):
        super(WebViews, self).__init__('web.view')
        self.__dict__['_map'] = MultiDict()

    def __repr__(self):
        """Programmers' representation for development-time diagnostics."""
        return 'WebViews({})'.format(len(self._map))

    def __call__(self, result):
        """Identify view to use based on the type of result when our instance is called as a function.
                
                This generates a stream of candidates which should be called in turn until one returns a truthy value.
                """
        rtype = type(result)
        for candidate in self._map.getall(rtype):
            (yield candidate)
        else:
            for kind, candidate in self._map.iteritems():
                if kind is rtype:
                    pass
                elif isinstance(result, kind):
                    (yield candidate)

    def register(self, kind, handler):
        """Register a handler for a given type, class, interface, or abstract base class.
                
                View registration should happen within the `start` callback of an extension.  For example, to register the
                previous `json` view example:
                
                        class JSONExtension:
                                def start(self, context):
                                        context.view.register(tuple, json)
                
                The approach of explicitly referencing a view handler isn't very easy to override without also replacing the
                extension originally adding it, however there is another approach. Using named handlers registered as discrete
                plugins (via the `entry_point` argument in `setup.py`) allows the extension to easily ask "what's my handler?"
                
                        class JSONExtension:
                                def start(self, context):
                                        context.view.register(
                                                        tuple,
                                                        context.view.json
                                                )
                
                Otherwise unknown attributes of the view registry will attempt to look up a handler plugin by that name.
                """
        if py3:
            pypy or log.debug('Registering view handler.', extra=dict(type=(name(kind)), handler=(name(handler))))
        else:
            log.debug('Registering view handler.', extra=dict(type=(repr(kind)), handler=(repr(handler))))
        self._map.add(kind, handler)
        return handler