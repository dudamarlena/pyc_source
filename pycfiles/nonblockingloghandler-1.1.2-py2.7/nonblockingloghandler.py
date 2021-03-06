# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\nonblockingloghandler.py
# Compiled at: 2013-04-19 12:03:39
"""
    Provides a NonblockingLogHandler class consistent with the Python logging
    subsystem.

    This handler acts as a proxy for the another log handler that may be slow
    to execute: e.g. the SMTPHandler, SocketHandler, SysLogHandler - especially
    when they are talking to remote servers.

    If you have a real-time system (i.e. one where a late response is a wrong
    response) and you are sending log messages via email, http, syslog, etc.,
    you should consider using this module to protect against unexpected delays.

    It is intended to be a drop-in replacement (see provisos below) for your
    proxied handler. Unlike the proxied handler, this handler which returns
    quickly, and executes the actually logging in the background, in a separate
    thread.

    Provisos:

    * If you pass an objects to the logging functions, be aware that their
      __str__() functions should be fast. I/O bound str() calls are outside the
      scope of this module.

      Execution of str() functions on message parameters and string formatting
      is done immediately, in the calling thread. This is to guarantee both
      the thread-safety of the logged objects and also that the log shows the
      object's values at the time of the call, not the time of the emit.

    * If you subclass from Formatter, note that it will not have the user
      parameters from the logging call passed to it. It will only receive the
      resulting message string formatted according to the client's wishes. It
      can still format dates, threadnames, levels, etc.

    * If you subclass from Filter, be aware that they should be fast. I/O-bound
      filters are outside of the scope of this module.

    * Clients should not directly call format() or emit() on the
      NonblockingLogHandler class. Consider them private.

    * Once the NonblockingLogHandler handler is initialised, any further calls
      to setLevel(), addFilter and removeFilter() made on the delegated handler
      are ignored by the proxy handler. Conversely, the delegated handler is
      not informed of calls made on the NonblockingLogHandler instance.

      Best practice would be to only update the NonblockingLogHandler handler,
      and not use the values stored in the delegated handler.
      
    * If the close() method is called on the NonblockingLogHandler handler,
      there is no need to call close() on the delegated handler; it will be
      called when the delegated handler is no longer required.

    Example usage:
        nonblocking_email_handler = nonblockingloghandler.NonblockingLogHandler(
                logging.SMTPHandler(
                    "localhost", "logging_system@example.com",
                    "admin@example.com", "Log message")
                )
        db_logger = logging.getLogger("database")
        database_logger.addHandler(nonblocking_email_handler)

        # This operation will return immediately, before email is sent.
        db_logger.critical("Database corrupted") 

        nonblocking_email_handler.close()
"""
import logging, sys
from threading import Thread
from autoclosingqueue import Queue
from nonblockingloghandlerversion import __version__

class NonblockingLogHandler(logging.Handler):
    """ Provides a NonblockingLogHandler class consistent with the Python logging
        subsystem. """
    SENTINEL = None

    def __init__(self, destination_handler, level=logging.NOTSET):
        self.message_queue = Queue()
        self.consumer_thread = Thread(name='NonblockingLogHandler.consumer', target=NonblockingLogHandler._consume, args=(
         self.message_queue, destination_handler))
        self.consumer_thread.daemon = True
        self.consumer_thread_started = False
        self.closed = False
        logging.Handler.__init__(self, level)

    def close(self):
        if not self.closed:
            self.closed = True
            self.message_queue.put(self.SENTINEL)

    def createLock(self):
        pass

    def acquire(self):
        pass

    def release(self):
        pass

    def emit(self, record):
        raise NotImplementedError('Emit should not be directly called on %s. Call handle() instead.' % self.__class__)

    def format(self, record):
        raise NotImplementedError('Format is considered private by %s' % self.__class__)

    def setFormatter(self, fmt):
        self._delegate('setFormatter', (fmt,))

    def flush(self):
        self._delegate('flush')

    def handle(self, record):
        if record.args:
            record.msg = record.msg % record.args
            record.args = []
        self._delegate('handle', (record,))

    def _delegate(self, attribute_name, args=[], kwargs={}):
        """Submit request to consumer thread."""
        self.message_queue.put((attribute_name, args, kwargs))
        if not self.consumer_thread_started:
            self.consumer_thread_started = True
            try:
                self.consumer_thread.start()
            except RuntimeError:
                pass

    @staticmethod
    def _consume(queue, destination_handler):
        """ Target of consumer thread.
            Execute methods sent through queue against (possibly slow)
            destination_handler, until told to stop or killed as a daemon
            thread.
            """
        try:
            while True:
                item = queue.get()
                if item == NonblockingLogHandler.SENTINEL:
                    queue.task_done()
                    break
                else:
                    attribute_name, args, kwargs = item
                    getattr(destination_handler, attribute_name)(*args, **kwargs)
                    queue.task_done()

        except Exception as unexpected_exception:
            sys.stderr.write('Unexpected exception (%s) in nonblockingloghander thread. Log messages can no longer be emitted.\n' % unexpected_exception)