# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/logging/handlers.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import logging, re, six
from django.utils.timezone import now
from simplejson import JSONEncoder
from structlog import get_logger
from structlog.processors import _json_fallback_handler
from sentry.utils import metrics
_default_encoder = JSONEncoder(separators=(',', ':'), ignore_nan=True, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, indent=None, encoding='utf-8', default=_json_fallback_handler).encode
throwaways = frozenset(('threadName', 'thread', 'created', 'process', 'processName',
                        'args', 'module', 'filename', 'levelno', 'exc_text', 'msg',
                        'pathname', 'lineno', 'funcName', 'relativeCreated', 'levelname',
                        'msecs'))

class JSONRenderer(object):

    def __call__(self, logger, name, event_dict):
        return _default_encoder(event_dict)


class HumanRenderer(object):

    def __call__(self, logger, name, event_dict):
        level = event_dict.pop('level')
        real_level = level.upper() if isinstance(level, six.string_types) else logging.getLevelName(level)
        base = '%s [%s] %s: %s' % (
         now().strftime('%H:%M:%S'),
         real_level,
         event_dict.pop('name', 'root'),
         event_dict.pop('event', ''))
        join = (' ').join(k + '=' + repr(v) for k, v in six.iteritems(event_dict))
        return '%s%s' % (base, ' (%s)' % join if join else '')


class StructLogHandler(logging.StreamHandler):

    def emit(self, record, logger=None):
        if logger is None:
            logger = get_logger()
        kwargs = {k:v for k, v in six.iteritems(vars(record)) if k not in throwaways and v is not None if k not in throwaways and v is not None}
        kwargs.update({'level': record.levelno, 'event': record.msg})
        if record.args:
            if isinstance(record.args, (tuple, list)):
                kwargs['positional_args'] = record.args
            else:
                kwargs['positional_args'] = (
                 record.args,)
        logger.log(**kwargs)
        return


class MessageContainsFilter(logging.Filter):
    """
    A logging filter that allows log records where the message
    contains given substring(s).

    contains -- a string or list of strings to match
    """

    def __init__(self, contains):
        if not isinstance(contains, list):
            contains = [
             contains]
        if not all(isinstance(c, six.string_types) for c in contains):
            raise TypeError("'contains' must be a string or list of strings")
        self.contains = contains

    def filter(self, record):
        message = record.getMessage()
        return any(c in message for c in self.contains)


whitespace_re = re.compile('\\s+')
metrics_badchars_re = re.compile('[^a-z0-9_.]')

class MetricsLogHandler(logging.Handler):

    def emit(self, record, logger=None):
        """
        Turn something like:
            > django.request.Forbidden (CSRF cookie not set.): /account
        into:
            > django.request.forbidden_csrf_cookie_not_set
        and track it as an incremented counter.
        """
        key = record.name + '.' + record.getMessage()
        key = key.lower()
        key = whitespace_re.sub('_', key)
        key = metrics_badchars_re.sub('', key)
        key = ('.').join(key.split('.')[:3])
        metrics.incr(key, skip_internal=False)