# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/ext/db.py
# Compiled at: 2019-06-09 23:33:48
# Size of source mod 2**32: 2276 bytes
"""Database connection handling extension."""
from weakref import proxy
from functools import partial
from core.context import ContextGroup

class DatabaseExtension:
    _provides = {
     'db'}

    def __init__(self, default=None, **engines):
        """Configure the database management extension."""
        if default is not None:
            engines['default'] = default
        self.engines = engines
        self.uses = set()
        self.needs = set()
        self.provides = set(self._provides)
        for name, engine in engines.items():
            if not getattr(engine, 'alias', None):
                engine.alias = name
            self.uses.update(getattr(engine, 'uses', ()))
            self.needs.update(getattr(engine, 'needs', ()))
            self.provides.update(getattr(engine, 'provides', ()))

        super().__init__()

    def start(self, context):
        context.db = ContextGroup(**self.engines)
        self._handle_event('start', context)

    def prepare(self, context):
        context.db = context.db._promote('Databases')
        context.db['_ctx'] = proxy(context)
        self._handle_event('prepare', context)

    def _handle_event(self, event, *args, **kw):
        """Broadcast an event to the database connections registered."""
        for engine in self.engines.values():
            if hasattr(engine, event):
                (getattr(engine, event))(*args, **kw)

    def __getattr__(self, name):
        """Allow the passing through of the events we don't otherwise trap to our database connection providers."""
        if name.startswith('_'):
            raise AttributeError()
        for engine in self.engines.values():
            if name in dir(engine):
                return partial(self._handle_event, name)

        raise AttributeError()


class DBExtension(DatabaseExtension):

    def __init__(self, *args, **kw):
        (super().__init__)(*args, **kw)
        from warnings import warn
        warn('DBExtension is deprecated, use DatabaseExtension instead.', DeprecationWarning)