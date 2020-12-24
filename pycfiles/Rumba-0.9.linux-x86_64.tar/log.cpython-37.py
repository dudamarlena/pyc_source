# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/rumba/log.py
# Compiled at: 2018-08-31 05:12:05
# Size of source mod 2**32: 10587 bytes
import logging, logging.handlers, multiprocessing, sys, time
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
loggers_set = set()
mq = multiprocessing.Queue()
logging_listener = None
try:
    from logging.handlers import QueueHandler
except ImportError:

    class QueueHandler(logging.Handler):
        __doc__ = '\n        This handler sends events to a queue. Typically, it would be used\n        together with a multiprocessing Queue to centralise logging to file\n        in one process (in a multi-process application), so as to avoid file\n        write contention between processes.\n\n        This code is new in Python 3.2, but this class can be copy pasted into\n        user code for use with earlier Python versions.\n        '

        def __init__(self, queue):
            logging.Handler.__init__(self)
            self.queue = queue

        def enqueue(self, record):
            self.queue.put_nowait(record)

        def prepare(self, record):
            self.format(record)
            record.msg = record.message
            record.args = None
            record.exc_info = None
            return record

        def emit(self, record):
            try:
                self.enqueue(self.prepare(record))
            except Exception:
                self.handleError(record)


try:
    from logging.handlers import QueueListener
except ImportError:
    import threading
    try:
        import Queue
    except ImportError:
        import queue as Queue

    class QueueListener(object):
        __doc__ = '\n        This class implements an internal threaded listener which watches for\n        LogRecords being added to a queue, removes them and passes them to a\n        list of handlers for processing.\n        '
        _sentinel = None

        def __init__(self, queue, respect_handler_level=False, *handlers):
            self.queue = queue
            self.handlers = handlers
            self._stop = threading.Event()
            self._thread = None
            self.respect_handler_level = respect_handler_level

        def dequeue(self, block):
            return self.queue.get(block)

        def start(self):
            self._thread = t = threading.Thread(target=(self._monitor))
            t.setDaemon(True)
            t.start()

        def prepare(self, record):
            return record

        def handle(self, record):
            record = self.prepare(record)
            for handler in self.handlers:
                if not self.respect_handler_level:
                    process = True
                else:
                    process = record.levelno >= handler.level
                if process:
                    handler.handle(record)

        def _monitor(self):
            q = self.queue
            has_task_done = hasattr(q, 'task_done')
            while not self._stop.isSet():
                try:
                    record = self.dequeue(True)
                    if record is self._sentinel:
                        break
                    self.handle(record)
                    if has_task_done:
                        q.task_done()
                except Queue.Empty:
                    pass

            while True:
                try:
                    record = self.dequeue(False)
                    if record is self._sentinel:
                        break
                    self.handle(record)
                    if has_task_done:
                        q.task_done()
                except Queue.Empty:
                    break

        def enqueue_sentinel(self):
            self.queue.put_nowait(self._sentinel)

        def stop(self):
            self._stop.set()
            self.enqueue_sentinel()
            self._thread.join()
            self._thread = None


class RumbaFormatter(logging.Formatter):
    __doc__ = '\n    The `logging.Formatter` subclass used by Rumba\n    '
    level_name_table = {'CRITICAL':'CRT', 
     'ERROR':'ERR', 
     'WARNING':'WRN', 
     'INFO':'INF', 
     'DEBUG':'DBG', 
     'CRT':'CRT', 
     'ERR':'ERR', 
     'WRN':'WRN', 
     'INF':'INF', 
     'DBG':'DBG'}

    def __init__(self):
        super(RumbaFormatter, self).__init__(fmt='%(asctime)s | %(levelname)3.3s | %(name)11.11s | %(message)s',
          datefmt='%H:%M:%S')

    def format(self, record):
        record.name = record.name.split('.')[(-1)]
        record.levelname = self.level_name_table[record.levelname]
        return super(RumbaFormatter, self).format(record)


