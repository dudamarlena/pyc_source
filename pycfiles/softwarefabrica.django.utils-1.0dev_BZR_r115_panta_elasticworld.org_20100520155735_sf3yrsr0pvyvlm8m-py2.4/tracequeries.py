# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/utils/tracequeries.py
# Compiled at: 2009-11-08 05:06:55
from django.conf import settings
from django.db import backends
import logging
DEFAULT_SLOW_QUERY_TIME = 0.01
_original_settings_DEBUG = settings.DEBUG
_original_CursorDebugWrapper = backends.util.CursorDebugWrapper
_slow_query_time = getattr(settings, 'SLOW_QUERY_TIME', DEFAULT_SLOW_QUERY_TIME)

class CursorTracingDebugWrapper(backends.util.CursorDebugWrapper):
    __module__ = __name__
    _on_execute_callback = None
    _on_executemany_callback = None
    _on_query_callback = None
    _do_log = False

    def __init__(self, cursor, db, on_execute_callback=None, on_executemany_callback=None, on_query_callback=None, log=None):
        super(CursorTracingDebugWrapper, self).__init__(cursor, db)
        if on_execute_callback is not None:
            self._on_execute_callback = on_execute_callback
        if on_executemany_callback is not None:
            self._on_executemay_callback = on_executemany_callback
        if on_query_callback is not None:
            self._on_query_callback = on_query_callback
        if log is not None:
            self._do_log = log
        return

    def execute(self, sql, params=()):
        r = super(CursorTracingDebugWrapper, self).execute(sql, params)
        if self._on_execute_callback is not None:
            f = self._on_execute_callback.im_func
            apply(f, (self, sql, params, self.db.queries[(-1)]))
        if self._on_query_callback is not None:
            f = self._on_query_callback.im_func
            apply(f, (self, sql, params, self.db.queries[(-1)]))
        if self._do_log:
            logging.debug(self.db.queries[(-1)])
        return r

    def executemany(self, sql, param_list):
        r = super(CursorTracingDebugWrapper, self).executemany(sql, param_list)
        if self._on_executemany_callback is not None:
            f = self._on_executemany_callback.im_func
            apply(f, (self, sql, param_list, self.db.queries[(-1)]))
        if self._on_query_callback is not None:
            f = self._on_query_callback.im_func
            apply(f, (self, sql, param_list, self.db.queries[(-1)]))
        if self._do_log:
            logging.debug(self.db.queries[(-1)])
        return r


def start_tracing_queries(on_execute_callback=None, on_executemany_callback=None, on_query_callback=None, log=None):
    """Start tracing SQL queries."""
    global _original_settings_DEBUG
    global _slow_query_time
    _slow_query_time = getattr(settings, 'SLOW_QUERY_TIME', DEFAULT_SLOW_QUERY_TIME)
    if on_execute_callback is not None:
        CursorTracingDebugWrapper._on_execute_callback = on_execute_callback
    if on_executemany_callback is not None:
        CursorTracingDebugWrapper._on_executemany_callback = on_executemany_callback
    if on_query_callback is not None:
        CursorTracingDebugWrapper._on_query_callback = on_query_callback
    if log is not None:
        CursorTracingDebugWrapper._do_log = log
    _original_settings_DEBUG = settings.DEBUG
    settings.DEBUG = True
    backends.util.CursorDebugWrapper = CursorTracingDebugWrapper
    return


def stop_tracing_queries():
    """Stop tracing SQL queries."""
    backends.util.CursorDebugWrapper = _original_CursorDebugWrapper
    settings.DEBUG = _original_settings_DEBUG


def log_slow_queries_cb(cursor_wrapper, sql, params_or_list, last_query):
    if float(last_query['time']) > float(_slow_query_time):
        logging.debug('\nSLOW QUERY:\n\t%s\n' % last_query)