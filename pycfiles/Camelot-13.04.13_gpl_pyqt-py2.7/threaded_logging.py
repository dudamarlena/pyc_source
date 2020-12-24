# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/core/threaded_logging.py
# Compiled at: 2013-04-11 17:47:52
"""
Logging is an important aspect of every application, as logs provide valuable
feedback to developers and first line support.  Camelot adds some
additional functions on top of the standard Python logging library.

The added functionallity is needed for two reasons :
    
    * Camelot applications are often installed in a distributed fashion.  Thus
      the log files need to be collected to provide meaningfull information to
      the developer.
      
    * Logging should never slow down/freeze the application.  Even when logging
      to files this may happen, since the application never knows for sure if
      a file is really local, and network connections may turn slow at any
      time.

Both issues are resolved by using a logging handler that collects all logs, and
periodically sends them to an http server in the background::
    
    handler = ThreadedHttpHandler('www.example.com:80', '/my_logs/')
    handler.setLevel(logging.INFO)
    logging.root.addHandler(handler)

The logging url could include a part indentifying the user and as such assisting
first line support.
"""
from PyQt4 import QtCore
import getpass, logging
from logging import handlers
import sys
LOGGER = logging.getLogger('camelot.core.logging')

class ThreadedTimer(QtCore.QThread):
    """Thread that checks every interval milli seconds if there 
    are logs to be sent to the server"""

    def __init__(self, interval, handler):
        QtCore.QThread.__init__(self)
        self._timer = None
        self._interval = interval
        self._handler = handler
        return

    def run(self):
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._handler.timeout)
        self._timer.start(self._interval)
        self.exec_()


class ThreadedHttpHandler(handlers.HTTPHandler):
    """An Http Logging handler that does the logging itself in a different 
    thread, to prevent slow down of the main thread"""

    def __init__(self, host, url, method='GET'):
        handlers.HTTPHandler.__init__(self, host, url, method)
        self._records_to_emit = []
        self._threaded_timer = ThreadedTimer(1000, self)
        self._threaded_timer.start()

    @QtCore.pyqtSlot()
    def timeout(self):
        while len(self._records_to_emit):
            record = self._records_to_emit.pop()
            handlers.HTTPHandler.emit(self, record)

    def emit(self, record):
        self._records_to_emit.append(record)


class ThreadedAwsHandler(logging.Handler):
    """A logging handler that sends the logs to an AWS queue through the
    SQS, this handler requires the boto library"""

    def __init__(self, access_key, secret_access_key, queue_name, revision=0, connection_kwargs={}):
        """:param connection_kwargs: arguments to be used when creating the
        underlying boto connection to aws"""
        logging.Handler.__init__(self)
        self._access_key = access_key
        self._secret_access_key = secret_access_key
        self._connection_kwargs = connection_kwargs
        self._queue_name = queue_name
        self._records_to_emit = []
        self._queue = None
        self._connected = True
        self._threaded_timer = ThreadedTimer(1000, self)
        self._threaded_timer.start()
        self._max_cache = 1000
        try:
            if sys.platform.startswith('win'):
                self._user = getpass.getuser().decode('mbcs')
            else:
                self._user = getpass.getuser()
        except Exception:
            self._user = getpass.getuser().encode('ascii', 'ignore')

        self._revision = revision
        return

    def emit(self, record):
        import json
        if len(self._records_to_emit) >= self._max_cache:
            return
        else:
            ei = record.exc_info
            if record.name and record.name.startswith('boto'):
                return
            if ei:
                self.format(record)
                record.exc_info = None
            record_dict = dict(user=self._user, revision=self._revision)
            record_dict.update(record.__dict__)
            self._records_to_emit.append(json.dumps(record_dict))
            if ei:
                record.exc_info = ei
            return

    @QtCore.pyqtSlot()
    def timeout(self):
        from boto.sqs.message import Message
        if not self._queue and self._connected:
            try:
                from boto.sqs.connection import SQSConnection
                sqs_connection = SQSConnection(self._access_key, self._secret_access_key, **self._connection_kwargs)
                self._queue = sqs_connection.get_queue(self._queue_name)
                if self._queue == None:
                    raise Exception('Queue %s does not exist' % self._queue_name)
            except Exception as e:
                LOGGER.error('Could not connect to logging queue %s' % self._queue_name, exc_info=e)
                self._connected = False

        while len(self._records_to_emit) and self._connected:
            record = self._records_to_emit.pop()
            self._queue.write(Message(body=record))

        return


class CloudLaunchHandler(ThreadedAwsHandler):
    """A logging handler that sends the logs to the Cloud Launch service,
    requires the cloudlaunch library, and only works with applications tested
    or deployed through cloudlaunch
    
    The cloudlaunch record can be obtained using the get_cloud_record
    method of the cloudlaunch.resources module.
    """

    def __init__(self, cloud_record, connection_kwargs={}):
        """:param cloud_record: the cloud record describing the application
        """
        queue_name = 'cloudlaunch-%s-%s-logging' % (cloud_record.author.replace(' ', '_'), cloud_record.name.replace(' ', '_'))
        ThreadedAwsHandler.__init__(self, cloud_record.public_access_key, cloud_record.public_secret_key, queue_name, revision=cloud_record.revision, connection_kwargs=connection_kwargs)