def setup():
    """Configures the logging framework with default values."""
    global mq
    queue_handler = QueueHandler(mq)
    queue_handler.setLevel(logging.DEBUG)
    logging.basicConfig(handlers=[queue_handler], level=(logging.DEBUG))
    logging.getLogger('').setLevel(logging.ERROR)
    logging.getLogger('rumba').setLevel(logging.INFO)


def _get_logger_with_setup(name):
    global _get_logger
    setup()
    _get_logger = _get_logger_without_setup
    return logging.getLogger(name)


def _get_logger_without_setup(name):
    return logging.getLogger(name)


_get_logger = _get_logger_with_setup

def get_logger(name):
    """
    Returns the logger named `name`.

    `name` should be the module name, for consistency.

    If setup has not been called yet, it will call it first.

    :param name: the name of the desired logger
    :type name: `str`
    :return: The logger
    """
    return _get_logger(name)


def set_logging_level(level, name=None):
    """
    Set the current logging level to `level` for the logger named `name`.
    If `name` is not specified, sets the logging level for all rumba loggers.

    :param level: the desired logging level, in string or int form.
    :type level: `str` or `int`
    :param name: The name of the logger to configure
    :type name: `str`

    .. note:: Accepted levels are:

              - DEBUG == 10,
              - INFO == 20,
              - WARNING == 30,
              - ERROR == 40,
              - CRITICAL == 50,
              - NOTSET == 0 (resets the logger: its level is set to
                the default or its parents' level)
    """
    if name is None:
        if level == 'NOTSET' or level == 0:
            set_logging_level(logging.INFO)
            return
        name = 'rumba'
    if level == 'NOTSET' or level == 0:
        if name == '':
            set_logging_level(logging.ERROR, '')
            return
    logger = get_logger(name)
    loggers_set.add(logger)
    logger.setLevel(level)


def reset_logging_level():
    """
    Resets the current logging level of all loggers to the default.
    For the Rumba library the default is INFO.
    """
    for logger in loggers_set:
        logger.setLevel(logging.NOTSET)

    set_logging_level(logging.INFO)
    set_logging_level(logging.ERROR, '')


def flush_log():
    """
    Flush the log.
    """
    time.sleep(0.1)


def flush_and_kill_logging():
    """
    Flushes all queued log messages and stops the logging facility.
    Since the logging is done by a daemon thread, log entries might be lost
    if execution is interrupted abruptly. Call this method to make sure
    this does not happen.
    """
    global logging_listener
    logging_listener.stop()


class LogOptions(object):
    __doc__ = 'Class holding the logging configuration'

    def __init__(self):
        global logging_listener
        logging_listener = QueueListener(mq)
        self.log_to_console()
        logging_listener.start()

    @staticmethod
    def _get_handlers():
        return tuple(logging_listener.handlers)

    @staticmethod
    def _set_handlers(*handlers):
        logging_listener.handlers = handlers

    def _add_handler(self, handler):
        handler.setFormatter(RumbaFormatter())
        handler.setLevel(DEBUG)
        handlers = self._get_handlers() + (handler,)
        (self._set_handlers)(*handlers)
        return self

    def log_to_file(self, path='rumba.log'):
        """
        Set the logging framework to log to file on top of the other
        logging facilities.

        :param path: logging file filename
        :type path: `str`
        :return: this `.LogOptions` instance
        """
        new_handler = logging.handlers.RotatingFileHandler(path)
        return self._add_handler(new_handler)

    def reset_logging(self):
        """
        Disable all logging facilities

        :return: this `.LogOptions` instance
        """
        (self._set_handlers)(*tuple())
        return self

    def log_to_console(self):
        """
        Set the logging framework to log to stdout on top of the
        other configured logging facilities

        :return: this `.LogOptions` instance
        """
        new_handler = logging.StreamHandler(sys.stdout)
        return self._add_handler(new_handler)


options = LogOptions()