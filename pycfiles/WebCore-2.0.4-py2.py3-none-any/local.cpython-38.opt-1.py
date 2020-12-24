# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/ext/local.py
# Compiled at: 2020-05-11 19:05:16
# Size of source mod 2**32: 2353 bytes
from __future__ import unicode_literals
from threading import local
from marrow.package.loader import traverse
log = __import__('logging').getLogger(__name__)

class ThreadLocalExtension(object):
    __doc__ = 'Provide the current context as a thread local global.\n\t\n\tThis provides a convienent "superglobal" variable where you can store per-thread data.\n\t\n\tWhile the context itself is cleaned up after each call, any data you add won\'t be.  These are not request-locals.\n\t'
    first = True
    provides = ['local', 'threadlocal']

    def __init__(self, where='web.core:local'):
        """Initialize thread local storage for the context.
                
                By default the `local` object in the `web.core` package will be populated as a `threading.local` pool. The
                context, during a request, can then be accessed as `web.core.local.context`. Your own extensions can add
                additional arbitrary data to this pool.
                """
        super(ThreadLocalExtension, self).__init__()
        log.debug('Initalizing ThreadLocal extension.')
        self.where = where
        self.local = None
        self.preserve = False

    def _lookup(self):
        module, _, name = self.where.rpartition(':')
        module = traverse((__import__(module)), ('.'.join(module.split('.')[1:])), separator='.')
        return (
         module, name)

    def start(self, context):
        module, name = self._lookup()
        log.debug('Preparing thread local storage and assigning main thread application context.')
        if hasattr(module, name):
            self.local = getattr(module, name)
            self.preserve = True
        else:
            self.local = local()
            setattr(module, name, self.local)
        self.local.context = context

    def stop(self, context):
        self.local = None
        log.debug('Cleaning up thread local storage.')
        if not self.preserve:
            module, name = self._lookup()
            delattr(module, name)

    def prepare(self, context):
        """Executed prior to processing a request."""
        log.debug('Assigning thread local request context.')
        self.local.context = context

    def done(self, result):
        """Executed after the entire response has been sent to the client."""
        log.debug('Cleaning up thread local request context.')
        del self.local.context