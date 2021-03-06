# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dblogger/logger.py
# Compiled at: 2015-04-26 18:06:04
""":mod:`logging` handler that stores log messages in a database.

.. This software is released under an MIT/X11 open source license.
   Copyright 2013-2014 Diffeo, Inc.

"""
from __future__ import absolute_import
import time, logging, cPickle as pickle, sys, traceback
try:
    from tblib import pickling_support
    pickling_support.install()
except Exception as exc:
    pass

from dblogger.utils import gen_uuid
import kvlayer, yakonfig

class DatabaseLogHandler(logging.Handler):
    """Log handler that stores log messages in a database.

    This uses :mod:`kvlayer` to store the actual log messages.
    When the log handler is created, the caller needs to pass
    in either the :mod:`kvlayer` configuration or the actual
    :class:`kvlayer.AbstractStorage` object.  The constructor
    also accepts a virtual table name, defaulting to ``log``.

    If a global YAML file is used to configure the application, then
    YAML reference syntax can be used to share this handler's
    configuration with the global kvlayer configuration.

    .. code-block:: yaml

        kvlayer: &kvlayer
          storage_type: redis
          storage_addresses: [ 'redis.example.com:6379' ]
        logging:
          handlers:
            db:
              class: dblogger.DatabaseLogHandler
              storage_config: *kvlayer

    Log messages are stored in a table with a single UUID key, where
    the high-order bits of the UUID are in order by time.  The actual
    table values are serialized JSON representations of the log
    records.

    This log handlers adds a format string property ``%(humantime)s``
    with a time in a fixed format, and ``%(exc_text)s`` with the
    formatted traceback from an exception.  These properties are also
    included in the JSON stored in the database..

    .. automethod:: __init__

    """

    def __init__(self, storage_client=None, table_name='log', storage_config=None):
        """Create a new database log handler.

        You must either pass in ``storage_client``, an actual kvlayer
        client object, or ``storage_config``, a dictionary which will
        be passed to ``kvlayer.client()``.  Log messages
        will be stored in the table ``table_name``.

        :param storage_client: existing storage client
        :type storage_client: :class:`kvlayer.AbstractStorage`
        :param str table_name: virtual table name
        :param dict storage_config: configuration for new storage client

        """
        super(DatabaseLogHandler, self).__init__()
        if storage_client is None:
            if storage_config is None:
                raise RuntimeError('must pass either storage_client or storage_config')
            with yakonfig.defaulted_config([
             kvlayer], config=dict(kvlayer=storage_config)):
                storage_client = kvlayer.client()
        self.storage = storage_client
        self.table_name = table_name
        storage_client.setup_namespace({table_name: 1})
        self.sequence_number = 0
        return

    def formatDBTime(self, record):
        record.humantime = time.strftime('%Y-%m-%dT%H:%M:%S-%Z', time.localtime(record.created))

    @classmethod
    def deserialize(cls, rec_pickle):
        try:
            xdict = pickle.loads(rec_pickle)
        except Exception:
            xdict = {'msg': 'warning!!!! failed to unpickle: %r' % rec_pickle}

        return logging.makeLogRecord(xdict)

    def emit(self, record):
        """
        handle a record by formatting parts of it, and pushing it into
        storage.
        """
        self.format(record)
        self.formatDBTime(record)
        failure = []
        if record.args:
            try:
                record.msg = record.msg % record.args
                record.args = None
            except Exception as exc:
                failure.append('failed to run string formatting on provided args')
                failure.append(traceback.format_exc(exc))
                failure.append('record.msg = %r' % record.msg)
                failure.append('record.args = %r' % (record.args,))
                failure.append('logging failed so shutting down entire process')

        if record.exc_info:
            record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
        else:
            record.exc_text = ''
        new_uuid = gen_uuid(record.created, self.sequence_number)
        self.sequence_number += 1
        try:
            dbrec = pickle.dumps(record.__dict__, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as exc:
            failure.append('failed to dump log record, will shutdown')
            failure.append(traceback.format_exc(exc))
            failure.append('failed to pickle the __dict__ on: record=%r' % record)
            failure.append('failed to pickle: record.__dict__=%r' % record.__dict__)
            failure.append('logging failed so shutting down entire process')

        if failure:
            dbrec = ('\n').join(failure)
        self.storage.put(self.table_name, ((new_uuid,), dbrec))
        if failure:
            sys.exit(dbrec)
        return