# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sovereign/logs.py
# Compiled at: 2020-04-29 02:35:50
# Size of source mod 2**32: 1841 bytes
import structlog
from structlog.exceptions import DropEvent
import threading
from sovereign import config
THREADLOCAL = threading.local()

def _ensure_threadlocal():
    THREADLOCAL.context = getattr(THREADLOCAL, 'context', {})


def merge_log_context_in_thread(logger, method_name, event_dict):
    """
    This processor takes a dict from thread-local context,
    merges it, and returns it to structlog so that it can emit a
    log message, complete with context from different parts
    of the application.
    """
    _ensure_threadlocal()
    context = THREADLOCAL.context.copy()
    context.update(event_dict)
    return context


def new_log_context():
    THREADLOCAL.context = {}


def add_log_context(**kwargs):
    _ensure_threadlocal()
    THREADLOCAL.context.update(kwargs)


class AccessLogsEnabled:

    def __call__(self, logger, method_name, event_dict):
        if not config.enable_access_logs:
            raise DropEvent
        return event_dict


class FilterDebugLogs:

    def __call__(self, logger, method_name, event_dict):
        if event_dict.get('level') == 'debug':
            if not config.debug_enabled:
                raise DropEvent
        return event_dict


structlog.configure(processors=[
 AccessLogsEnabled(),
 merge_log_context_in_thread,
 structlog.stdlib.add_log_level,
 FilterDebugLogs(),
 structlog.processors.JSONRenderer()])
LOG = structlog.getLogger()