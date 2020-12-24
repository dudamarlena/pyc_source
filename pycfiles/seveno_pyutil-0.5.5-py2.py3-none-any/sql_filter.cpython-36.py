# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomislav/dev/seveno_pyutil/build/lib/seveno_pyutil/logging_utilities/sql_filter.py
# Compiled at: 2019-05-16 05:57:07
# Size of source mod 2**32: 11010 bytes
import enum, logging, timeit
from datetime import date, datetime, timedelta
import pygments, sqlparse
from pygments.formatters import Terminal256Formatter
from pygments.lexers import SqlLexer
try:
    import simplejson as json
except Exception:
    import json

class JsonEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        else:
            if isinstance(o, enum.Enum):
                return o.name
            return super().default(o)


class SQLFilter(logging.Filter):
    __doc__ = "\n    Filter for Django's and SQLAlchemy SQL loggers. Reformats and colorizes\n    queries.\n\n    To use it with Django:\n\n    - add it to ``django.db.backends`` and ``django.db.backends.schema``\n      loggers\n    - remove ``%(message)s`` from log format because it will cause to double\n      emit each SQL statement. Use this filter's placeholder's instead.\n\n    To use it with SQLAlchemy:\n\n    - add it to ``sqlalchemy.engine`` logger and call\n      `:meth:register_sqlalchemy_logging_events`\n\n    Supports following loging placeholders:\n\n    +-------------------+----------------------------------------------+\n    | placeholder       | description                                  |\n    +-------------------+----------------------------------------------+\n    | %(sql)s           | Formatted SQL statement that was executed    |\n    +-------------------+----------------------------------------------+\n    | %(sql_duration)s  | Formatted duration of SQL execution          |\n    +-------------------+----------------------------------------------+\n\n    Arguments:\n        colorize_queries(bool): Should apply shell coloring escape sequences to\n            formatted SQL?\n        multiline_queries(bool): Should emit SQL as indented, multiline of\n            single line log statements? In development it is usually nice to\n            have it be `True`. In production environments, multiline logs are\n            pain and should be avoided.\n\n    Example::\n\n        import logging\n        from logging.config import dictConfig\n\n        from seveno_pyutil import SQLFilter\n\n        try:\n            import sqlalchemy\n            SQLFilter.register_sqlalchemy_logging_events('myapp.db')\n        except ImportError:\n            pass\n\n        dictConfig({\n            'version': 1,\n            'disable_existing_loggers': False,\n            'formatters': {\n                'django_sql': {'format': '(%(sql_duration)s) %(sql)s'},\n                'sqlalchemy_sql': {'format': '(%(sql_duration)s) %(sql)s %(message)s'}\n            },\n            'filters': {\n                'colored_sql': {\n                    '()': 'seveno_pyutil.SQLFilter'\n                    'colorize_queries': True,\n                    'multiline_queries': True,\n                }\n            },\n            'handlers': {\n                'console_django': {\n                    'class': 'logging.StreamHandler',\n                    'level': 'DEBUG',\n                    'formatter': 'django_sql',\n                    'filters': ['colored_sql'],\n                    'stream': 'ext://sys.stdout'\n                },\n                'console_sqlalchemy': {\n                    'class': 'logging.StreamHandler',\n                    'level': 'DEBUG',\n                    'formatter': 'sqlalchemy_sql',\n                    'filters': ['colored_sql'],\n                    'stream': 'ext://sys.stdout'\n                }\n            },\n            'loggers': {\n                'myapp.db': {\n                    'level': 'DEBUG',\n                    'propagate': False,\n                    'handlers': ['console_sqlalchemy']\n                },\n                'django.db.backends': {\n                    'level': 'DEBUG',\n                    'propagate': False,\n                    'handlers': ['console_django']\n                },\n                'django.db.backends.schema': {\n                    'level': 'DEBUG',\n                    'propagate': False,\n                    'handlers': ['console_django']\n                }\n            }\n        })\n\n    "
    KEY_SQL_CUMULATIVE_DURATION = 'cumulative_duration'
    KEY_SQL_COUNT = 'statements_count'

    @classmethod
    def register_sqlalchemy_logging_events(cls, logger, duration_threshold_ms=None, statistics_ctx_get=None):
        """
        Must be called when logging SQLAlchemy statements and durations.

        Arguments:
            logger: name of logger or logging.Logger instance that will be used to log
                SQL messages.
            duration_threshold_ms: If given, only queries lasting longer than this
                threshold will be logged.
            statistics_ctx_get: callable that returns mutable dict. If given, then each
                time SQL query is executes, this dict will be updated.

                It can be used for example in Flask to track SQL execution statistics
                during one HTTP request::

                    import flask
                    from seveno_pyutil import register_sqlalchemy_logging_events

                    def sqlalchemy_stats():
                        return flask.g.setdefault("sqlalchemy_statistics", {})

                    register_sqlalchemy_logging_events(
                        "may_app_sql_logger", statistics_ctx_get=sqlalchemy_stats
                    )

                    @flask.before_request
                    def track_sqlalchemy():
                        @flask.after_this_request
                        def log_sqlalchemy_stats(response):
                            logger.info(
                                "SQLAlchemy statistics for request %s",
                                sqlalchemy_stats()
                            )
                            flask.g["sqlalchemy_statistics"] = {}
        """
        from sqlalchemy import event
        from sqlalchemy.engine import Engine
        _logger = logger
        if isinstance(logger, str):
            _logger = logging.getLogger(logger)
        if duration_threshold_ms is not None:
            if not isinstance(duration_threshold_ms, timedelta):
                duration_threshold_ms = timedelta(milliseconds=duration_threshold_ms)

        def duration_ms(conn):
            return timedelta(milliseconds=((timeit.default_timer() - conn.info['query_start_time'].pop(-1)) * 1000.0))

        @event.listens_for(Engine, 'before_cursor_execute')
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            conn.info.setdefault('query_start_time', []).append(timeit.default_timer())

        @event.listens_for(Engine, 'after_cursor_execute')
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            statement_duration = duration_ms(conn)
            if duration_threshold_ms is not None:
                if statement_duration >= duration_threshold_ms:
                    _logger.warning(('Detected SQL query running longer than {:.3f} ms! '.format(duration_threshold_ms.total_seconds() * 1000)),
                      extra={'sql_statement':statement, 
                     'sql_parameters':parameters, 
                     'sql_duration_ms':statement_duration.total_seconds() * 1000})
            if duration_threshold_ms is None:
                _logger.debug('',
                  extra={'sql_statement':statement, 
                 'sql_parameters':parameters, 
                 'sql_duration_ms':statement_duration.total_seconds() * 1000})
            if statistics_ctx_get:
                try:
                    data = statistics_ctx_get()
                    data.setdefault(cls.KEY_SQL_CUMULATIVE_DURATION, timedelta())
                    data.setdefault(cls.KEY_SQL_COUNT, 0)
                    data[cls.KEY_SQL_CUMULATIVE_DURATION] += statement_duration
                    data[cls.KEY_SQL_COUNT] += 1
                except Exception:
                    _logger.error('Failed to collect SQL statistics!', exc_info=1)

        @event.listens_for(Engine, 'handle_error')
        def receive_handle_error(exception_context):
            _logger.critical('',
              extra={'sql_statement':exception_context.statement, 
             'sql_parameters':exception_context.parameters, 
             'sql_duration_ms':duration_ms(conn).total_seconds() * 1000})

    def __init__(self, colorize_queries=False, multiline_queries=False, *args, **kwargs):
        self.colorize_queries = colorize_queries
        self.multiline_queries = multiline_queries
        (super(SQLFilter, self).__init__)(*args, **kwargs)

    def filter(self, record):
        sql = getattr(record, 'sql_statement', None) or getattr(record, 'sql', None) or ''
        if sql:
            if self.multiline_queries:
                sql = sqlparse.format(sql, reindent=True, keyword_case='upper').strip()
            else:
                sql = ' '.join(l.strip() for l in sqlparse.format(sql,
                  reindent=True, keyword_case='upper').splitlines()).strip()
        else:
            if sql:
                if not sql.endswith(';'):
                    sql = sql + ';'
            if hasattr(record, 'sql_parameters'):
                params_dict = record.sql_parameters
                params = json.dumps((record.sql_parameters), cls=JsonEncoder).strip()
            else:
                params_dict = {}
            params = ''
        if self.colorize_queries:
            if sql:
                sql = pygments.highlight(sql, SqlLexer(), Terminal256Formatter(style='monokai')).strip()
        else:
            if params:
                params = pygments.highlight(params, pygments.lexers.get_lexer_for_mimetype('application/json'), Terminal256Formatter(style='monokai')).strip()
            else:
                if params and params_dict:
                    record.sql = '{} with params {}'.format(sql, params)
                else:
                    record.sql = sql or 'SQL'
            duration = getattr(record, 'sql_duration_ms', None) or getattr(record, 'duration', None)
            if duration:
                record.sql_duration = '{:.3f} ms'.format(duration)
            else:
                record.sql_duration = '_.___ ms'
        return super().filter(record)