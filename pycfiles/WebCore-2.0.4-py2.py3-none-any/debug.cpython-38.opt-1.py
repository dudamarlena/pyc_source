# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/ext/debug.py
# Compiled at: 2020-05-11 19:05:16
# Size of source mod 2**32: 2164 bytes
"""Web-based REPL shell and interactive debugger extension."""
from __future__ import unicode_literals
from webob.exc import HTTPNotFound
from backlash import DebuggedApplication
log = __import__('logging').getLogger(__name__)

class Console(object):
    __doc__ = 'Attach a console to your web application at an arbitrary location.'
    __slots__ = ('debugger', 'request')

    def __init__(self, context):
        self.debugger = context.get('debugger', None)
        self.request = context.request

    def __call__(self, *args, **kw):
        if not self.debugger:
            raise HTTPNotFound()
        return self.debugger.display_console(self.request)


class DebugExtension(object):
    __doc__ = 'Enable an interactive exception debugger and interactive console.\n\t\n\tPossible configuration includes:\n\t\n\t\t* `path` -- the path to the interactive console, defaults to: `/__console__`\n\t\t* `verbose` -- show ordinarily hidden stack frames, defaults to: `False`\n\t'
    __slots__ = ('path', 'verbose')
    provides = [
     'debugger', 'console']

    def __init__(self, path='/__console__', verbose=False):
        log.debug('Initializing debugger extension.')
        self.path = path
        self.verbose = verbose
        super(DebugExtension, self).__init__()

    def init_console(self):
        """Add variables to the console context."""
        return dict()

    def init_debugger(self, environ):
        """Add variables to the debugger context."""
        return dict(context=(environ.get('context')))

    def __call__(self, context, app):
        """Executed to wrap the application in middleware.
                
                The first argument is the application context, not request context.
                
                Accepts a WSGI application as the second argument and must likewise return a WSGI app.
                """
        log.debug('Wrapping application in debugger middleware.')
        app = DebuggedApplication(app,
          evalex=True,
          show_hidden_frames=(self.verbose),
          console_init_func=(self.init_console),
          context_injectors=[
         self.init_debugger])
        context.debugger = app
        return app