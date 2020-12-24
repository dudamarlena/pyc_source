# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/core/dispatch.py
# Compiled at: 2020-05-11 19:11:41
# Size of source mod 2**32: 4975 bytes
from __future__ import unicode_literals
from collections import deque
from inspect import isclass
from marrow.package.host import PluginManager
log = __import__('logging').getLogger(__name__)

class WebDispatchers(PluginManager):
    __doc__ = 'WebCore dispatch protocol adapter.\n\t\n\tThe process of resolving a request path to an endpoint. The dispatch protocol utilized is documented in full\n\tin the `protocol` project: https://github.com/marrow/protocols/blob/master/dispatch/README.md\n\t\n\tThe allowable controller structures offered by individual methods of dispatch is documented in the relevant\n\tdispatch project. Examples of dispatch include:\n\t\n\t* Object Dispatch: https://github.com/marrow/web.dispatch.object\n\t* Registered Routes: https://github.com/marrow/web.dispatch.route\n\t* Traversal: https://github.com/marrow/web.dispatch.traversal\n\t\n\tOthers may exist, and dispatch middleware may be available to perform more complex behaviours. The default\n\tdispatcher if not otherwise configured is object dispatch.\n\t'
    __isabstractmethod__ = False

    def __init__(self, ctx):
        super(WebDispatchers, self).__init__('web.dispatch')

    def __call__(self, context, handler, path):
        """Having been bound to an appropriate context, find a handler for the request path.
                
                This is the part of the WebCore request cycle that speaks the Dispatch protocol and performs event bridging.
                
                This requires a context prepared with a `context.extension.signal.dispatch` list and dispatch plugin registry
                as `context.dispatch`.  This does not use `self` to allow for more creative overriding.
                """
        is_endpoint = False
        callbacks = context.extension.signal.dispatch
        self = context.dispatch
        log.debug('Preparing dispatch.', extra=dict(request=(id(context.request)),
          path=(context.request.path_info),
          handler=(repr(handler))))
        path = path.strip('/')
        path = deque(path.split('/')) if path else deque()
        try:
            while not is_endpoint:
                dispatcher = self[getattr(handler, '__dispatch__', 'object')]
                starting = handler
                for consumed, handler, is_endpoint in dispatcher(context, handler, path):
                    if is_endpoint:
                        if not callable(handler):
                            if hasattr(handler, '__dispatch__'):
                                is_endpoint = False
                    for ext in callbacks:
                        ext(context, consumed, handler, is_endpoint)
                    else:
                        path = context.environ['PATH_INFO'].strip('/')
                        path = deque(path.split('/')) if path else deque()

                    if not is_endpoint:
                        if starting is handler:
                            break

        except LookupError:
            pass
        else:
            return (
             is_endpoint, handler if is_endpoint else None)

    def __getitem__(self, dispatcher):
        name = None
        if callable(dispatcher):
            if not isclass(dispatcher):
                return dispatcher
        if not isclass(dispatcher):
            name = dispatcher
            dispatcher = super(WebDispatchers, self).__getitem__(dispatcher)
        if isclass(dispatcher):
            dispatcher = dispatcher()
            if name:
                self.named[name] = dispatcher
        log.debug('Loaded dispatcher.', extra=dict(dispatcher=(repr(dispatcher))))
        return dispatcher