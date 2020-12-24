# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/sqlalchemy.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 8321 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import datetime, os, json, pendulum, time, random
from dateutil import relativedelta
from sqlalchemy import event, exc, select
from sqlalchemy.types import Text, DateTime, TypeDecorator
from airflow.utils.log.logging_mixin import LoggingMixin
log = LoggingMixin().log
utc = pendulum.timezone('UTC')

def setup_event_handlers(engine, reconnect_timeout_seconds, initial_backoff_seconds=0.2, max_backoff_seconds=120):

    @event.listens_for(engine, 'engine_connect')
    def ping_connection(connection, branch):
        if branch:
            return
        start = time.time()
        backoff = initial_backoff_seconds
        save_should_close_with_result = connection.should_close_with_result
        while True:
            connection.should_close_with_result = False
            try:
                try:
                    connection.scalar(select([1]))
                    break
                except exc.DBAPIError as err:
                    if time.time() - start >= reconnect_timeout_seconds:
                        log.error('Failed to re-establish DB connection within %s secs: %s', reconnect_timeout_seconds, err)
                        raise
                    else:
                        if err.connection_invalidated:
                            if backoff > initial_backoff_seconds:
                                log.warning('DB connection invalidated. Reconnecting...')
                            else:
                                log.debug('DB connection invalidated. Initial reconnect')
                            backoff += backoff * random.random()
                            time.sleep(min(backoff, max_backoff_seconds))
                            continue
                        else:
                            log.error('Unknown database connection error. Not retrying: %s', err)
                            raise

            finally:
                connection.should_close_with_result = save_should_close_with_result

    @event.listens_for(engine, 'connect')
    def connect(dbapi_connection, connection_record):
        connection_record.info['pid'] = os.getpid()

    if engine.dialect.name == 'sqlite':

        @event.listens_for(engine, 'connect')
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute('PRAGMA foreign_keys=ON')
            cursor.close()

    if engine.dialect.name == 'mysql':

        @event.listens_for(engine, 'connect')
        def set_mysql_timezone(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("SET time_zone = '+00:00'")
            cursor.close()

    @event.listens_for(engine, 'checkout')
    def checkout(dbapi_connection, connection_record, connection_proxy):
        pid = os.getpid()
        if connection_record.info['pid'] != pid:
            connection_record.connection = connection_proxy.connection = None
            raise exc.DisconnectionError('Connection record belongs to pid {}, attempting to check out in pid {}'.format(connection_record.info['pid'], pid))


class UtcDateTime(TypeDecorator):
    __doc__ = "\n    Almost equivalent to :class:`~sqlalchemy.types.DateTime` with\n    ``timezone=True`` option, but it differs from that by:\n\n    - Never silently take naive :class:`~datetime.datetime`, instead it\n      always raise :exc:`ValueError` unless time zone aware value.\n    - :class:`~datetime.datetime` value's :attr:`~datetime.datetime.tzinfo`\n      is always converted to UTC.\n    - Unlike SQLAlchemy's built-in :class:`~sqlalchemy.types.DateTime`,\n      it never return naive :class:`~datetime.datetime`, but time zone\n      aware value, even with SQLite or MySQL.\n    - Always returns DateTime in UTC\n\n    "
    impl = DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not isinstance(value, datetime.datetime):
                raise TypeError('expected datetime.datetime, not ' + repr(value))
            else:
                if value.tzinfo is None:
                    raise ValueError('naive datetime is disallowed')
            return value.astimezone(utc)

    def process_result_value(self, value, dialect):
        """
        Processes DateTimes from the DB making sure it is always
        returning UTC. Not using timezone.convert_to_utc as that
        converts to configured TIMEZONE while the DB might be
        running with some other setting. We assume UTC datetimes
        in the database.
        """
        if value is not None:
            if value.tzinfo is None:
                value = value.replace(tzinfo=utc)
            else:
                value = value.astimezone(utc)
        return value


class Interval(TypeDecorator):
    impl = Text
    attr_keys = {datetime.timedelta: ('days', 'seconds', 'microseconds'), 
     relativedelta.relativedelta: ('years', 'months', 'days', 'leapdays', 'hours', 'minutes', 'seconds', 'microseconds',
 'year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond')}

    def process_bind_param(self, value, dialect):
        if type(value) in self.attr_keys:
            attrs = {key:getattr(value, key) for key in self.attr_keys[type(value)]}
            return json.dumps({'type':type(value).__name__,  'attrs':attrs})
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if not value:
            return value
        else:
            data = json.loads(value)
            if isinstance(data, dict):
                type_map = {key.__name__:key for key in self.attr_keys}
                return (type_map[data['type']])(**data['attrs'])
            return data